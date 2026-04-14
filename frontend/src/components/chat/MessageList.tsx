import { useEffect, useRef } from 'react';
import type { Message } from '@/types';
import { APP_NAME } from '@/constants';
import { ChatBubbleIcon } from '@/components/icons';
import { MessageBubble } from './MessageBubble';

interface MessageListProps {
  messages: Message[];
  isStreaming: boolean;
  streamingMessageId?: string;
  userName?: string;
}

export function MessageList({ messages, isStreaming, streamingMessageId, userName }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isStreaming]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-accent/20 mb-4">
            <ChatBubbleIcon className="w-8 h-8 text-accent" />
          </div>
          <h2 className="text-xl font-semibold text-white mb-2">{APP_NAME}</h2>
          <p className="text-gray-400 max-w-sm">
            Start a conversation by typing a message below. You can also attach images!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      {messages.map(msg => (
        <MessageBubble
          key={msg.id}
          message={msg}
          isStreaming={isStreaming && msg.id === streamingMessageId}
          userName={userName}
        />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
