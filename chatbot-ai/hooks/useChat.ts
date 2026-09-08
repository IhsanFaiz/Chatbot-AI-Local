"use client";

import { useState, useRef, useCallback } from "react";
import { extractBotText } from "@/utils/streamParser";

export interface SourceItem {
  title: string;
  url: string;
}

export interface ChatMessageData {
  sender: "user" | "bot";
  text: string;
  status?: string;
  statusText?: string;
  sources?: SourceItem[];
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isWebSearchActive, setIsWebSearchActive] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll helper
  const scrollToBottom = useCallback((isImmediate = false) => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({
        behavior: isImmediate ? "auto" : "smooth",
      });
    }
  }, []);

  const toggleWebSearch = useCallback(() => {
    setIsWebSearchActive((prev) => !prev);
  }, []);

  const sendMessage = useCallback(
    async (text: string, forceWebSearch?: boolean) => {
      if (!text.trim() || isLoading) return;

      setIsLoading(true);
      setIsStreaming(false);

      // Append user message & bot placeholder
      setMessages((prev) => [
        ...prev,
        { sender: "user", text },
        { sender: "bot", text: "", status: "", statusText: "" },
      ]);

      // Immediate scroll when sending
      requestAnimationFrame(() => scrollToBottom(true));

      try {
        const useWeb = forceWebSearch !== undefined ? forceWebSearch : isWebSearchActive;
        const response = await fetch("http://127.0.0.1:5001/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json, text/plain, */*",
          },
          body: JSON.stringify({
            message: text,
            web_search: useWeb,
          }),
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
        let currentStatus = "";
        let currentStatusText = "";
        let currentSources: SourceItem[] = [];
        let pendingBatchUpdate = false;
        let lastScrollTime = 0;

        const updateStatus = (status: string, statusText: string, sources?: SourceItem[]) => {
          currentStatus = status;
          currentStatusText = statusText;
          if (sources && sources.length > 0) {
            currentSources = sources;
          }

          setMessages((prev) => {
            if (prev.length === 0) return prev;
            const copy = [...prev];
            const lastIdx = copy.length - 1;
            copy[lastIdx] = {
              ...copy[lastIdx],
              status: currentStatus,
              statusText: currentStatusText,
              sources: currentSources,
            };
            return copy;
          });
          scrollToBottom(false);
        };

        // Batch state updates per 40ms frame
        const flushUpdate = (final = false) => {
          const currentText = botTextBuffer;
          setMessages((prev) => {
            if (prev.length === 0) return prev;
            const copy = [...prev];
            const lastIdx = copy.length - 1;
            copy[lastIdx] = {
              sender: "bot",
              text: currentText,
              status:
                final && currentSources.length > 0
                  ? "done_search"
                  : currentStatus,
              statusText:
                final && currentSources.length > 0
                  ? "✓ Information retrieved from web"
                  : currentStatusText,
              sources: currentSources,
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

        const handleParsedChunk = (data: any, rawLine: string) => {
          if (data && typeof data === "object") {
            if (data.status) {
              updateStatus(data.status, data.status_text || "", data.sources);
              return;
            }

            const textChunk = data.text ?? data.response ?? data.message;
            if (textChunk !== undefined && textChunk !== null) {
              botTextBuffer += String(textChunk);
            } else {
              const extracted = extractBotText(rawLine);
              if (extracted) botTextBuffer += extracted;
            }
          } else {
            const extracted = extractBotText(rawLine);
            if (extracted) botTextBuffer += extracted;
          }
        };

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          sseBuffer += chunk;

          const lines = sseBuffer.split("\n");
          sseBuffer = lines.pop() ?? "";

          for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed) continue;

            if (trimmed.startsWith("data:")) {
              const jsonString = trimmed.replace(/^data:\s*/, "").trim();
              if (!jsonString || jsonString === "[DONE]") continue;

              try {
                const data = JSON.parse(jsonString);
                handleParsedChunk(data, jsonString);
              } catch {
                const extracted = extractBotText(jsonString);
                if (extracted) botTextBuffer += extracted;
              }
            } else {
              const extracted = extractBotText(trimmed);
              if (extracted) botTextBuffer += extracted;
            }
          }

          scheduleBatchUpdate();
        }

        // Flush any remaining content in sseBuffer
        if (sseBuffer.trim()) {
          const trimmed = sseBuffer.trim();
          if (trimmed.startsWith("data:")) {
            const jsonString = trimmed.replace(/^data:\s*/, "").trim();
            if (jsonString && jsonString !== "[DONE]") {
              try {
                const data = JSON.parse(jsonString);
                handleParsedChunk(data, jsonString);
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
          copy[copy.length - 1] = {
            sender: "bot",
            text: "Failed to connect to API server. Please ensure the backend is running.",
          };
          return copy;
        });
      } finally {
        setIsStreaming(false);
        setIsLoading(false);
        requestAnimationFrame(() => scrollToBottom(false));
      }
    },
    [isLoading, isWebSearchActive, scrollToBottom]
  );

  return {
    messages,
    isLoading,
    isStreaming,
    isWebSearchActive,
    toggleWebSearch,
    sendMessage,
    messagesEndRef,
  };
}
