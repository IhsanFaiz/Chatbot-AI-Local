"use client";

import React from "react";
import ChatMessage from "./ChatMessage";
import { ChatMessageData } from "@/hooks/useChat";

interface ChatMessagesProps {
  messages: ChatMessageData[];
  isLoading: boolean;
  isStreaming: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
}

function ChatMessagesComponent({
  messages,
  isLoading,
  isStreaming,
  messagesEndRef,
}: ChatMessagesProps) {
  return (
    <div className="w-full overflow-y-auto pt-17 pb-40 flex flex-col gap-4">
      {messages.map((m, index) => {
        const isLastMessage = index === messages.length - 1;
        const messageStreaming = isLastMessage && isStreaming;
        const messageLoading = isLastMessage && isLoading;

        return (
          <ChatMessage
            key={index}
            sender={m.sender}
            text={m.text}
            isStreaming={messageStreaming}
            isLoading={messageLoading}
          />
        );
      })}
      <div ref={messagesEndRef} className="h-6 min-h-[24px] w-full" />
    </div>
  );
}

export default React.memo(ChatMessagesComponent);
