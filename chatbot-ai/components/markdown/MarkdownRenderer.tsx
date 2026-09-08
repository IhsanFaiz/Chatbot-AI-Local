"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import CodeBlock from "./CodeBlock";

interface MarkdownRendererProps {
  content: string;
  isStreaming?: boolean;
}

function MarkdownRendererComponent({ content, isStreaming = false }: MarkdownRendererProps) {
  const sanitizedText = content.replace(/\n{3,}/g, "\n\n").trim();

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        p({ children }) {
          return <p className="mb-2.5 last:mb-0 leading-relaxed">{children}</p>;
        },
        ul({ children }) {
          return <ul className="my-2 pl-5 list-disc space-y-1">{children}</ul>;
        },
        ol({ children }) {
          return <ol className="my-2 pl-5 list-decimal space-y-1">{children}</ol>;
        },
        li({ children }) {
          return <li className="leading-relaxed">{children}</li>;
        },
        h1({ children }) {
          return <h1 className="text-lg font-bold mt-3 mb-1.5">{children}</h1>;
        },
        h2({ children }) {
          return <h2 className="text-base font-bold mt-3 mb-1.5">{children}</h2>;
        },
        h3({ children }) {
          return <h3 className="text-base font-semibold mt-2.5 mb-1">{children}</h3>;
        },
        blockquote({ children }) {
          return <blockquote className="border-l-2 border-primary/50 pl-3 italic my-2 text-muted-foreground">{children}</blockquote>;
        },
        code(props) {
          const { children, className } = props;
          const match = /language-(\w+)/.exec(className || "");

          if (match) {
            // High-performance code block rendering during active streaming
            if (isStreaming) {
              return (
                <div className="relative my-4 overflow-hidden rounded-lg border border-border bg-zinc-900">
                  <div className="flex items-center justify-between px-4 py-2 bg-zinc-800 text-zinc-300 text-xs font-mono">
                    <span>{match[1]}</span>
                  </div>
                  <pre className="p-4 text-zinc-100 font-mono text-sm overflow-x-auto whitespace-pre">
                    <code>{String(children).replace(/\n$/, "")}</code>
                  </pre>
                </div>
              );
            }

            // Full interactive CodeBlock with Prism syntax highlighting after stream completes
            return (
              <CodeBlock
                language={match[1]}
                value={String(children).replace(/\n$/, "")}
              />
            );
          }

          return (
            <code className="bg-background/50 border border-border px-1.5 py-0.5 rounded text-xs font-mono">
              {children}
            </code>
          );
        },
      }}
    >
      {sanitizedText}
    </ReactMarkdown>
  );
}

export default React.memo(MarkdownRendererComponent);
