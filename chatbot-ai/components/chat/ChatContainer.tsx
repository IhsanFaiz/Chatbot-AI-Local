"use client";

import React from "react";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";
import { ChatMessageData } from "@/hooks/useChat";

interface ChatContainerProps {
  messages: ChatMessageData[];
  isLoading: boolean;
  isStreaming: boolean;
  sendMessage: (text: string) => void;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
}

function ChatContainerComponent({
  messages,
  isLoading,
  isStreaming,
  sendMessage,
  messagesEndRef,
}: ChatContainerProps) {
  return (
    <div className="max-w-3xl h-full flex flex-col justify-between mx-auto w-full">
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
        isStreaming={isStreaming}
        messagesEndRef={messagesEndRef}
      />
      <ChatInput
        onSend={sendMessage}
        isLoading={isLoading}
        isFloating={true}
      />
    </div>
  );
}

export default React.memo(ChatContainerComponent);
