import type { Message } from '@/types';
import { Avatar } from '@/components/common/Avatar';
import { ImageLightbox } from '@/components/common/ImageLightbox';
import { cn } from '@/utils/cn';
import { AI_NAME } from '@/constants';
import { ToolIcon } from '@/components/icons';
import { MarkdownRenderer } from './MarkdownRenderer';
import { StreamingIndicator } from './StreamingIndicator';

interface MessageBubbleProps {
  message: Message;
  isStreaming?: boolean;
  userName?: string;
}

export function MessageBubble({ message, isStreaming = false, userName = 'You' }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const isToolCall = message.type === 'tool_call';

  if (isToolCall) {
    return (
      <div className="flex gap-3 px-4 py-2 border-l-2 border-accent/40 bg-dark-surface/30">
        <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-accent/20">
          <ToolIcon className="text-accent" />
        </div>
        <div className="flex-1 min-w-0">
          {message.toolName && (
            <span className="inline-block px-2 py-0.5 text-xs font-medium bg-accent/20 text-accent rounded-full mb-1">
              {message.toolName}
            </span>
          )}
          {message.content ? (
            <p className="text-sm text-gray-400 mt-1">{message.content}</p>
          ) : (
            isStreaming && <StreamingIndicator isThinking />
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={cn('flex gap-3 px-4 py-4', isUser ? 'bg-transparent' : 'bg-dark-surface/50')}>
      <Avatar name={userName} isBot={!isUser} />
      <div className="flex-1 min-w-0">
        <div className="text-sm font-semibold text-gray-300 mb-1">
          {isUser ? userName : AI_NAME}
        </div>

        {/* Images */}
        {message.images && message.images.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-2">
            {message.images.map(img => (
              <ImageLightbox
                key={img.id}
                src={img.dataUrl}
                alt={img.name}
                className="max-h-48 rounded-lg border border-dark-border object-contain"
              />
            ))}
          </div>
        )}

        {/* Content */}
        <div className="text-gray-200 overflow-hidden break-words">
          {isUser ? (
            <p className="whitespace-pre-wrap break-words leading-7">{message.content}</p>
          ) : (
            <>
              {isStreaming && !message.content ? (
                <StreamingIndicator isThinking />
              ) : (
                <>
                  <MarkdownRenderer content={message.content} />
                  {isStreaming && <StreamingIndicator />}
                </>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
