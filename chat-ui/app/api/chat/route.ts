import { openai } from "@ai-sdk/openai"
import { streamText } from "ai"

// Allow streaming responses up to 30 seconds
export const maxDuration = 30

export async function POST(req: Request) {
  const { messages } = await req.json()

  // This is where you'll connect to your Python RAG backend
  // For now, we'll use a direct OpenAI call as a placeholder
  try {
    // Option 1: Call your Python backend API
    // const response = await fetch('http://your-python-backend/query', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ query: messages[messages.length - 1].content }),
    // });
    // const data = await response.json();

    // Option 2: Direct OpenAI call (placeholder)
    const result = streamText({
      model: openai("gpt-4o"),
      messages,
      system:
        "You are a helpful assistant that answers questions based on the user's documents. If you don't know the answer, say so.",
    })

    return result.toDataStreamResponse()
  } catch (error) {
    console.error("Error:", error)
    return new Response(JSON.stringify({ error: "Failed to process your request" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    })
  }
}

