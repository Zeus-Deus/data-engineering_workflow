// Import the environment helper
import { FASTAPI_URL } from '../../../lib/environment';

export async function POST(req: Request) {
  const { messages } = await req.json();

  try {
    const userMessage = messages[messages.length - 1].content;
    console.log("Sending question to FastAPI:", userMessage);

    // Call FastAPI endpoint
    const response = await fetch(`${FASTAPI_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: userMessage }),
    });

    if (!response.ok) {
      throw new Error(`FastAPI backend error: ${response.status}`);
    }

    const data = await response.json();
    console.log("FastAPI response:", data);
    
    // Return the response directly since FastAPI already formats it correctly
    return new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json" }
    });
  } catch (error) {
    console.error("Error:", error);
    return new Response(
      JSON.stringify({ error: "Failed to process your request" }),
      { status: 500 }
    );
  }
}

