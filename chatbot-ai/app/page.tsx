'use client';

import { useChat } from "@/hooks/useChat";
import ChatContainer from "@/components/chat/ChatContainer";
import ChatInput from "@/components/chat/ChatInput";
import { ModeToggle } from "@/components/ui/darkmodeButton";

export default function Home() {
  const {
    messages,
    isLoading,
    isStreaming,
    isWebSearchActive,
    toggleWebSearch,
    sendMessage,
    messagesEndRef,
  } = useChat();

  const isChatActive = messages.length > 0;

  return (
    <>
      {isChatActive ? (
        <ChatContainer
          messages={messages}
          isLoading={isLoading}
          isStreaming={isStreaming}
          isWebSearchActive={isWebSearchActive}
          onToggleWebSearch={toggleWebSearch}
          sendMessage={sendMessage}
          messagesEndRef={messagesEndRef}
        />
      ) : (
        <div className="relative min-h-svh w-full bg-background text-foreground flex flex-col justify-center items-center px-4 overflow-hidden">
          <div className="absolute top-[50%] left-[50%] w-[30vw] h-[5vw] rounded-full bg-blue-400/70 blur-[120px] pointer-events-none" />
          <div className="absolute top-[50%] right-[50%] w-[30vw] h-[5vw] rounded-full bg-blue-700/70 blur-[120px] pointer-events-none" />

          <div className="fixed top-6 right-6 z-50">
            <ModeToggle />
          </div>

          <div className="text-center mb-8 w-full max-w-2xl z-10">
            <p className="text-muted-foreground mt-2 text-lg md:text-2xl font-medium">
              How can I help you today?
            </p>
          </div>

          <ChatInput
            onSend={sendMessage}
            isLoading={isLoading}
            isFloating={false}
            isWebSearchActive={isWebSearchActive}
            onToggleWebSearch={toggleWebSearch}
          />
        </div>
      )}
    </>
  );
}