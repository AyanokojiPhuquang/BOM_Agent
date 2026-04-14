import type { Conversation, ImageAttachment } from '@/types';
import { APP_NAME } from '@/constants';
import { MenuIcon } from '@/components/icons';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';

interface ChatAreaProps {
  conversation: Conversation | null;
  isStreaming: boolean;
  streamingMessageId?: string;
  userName?: string;
  onSendMessage: (text: string, images: ImageAttachment[]) => void;
  onStopStream: () => void;
  onToggleSidebar: () => void;
}

export function ChatArea({
  conversation,
  isStreaming,
  streamingMessageId,
  userName,
  onSendMessage,
  onStopStream,
  onToggleSidebar,
}: ChatAreaProps) {
  return (
    <div className="flex-1 flex flex-col h-full bg-dark-bg">
      {/* Header */}
      <div className="flex items-center gap-3 px-4 py-3 border-b border-dark-border bg-dark-bg">
        <button
          onClick={onToggleSidebar}
          className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-dark-hover transition-colors"
        >
          <MenuIcon />
        </button>
        <h1 className="text-sm font-medium text-gray-300 truncate">
          {conversation?.title ?? APP_NAME}
        </h1>
      </div>

      {/* Messages */}
      <MessageList
        messages={conversation?.messages ?? []}
        isStreaming={isStreaming}
        streamingMessageId={streamingMessageId}
        userName={userName}
      />

      {/* Input */}
      <ChatInput
        onSend={(text, images) => onSendMessage(text, images)}
        disabled={isStreaming}
        onStop={onStopStream}
      />
    </div>
  );
}
