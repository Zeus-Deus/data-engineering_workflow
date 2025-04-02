/**
 * Utility functions for integrating with the Python RAG backend
 */

// Function to send a query to the Python backend
export async function queryRagSystem(query: string) {
  try {
    const response = await fetch("http://your-python-backend-url/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    })

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Failed to query RAG system:", error)
    throw error
  }
}

// Function to stream responses from the Python backend
// This can be implemented if your Python backend supports streaming
export async function streamFromPythonBackend(query: string, onChunk: (chunk: string) => void) {
  try {
    const response = await fetch("http://your-python-backend-url/stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    })

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) throw new Error("Response body is null")

    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      onChunk(chunk)
    }
  } catch (error) {
    console.error("Failed to stream from Python backend:", error)
    throw error
  }
}

