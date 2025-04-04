// Environment variables
declare namespace NodeJS {
  interface ProcessEnv {
    NEXT_PUBLIC_FASTAPI_URL: string;
  }
}

// Message types that match the AI SDK expectations
export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
}; 