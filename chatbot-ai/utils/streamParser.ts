export const extractBotText = (raw: string): string => {
  if (!raw) return "";

  const trimmed = raw.trim();

  // 1. Try parsing complete JSON
  try {
    const parsed = JSON.parse(trimmed);
    if (typeof parsed === "object" && parsed !== null) {
      const val = parsed.text ?? parsed.response ?? parsed.message;
      if (typeof val === "string") return val;
      if (typeof val === "object" && val !== null) return extractBotText(JSON.stringify(val));
    } else if (typeof parsed === "string") {
      return extractBotText(parsed);
    }
  } catch {
    // Incomplete JSON or non-JSON string
  }

  // 2. Extract value from "text": "...", "response": "...", or "message": "..."
  const textMatch = /"(?:text|response|message)"\s*:\s*"([\s\S]*)/.exec(trimmed);
  if (textMatch) {
    let content = textMatch[1];
    content = content.replace(/"\s*}\s*$/, "").replace(/"\s*$/, "");
    content = content.replace(/\\"/g, '"').replace(/\\n/g, '\n').replace(/\\\\/g, '\\');
    return content;
  }

  // 3. Fallback: clean leading prefixes
  return trimmed.replace(/^\s*(?:response|text|message):\s*/i, "");
};
