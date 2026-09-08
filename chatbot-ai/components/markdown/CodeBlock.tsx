"use client";

import React, { useState } from "react";
import { Copy, Check } from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

interface CodeBlockProps {
  language: string;
  value: string;
}

function CodeBlockComponent({ language, value }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copyCode = async () => {
    await navigator.clipboard.writeText(value);
    setCopied(true);
    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  return (
    <div className="relative my-4 overflow-hidden rounded-lg border">
      <div className="flex items-center justify-between px-4 py-2 bg-zinc-800 text-zinc-300 text-sm">
        <span>{language}</span>

        <button
          onClick={copyCode}
          className="flex items-center gap-1 hover:text-white"
        >
          {copied ? (
            <>
              <Check size={16} />
              Copied
            </>
          ) : (
            <>
              <Copy size={16} />
              Copy
            </>
          )}
        </button>
      </div>

      <SyntaxHighlighter
        language={language}
        style={oneDark}
        customStyle={{
          margin: 0,
          borderRadius: 0,
        }}
      >
        {value}
      </SyntaxHighlighter>
    </div>
  );
}

export default React.memo(CodeBlockComponent);
