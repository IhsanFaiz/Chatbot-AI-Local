"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Send, Image, Mic } from "lucide-react";

interface ChatInputProps {
  onSend: (text: string) => void;
  isLoading: boolean;
  isFloating?: boolean;
}

function ChatInputComponent({ onSend, isLoading, isFloating = false }: ChatInputProps) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  // Auto-resize height based on input content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      const newHeight = Math.min(textareaRef.current.scrollHeight, 160);
      textareaRef.current.style.height = `${Math.max(56, newHeight)}px`;
    }
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = useCallback(
    (e?: React.FormEvent) => {
      if (e) e.preventDefault();
      if (!input.trim() || isLoading) return;

      const messageText = input;
      setInput("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "56px";
      }
      onSend(messageText);
    },
    [input, isLoading, onSend]
  );

  const formClasses = isFloating
    ? "fixed bottom-6 left-0 right-0 flex items-center justify-center bg-gradient-to-t from-background via-background/90 to-transparent pt-4 pb-2 z-20"
    : "relative w-full max-w-2xl flex items-end z-10";

  const containerClasses = isFloating
    ? "relative w-full max-w-3xl flex items-end z-10 px-4"
    : "relative w-full flex items-end z-10";

  const rightActionClasses = isFloating
    ? "absolute right-7 bottom-2.5 flex items-center gap-1"
    : "absolute right-3 bottom-2.5 flex items-center gap-1";

  return (
    <form onSubmit={handleSubmit} className={formClasses}>
      <div className={containerClasses}>
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          rows={1}
          className="w-full min-h-[56px] max-h-40 pl-6 pr-32 py-3.5 rounded-3xl text-base bg-muted/40 border border-muted-foreground/20 focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-offset-0 shadow-sm backdrop-blur-sm resize-none overflow-y-auto outline-none transition-all text-foreground placeholder:text-muted-foreground"
          placeholder="Ask Something..."
        />

        <div className={rightActionClasses}>
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="h-10 w-10 rounded-full text-muted-foreground hover:text-foreground hover:bg-muted"
          >
            <Image className="h-5 w-5" />
          </Button>

          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="h-10 w-10 rounded-full text-muted-foreground hover:text-foreground hover:bg-muted"
          >
            <Mic className="h-5 w-5" />
          </Button>

          <Button
            type="submit"
            size="icon"
            disabled={isLoading || !input.trim()}
            className="h-10 w-10 cursor-pointer rounded-full transition-transform active:scale-95 disabled:opacity-50"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </form>
  );
}

export default React.memo(ChatInputComponent);
