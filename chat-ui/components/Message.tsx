import React from 'react';
import { Message as MessageType } from "@/types";

interface MessageProps {
  message: MessageType;
}

export function Message({ message }: MessageProps) {
  return (
    <div className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[80%] rounded-lg p-3 ${
        message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
      }`}>
        <p className="whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
} 