"use client";

import { useState, useRef, useEffect } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Message } from "@/components/Message";
import { ChatInput } from "@/components/ChatInput";
import { Message as MessageType } from "@/types";

export default function ChatInterface() {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    try {
      setIsLoading(true);
      setErrorMessage("");
      
      // Add user message
      const userMessage: MessageType = {
        id: Date.now().toString(),
        role: "user",
        content: input
      };
      
      setMessages(prev => [...prev, userMessage]);
      setInput("");
      
      // Send to API
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: [...messages, userMessage] })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `API error: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("Received response data:", data);
      
      // Add assistant message
      setMessages(prev => {
        console.log("Previous messages:", prev);
        const newMessages = [...prev, data];
        console.log("New messages array:", newMessages);
        return newMessages;
      });
    } catch (err) {
      console.error("Error submitting:", err);
      setErrorMessage(err instanceof Error ? err.message : "Failed to send message. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
      <Card className="w-full max-w-3xl h-[80vh] flex flex-col">
        <CardHeader className="border-b">
          <CardTitle className="text-center">Knowledge Assistant</CardTitle>
        </CardHeader>

        <CardContent className="flex-grow overflow-y-auto p-4 space-y-4">
          {messages.map((message) => {
            console.log("Rendering message:", message);
            return <Message key={message.id} message={message} />;
          })}
          {errorMessage && (
            <div className="flex justify-center">
              <div className="max-w-[80%] rounded-lg p-3 bg-red-100 text-red-800">
                <p>Error: {errorMessage}</p>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </CardContent>

        <CardFooter className="border-t p-4">
          <ChatInput
            input={input}
            isLoading={isLoading}
            onInputChange={handleInputChange}
            onSubmit={handleSubmit}
          />
        </CardFooter>
      </Card>
    </div>
  );
}

