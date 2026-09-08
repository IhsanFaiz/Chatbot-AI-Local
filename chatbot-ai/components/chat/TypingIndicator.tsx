"use client";

import React from "react";
import { LoaderPinwheelIcon } from "lucide-react";

function TypingIndicatorComponent() {
  return (
    <div className="flex items-center gap-2 py-1 text-muted-foreground">
      <LoaderPinwheelIcon className="size-5 animate-spin text-primary" />
    </div>
  );
}

export default React.memo(TypingIndicatorComponent);
