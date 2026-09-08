"use client";

import React from "react";
import MarkdownRenderer from "@/components/markdown/MarkdownRenderer";
import TypingIndicator from "./TypingIndicator";

interface ChatMessageProps {
  sender: "user" | "bot";
  text: string;
  isStreaming?: boolean;
  isLoading?: boolean;
}

function ChatMessageComponent({
  sender,
  text,
  isStreaming = false,
  isLoading = false,
}: ChatMessageProps) {
  const isUser = sender === "user";

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`${
          isUser
            ? "max-w-[80%] px-4 py-3 rounded-2xl text-base bg-primary text-primary-foreground rounded-tr-none whitespace-pre-wrap break-words"
            : "w-full text-base text-foreground px-0 py-1"
        }`}
      >
        {isUser ? (
          <>{text}</>
        ) : (
          <>
            {isLoading && !text ? (
              <TypingIndicator />
            ) : (
              <MarkdownRenderer content={text} isStreaming={isStreaming} />
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default React.memo(ChatMessageComponent);
