interface StreamingIndicatorProps {
  /** True when no content has arrived yet (agent is thinking) */
  isThinking?: boolean;
}

export function StreamingIndicator({ isThinking = false }: StreamingIndicatorProps) {
  if (isThinking) {
    return (
      <div className="flex items-center gap-3 py-2">
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-accent animate-thinking-dot" style={{ animationDelay: '0s' }} />
          <span className="w-2 h-2 rounded-full bg-accent animate-thinking-dot" style={{ animationDelay: '0.15s' }} />
          <span className="w-2 h-2 rounded-full bg-accent animate-thinking-dot" style={{ animationDelay: '0.3s' }} />
        </div>
        <span className="text-sm text-gray-400 animate-fade-in">Thinking...</span>
      </div>
    );
  }

  return (
    <span className="inline-block w-2 h-5 ml-0.5 bg-accent/70 rounded-sm animate-cursor-blink" />
  );
}
