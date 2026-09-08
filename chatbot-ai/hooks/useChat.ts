"use client";

import { useState, useRef, useCallback } from "react";
import { extractBotText } from "@/utils/streamParser";

export interface ChatMessageData {
  sender: "user" | "bot";
  text: string;
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll helper
  const scrollToBottom = useCallback((isImmediate = false) => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({
        behavior: isImmediate ? "auto" : "smooth",
      });
    }
  }, []);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || isLoading) return;

      setIsLoading(true);
      setIsStreaming(false);

      // Append user message & bot placeholder
      setMessages((prev) => [
        ...prev,
        { sender: "user", text },
        { sender: "bot", text: "" },
      ]);

      // Immediate scroll when sending
      requestAnimationFrame(() => scrollToBottom(true));

      try {
        const response = await fetch("http://127.0.0.1:5001/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json, text/plain, */*",
          },
          body: JSON.stringify({ message: text }),
        });

        if (!response.ok) {
          throw new Error(`Server returned status ${response.status}`);
        }

        if (!response.body) {
          throw new Error("Response body is not readable");
        }

        setIsStreaming(true);
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let sseBuffer = "";
        let botTextBuffer = "";
        let pendingBatchUpdate = false;
        let lastScrollTime = 0;

        // Batch state updates per 40ms frame
        const flushUpdate = (final = false) => {
          const currentText = botTextBuffer;
          setMessages((prev) => {
            if (prev.length === 0) return prev;
            const copy = [...prev];
            copy[copy.length - 1] = {
              sender: "bot",
              text: currentText,
            };
            return copy;
          });

          // Throttle scroll execution during streaming
          const now = Date.now();
          if (final || now - lastScrollTime > 100) {
            lastScrollTime = now;
            scrollToBottom(true);
          }
        };

        const scheduleBatchUpdate = () => {
          if (!pendingBatchUpdate) {
            pendingBatchUpdate = true;
            setTimeout(() => {
              pendingBatchUpdate = false;
              flushUpdate(false);
            }, 40);
          }
        };

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          sseBuffer += chunk;

          const lines = sseBuffer.split("\n");
          // Retain last incomplete line in sseBuffer
          sseBuffer = lines.pop() ?? "";

          for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed) continue;

            if (trimmed.startsWith("data:")) {
              const jsonString = trimmed.replace(/^data:\s*/, "").trim();
              if (!jsonString || jsonString === "[DONE]") continue;

              try {
                const data = JSON.parse(jsonString);
                const textChunk = data.text ?? data.response ?? data.message;
                if (textChunk !== undefined && textChunk !== null) {
                  botTextBuffer += String(textChunk);
                } else {
                  const extracted = extractBotText(jsonString);
                  if (extracted) botTextBuffer += extracted;
                }
              } catch {
                const extracted = extractBotText(jsonString);
                if (extracted) botTextBuffer += extracted;
              }
            } else {
              // Raw chunk not prefixed with data:
              const extracted = extractBotText(trimmed);
              if (extracted) botTextBuffer += extracted;
            }
          }

          scheduleBatchUpdate();
        }

        // Flush any remaining content in sseBuffer after stream completion
        if (sseBuffer.trim()) {
          const trimmed = sseBuffer.trim();
          if (trimmed.startsWith("data:")) {
            const jsonString = trimmed.replace(/^data:\s*/, "").trim();
            if (jsonString && jsonString !== "[DONE]") {
              try {
                const data = JSON.parse(jsonString);
                const textChunk = data.text ?? data.response ?? data.message;
                if (textChunk !== undefined && textChunk !== null) {
                  botTextBuffer += String(textChunk);
                } else {
                  const extracted = extractBotText(jsonString);
                  if (extracted) botTextBuffer += extracted;
                }
              } catch {
                const extracted = extractBotText(jsonString);
                if (extracted) botTextBuffer += extracted;
              }
            }
          } else {
            const extracted = extractBotText(trimmed);
            if (extracted) botTextBuffer += extracted;
          }
        }

        flushUpdate(true);
      } catch (error) {
        setMessages((prev) => {
          if (prev.length === 0) return prev;
          const copy = [...prev];
          copy[copy.length - 1] = { sender: "bot", text: "Failed hit API" };
          return copy;
        });
      } finally {
        setIsStreaming(false);
        setIsLoading(false);
        requestAnimationFrame(() => scrollToBottom(false));
      }
    },
    [isLoading, scrollToBottom]
  );

  return {
    messages,
    isLoading,
    isStreaming,
    sendMessage,
    messagesEndRef,
  };
}
