import React from 'react';
import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface ChatInputProps {
  input: string;
  isLoading: boolean;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function ChatInput({ input, isLoading, onInputChange, onSubmit }: ChatInputProps) {
  return (
    <form onSubmit={onSubmit} className="flex w-full gap-2">
      <Input
        value={input}
        onChange={onInputChange}
        placeholder="Ask a question..."
        className="flex-grow"
        disabled={isLoading}
      />
      <Button type="submit" disabled={isLoading || !input.trim()}>
        {isLoading ? "Thinking..." : <Send className="h-4 w-4" />}
      </Button>
    </form>
  );
} 