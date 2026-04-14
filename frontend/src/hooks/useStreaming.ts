import { useState, useRef, useCallback } from 'react';
import type { SSEChunk, SSEToolCall, SSEToolResult, ImageAttachment } from '@/types';
import { getToken } from '@/services/api';

export function useStreaming() {
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const startStream = useCallback(
    async (
      messages: { role: string; content: string; images?: ImageAttachment[] }[],
      conversationId: string | null,
      onChunk: (content: string) => void,
      onDone: (conversationId: string | null) => void,
      onToolCall?: (toolCall: SSEToolCall) => void,
      onToolResult?: (toolResult: SSEToolResult) => void,
    ) => {
      setIsStreaming(true);
      const controller = new AbortController();
      abortControllerRef.current = controller;

      try {
        const res = await fetch('/api/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${getToken()}`,
          },
          body: JSON.stringify({
            model: 'gpt-4o',
            messages,
            stream: true,
            conversation_id: conversationId,
          }),
          signal: controller.signal,
        });

        if (!res.ok) throw new Error(`Chat API error: ${res.status}`);

        const returnedConvId = res.headers.get('X-Conversation-Id');
        const reader = res.body!.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() ?? '';

          for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const data = line.slice(6).trim();
            if (data === '[DONE]') {
              onDone(returnedConvId);
              continue;
            }
            try {
              const parsed: SSEChunk = JSON.parse(data);
              const delta = parsed.choices[0]?.delta;
              if (!delta) continue;
              if (delta.content) onChunk(delta.content);
              if (delta.tool_call) onToolCall?.(delta.tool_call);
              if (delta.tool_result) onToolResult?.(delta.tool_result);
            } catch {
              // skip malformed
            }
          }
        }
      } catch (err) {
        if ((err as Error).name !== 'AbortError') {
          console.error('Streaming error:', err);
        }
        onDone(null);
      } finally {
        abortControllerRef.current = null;
        setIsStreaming(false);
      }
    },
    [],
  );

  const stopStream = useCallback(() => {
    abortControllerRef.current?.abort();
  }, []);

  return { startStream, stopStream, isStreaming };
}
