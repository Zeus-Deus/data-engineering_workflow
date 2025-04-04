// Import the environment helper
import { FASTAPI_URL } from '../../../lib/environment';

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();
    
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return new Response(
        JSON.stringify({ error: "Invalid request: messages array is required" }),
        { status: 400 }
      );
    }

    const userMessage = messages[messages.length - 1].content;
    if (!userMessage || typeof userMessage !== 'string') {
      return new Response(
        JSON.stringify({ error: "Invalid request: message content is required" }),
        { status: 400 }
      );
    }

    console.log("Sending question to FastAPI:", userMessage);

    // Call FastAPI endpoint
    const response = await fetch(`${FASTAPI_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: userMessage }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`FastAPI backend error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log("FastAPI response:", data);
    
    // Transform the response to match our Message type
    const assistantMessage = {
      id: Date.now().toString(),
      role: "assistant" as const,
      content: data.answer
    };
    
    return new Response(JSON.stringify(assistantMessage), {
      headers: { "Content-Type": "application/json" }
    });
  } catch (error) {
    console.error("Error:", error);
    const errorMessage = error instanceof Error ? error.message : "Failed to process your request";
    return new Response(
      JSON.stringify({ error: errorMessage }),
      { status: 500 }
    );
  }
}

