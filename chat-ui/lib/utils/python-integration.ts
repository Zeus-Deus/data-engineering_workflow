/**
 * Utility functions for integrating with the Python RAG backend
 */

// Function to send a query to the Python backend
export async function queryRagSystem(query: string) {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_FASTAPI_URL;
    if (!backendUrl) {
      throw new Error("Environment variable NEXT_PUBLIC_FASTAPI_URL is not set.");
    }

    const response = await fetch(`${backendUrl}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Failed to query RAG system:", error);
    throw error;
  }
}

// Function to stream responses from the Python backend
export async function streamFromPythonBackend(query: string, onChunk: (chunk: unknown) => void) {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_FASTAPI_URL;
    if (!backendUrl) {
      throw new Error("Environment variable NEXT_PUBLIC_FASTAPI_URL is not set.");
    }

    const response = await fetch(`${backendUrl}/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) throw new Error("Response body is null");

    const decoder = new TextDecoder();
    let buffer = ""; // Buffer to accumulate incomplete JSON chunks

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      // Decode the chunk and append it to the buffer
      buffer += decoder.decode(value, { stream: true });

      // Attempt to parse complete JSON objects from the buffer using newline as a delimiter
      const boundary = buffer.lastIndexOf("\n");
      if (boundary !== -1) {
        const completeChunks = buffer.slice(0, boundary).split("\n");
        buffer = buffer.slice(boundary + 1); // Keep the remaining incomplete chunk

        for (const chunk of completeChunks) {
          try {
            const parsed = JSON.parse(chunk);
            onChunk(parsed); // Pass the parsed JSON object to the callback
          } catch (err) {
            console.error("Failed to parse JSON chunk:", chunk, err);
          }
        }
      }
    }

    // Handle any remaining data in the buffer
    if (buffer.trim()) {
      try {
        const parsed = JSON.parse(buffer);
        onChunk(parsed);
      } catch (err) {
        console.error("Failed to parse final JSON chunk:", buffer, err);
      }
    }
  } catch (error) {
    console.error("Failed to stream from Python backend:", error);
    throw error;
  }
}

