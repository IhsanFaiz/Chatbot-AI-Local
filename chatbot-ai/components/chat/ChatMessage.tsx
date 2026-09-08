"use client";

import React, { useState } from "react";
import MarkdownRenderer from "@/components/markdown/MarkdownRenderer";
import TypingIndicator from "./TypingIndicator";
import { Globe, ExternalLink, ChevronDown, ChevronUp, AlertCircle, CheckCircle2 } from "lucide-react";

export interface SourceItem {
  title: string;
  url: string;
}

interface ChatMessageProps {
  sender: "user" | "bot";
  text: string;
  status?: string;
  statusText?: string;
  sources?: SourceItem[];
  isStreaming?: boolean;
  isLoading?: boolean;
}

function ChatMessageComponent({
  sender,
  text,
  status,
  statusText,
  sources = [],
  isStreaming = false,
  isLoading = false,
}: ChatMessageProps) {
  const isUser = sender === "user";
  const [showSources, setShowSources] = useState(false);

  const hasSources = sources && sources.length > 0;
  const isWebStepActive =
    (status === "searching" ||
      status === "reading" ||
      status === "processing" ||
      status === "generating") &&
    isStreaming;
  const isOffline = status === "offline";

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`${
          isUser
            ? "max-w-[80%] px-4 py-3 rounded-2xl text-base bg-primary text-primary-foreground rounded-tr-none whitespace-pre-wrap break-words"
            : "w-full text-base text-foreground px-0 py-1 flex flex-col gap-3"
        }`}
      >
        {isUser ? (
          <>{text}</>
        ) : (
          <>
            {/* Live Web Search / Process Status Indicator */}
            {isWebStepActive && statusText && (
              <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-medium bg-muted/70 text-muted-foreground border border-border w-fit animate-pulse">
                <span className="inline-block w-2 h-2 rounded-full bg-blue-500 animate-ping" />
                <span>{statusText}</span>
              </div>
            )}

            {/* Offline Alert Indicator */}
            {isOffline && (
              <div className="flex items-start gap-2.5 p-3.5 rounded-xl text-xs sm:text-sm bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 max-w-xl">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <div className="flex flex-col gap-0.5">
                  <span className="font-semibold">Web Search Offline</span>
                  <span className="text-muted-foreground text-xs">
                    Please connect to the internet to retrieve real-time web results.
                  </span>
                </div>
              </div>
            )}

            {/* Completed Web Search Sources Accordion */}
            {hasSources && !isWebStepActive && (
              <div className="flex flex-col gap-2 max-w-2xl">
                <button
                  type="button"
                  onClick={() => setShowSources((prev) => !prev)}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-muted/40 hover:bg-muted/80 text-muted-foreground transition-all w-fit cursor-pointer border border-border/50"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                  <span>✓ Information retrieved from web ({sources.length} sources)</span>
                  {showSources ? (
                    <ChevronUp className="w-3.5 h-3.5 ml-1 opacity-70" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5 ml-1 opacity-70" />
                  )}
                </button>

                {showSources && (
                  <div className="flex flex-wrap gap-2 p-3 rounded-xl bg-card border border-border/70 text-xs">
                    {sources.map((src, idx) => (
                      <a
                        key={idx}
                        href={src.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-muted hover:bg-muted/80 text-foreground transition-colors max-w-xs truncate"
                        title={src.title}
                      >
                        <Globe className="w-3 h-3 text-muted-foreground flex-shrink-0" />
                        <span className="truncate">{src.title || src.url}</span>
                        <ExternalLink className="w-2.5 h-2.5 text-muted-foreground flex-shrink-0" />
                      </a>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Bot Message Body or Typing Indicator */}
            {isLoading && !text && !statusText ? (
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
