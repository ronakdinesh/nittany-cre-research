/// <reference types="@cloudflare/workers-types" />
import { Parallel } from "parallel-web";
import { createGroq } from "@ai-sdk/groq";
import { streamText, tool, stepCountIs } from "ai";
import { z } from "zod/v4";
import { rateLimitMiddleware } from "./ratelimit";
//@ts-ignore
import indexHtml from "./index.html";

export interface Env {
  PARALLEL_API_KEY: string;
  GROQ_API_KEY: string;
  RATE_LIMIT_KV: KVNamespace;
}

function getClientIP(request: Request): string {
  const cfConnectingIP = request.headers.get("CF-Connecting-IP");
  if (cfConnectingIP) return cfConnectingIP;

  const xForwardedFor = request.headers.get("X-Forwarded-For");
  if (xForwardedFor) return xForwardedFor.split(",")[0].trim();

  const xRealIP = request.headers.get("X-Real-IP");
  if (xRealIP) return xRealIP;

  return "unknown";
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    // Ensure required environment variables are present
    if (!env.PARALLEL_API_KEY || !env.GROQ_API_KEY) {
      return new Response("Missing required API keys", { status: 500 });
    }

    if (!env.RATE_LIMIT_KV) {
      return new Response("Rate limiting service unavailable", { status: 500 });
    }

    // Serve the HTML page
    if (request.method === "GET") {
      return new Response(indexHtml, {
        headers: { "Content-Type": "text/html" },
      });
    }

    // Handle research requests with rate limiting
    if (request.method === "POST") {
      // Apply rate limiting - config builder gets access to request
      const rateLimitResponse = await rateLimitMiddleware(env.RATE_LIMIT_KV, {
        limits: [
          {
            name: "IP hourly",
            requests: 100,
            windowMs: 60 * 60 * 1000, // 1 hour
            limiter: getClientIP(request), // Actual IP address
          },
          {
            name: "Global per minute",
            requests: 100,
            windowMs: 60 * 1000, // 1 minute
            limiter: "global", // Hardcoded global limiter
          },
          {
            name: "Global daily",
            requests: 10000,
            windowMs: 24 * 60 * 60 * 1000, // 1 day
            limiter: "global", // Hardcoded global limiter
          },
        ],
      });

      if (rateLimitResponse) {
        return rateLimitResponse;
      }

      try {
        const { query, systemPrompt } = await request.json<any>();
        console.log({ query });
        if (!query) {
          return new Response("Query is required", { status: 400 });
        }

        const execute = async ({ objective }) => {
          const parallel = new Parallel({
            apiKey: env.PARALLEL_API_KEY,
          });

          const searchResult = await parallel.beta.search({
            // Choose objective or search queries. We choose objective because it allows natural language way of describing what you're looking for
            objective,
            search_queries: undefined,
            // "base" works best for apps where speed is important, while "pro" is better when freshness and content-quality is critical
            processor: "base",

            source_policy: {
              exclude_domains: undefined,
              include_domains: undefined,
            },
            max_results: 10,
            // Keep low to save tokens
            max_chars_per_result: 2500,
          });
          return searchResult;
        };

        // Define the search tool
        const searchTool = tool({
          description: `# Commercial Real Estate Research Tool - Global & MENA Markets

**Purpose:** Search for current commercial real estate data, property information, market trends, and investment insights for global markets, with particular strength in MENA (Middle East and North Africa) markets.

**Usage:**
- objective: Natural-language description of your commercial real estate research goal (max 200 characters)
  MENA Examples:
  - "Find recent sales comps for office buildings in Dubai Marina"
  - "Current market cap rates for retail properties in Riyadh, Saudi Arabia"
  - "Office property prices in UAE"
  - "Industrial lease rates in KSA"
  - "Zoning regulations for mixed-use development in New Cairo, Egypt"
  - "Demographics and economic indicators for Abu Dhabi, UAE"
  - "Industrial property lease rates in Doha, Qatar"
  
  Global Examples:
  - "Office property prices per square foot in Manhattan, New York"
  - "Retail vacancy rates in London, UK"
  - "Industrial cap rates in Singapore"
  - "Residential property trends in Tokyo, Japan"
  - "Hospitality investment opportunities in European markets"

**Best Practices:**
- Specify property type (office, retail, industrial, residential, hospitality, etc.)
- Include location details (city, country, district/area)
- Request specific metrics (price per sqft/sq meter, cap rates, yield rates, vacancy rates, etc.)
- Mention if you need recent/current data (real estate markets are dynamic)
- Keep objectives concise but include key search terms for real estate databases and sources
- For MENA markets, consider regional variations in measurement units and market practices`,
          inputSchema: z.object({
            objective: z
              .string()
              .describe(
                "Natural-language description of your commercial real estate research goal (max 200 characters)"
              ),
          }),
          execute,
        });

        // Initialize Groq provider
        const groq = createGroq({
          apiKey: env.GROQ_API_KEY,
        });

        // Stream the research process
        const result = streamText({
          model: groq("meta-llama/llama-4-maverick-17b-128e-instruct"),
          system:
            systemPrompt ||
            `You are a commercial real estate research agent specializing in global property analysis, market research, and investment insights, with particular expertise in MENA (Middle East and North Africa) markets. You have access to a web search tool to gather current market data, property information, and commercial real estate intelligence worldwide.

Your expertise includes:
- Commercial property valuations and comps globally (with deep knowledge of MENA markets: Dubai, Riyadh, Cairo, Abu Dhabi, Doha, UAE, KSA, etc.)
- Market trends and analysis (office, retail, industrial, residential, hospitality) across global and MENA markets
- Zoning and regulatory information for jurisdictions worldwide, including MENA, UAE, and KSA
- Property history and ownership details in global and MENA markets
- Area demographics and economic indicators for cities and regions globally
- Investment analysis, cap rates, and yield rates in global and MENA markets
- Lease rates and market comparables across international and MENA cities

Instructions:
1. For ANY user query about commercial real estate (global or MENA-specific), use the search tool to gather current, accurate data
2. Conduct 1-3 searches from different angles (e.g., property details, market trends, comparable properties)
3. Provide comprehensive, data-driven answers with specific metrics, dates, and sources
4. Focus on actionable insights for real estate professionals, investors, and brokers operating globally or in MENA markets
5. When researching MENA markets, be aware of regional variations in regulations, market practices, and currency (AED, SAR, EGP, QAR, etc.)
6. For global queries, adapt your research approach to the specific market's conventions and data availability

The current date is ${new Date(Date.now()).toISOString().slice(0, 10)}

IMPORTANT: Always use the search tool to gather current market data - commercial real estate information changes frequently and requires up-to-date sources!`,
          prompt: query,
          tools: { search: searchTool },
          toolChoice: "auto",
          stopWhen: stepCountIs(25),
          maxOutputTokens: 8000,
        });

        // Return the streaming response
        const encoder = new TextEncoder();
        const stream = new ReadableStream({
          async start(controller) {
            try {
              for await (const chunk of result.fullStream) {
                const data = `data: ${JSON.stringify(chunk)}\n\n`;
                controller.enqueue(encoder.encode(data));
              }
              controller.enqueue(encoder.encode("data: [DONE]\n\n"));
            } catch (error) {
              console.error("Stream error:", error);
              controller.enqueue(
                encoder.encode(
                  `data: ${JSON.stringify({
                    type: "error",
                    error: error.message || "Unknown error occurred",
                  })}\n\n`
                )
              );
            } finally {
              controller.close();
            }
          },
        });

        return new Response(stream, {
          headers: {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            Connection: "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
          },
        });
      } catch (error) {
        console.error("Research error:", error);
        return new Response(JSON.stringify({ error: error.message }), {
          status: 500,
          headers: { "Content-Type": "application/json" },
        });
      }
    }

    return new Response("Not found", { status: 404 });
  },
} satisfies ExportedHandler<Env>;
