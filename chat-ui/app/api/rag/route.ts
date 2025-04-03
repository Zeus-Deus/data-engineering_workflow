export async function POST(req: Request) {
  try {
    const { question } = await req.json();
    
    console.log("Sending request to RAG API with question:", question);

    // Send the question to the FastAPI backend
    const response = await fetch(`${process.env.API_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("RAG API error:", response.status, errorText);
      return Response.json({ error: `RAG API error: ${response.status}` }, { status: 500 });
    }

    const data = await response.json();
    console.log("Received response from RAG API:", data);
    
    return Response.json(data);
  } catch (error) {
    console.error("Error in RAG API:", error);
    return Response.json({ error: "Failed to process your request" }, { status: 500 });
  }
} 