import { useState, useCallback } from 'react';
import { useConversations } from '@/hooks/useConversations';
import { useStreaming } from '@/hooks/useStreaming';
import { useAuth } from '@/hooks/useAuth';
import { Sidebar } from './Sidebar';
import { ChatArea } from './ChatArea';
import { generateId } from '@/utils/id';
import { useNavigate } from 'react-router-dom';
import type { ImageAttachment, SSEToolCall } from '@/types';

export function ChatLayout() {
  const {
    conversations,
    activeConversation,
    activeId,
    setActiveId,
    createConversation,
    addMessage,
    updateMessageContent,
    updateMessageMeta,
    deleteConversation,
  } = useConversations();

  const { startStream, stopStream, isStreaming } = useStreaming();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [streamingMsgId, setStreamingMsgId] = useState<string | null>(null);

  const handleSendMessage = useCallback(
    async (text: string, images: ImageAttachment[]) => {
      let convId = activeId;
      if (!convId) {
        convId = await createConversation();
      }

      const userMsg = {
        id: generateId(),
        role: 'user' as const,
        content: text,
        images: images.length > 0 ? images : undefined,
        createdAt: Date.now(),
      };
      addMessage(convId, userMsg);

      let currentMsgId = generateId();
      addMessage(convId, {
        id: currentMsgId,
        role: 'assistant' as const,
        content: '',
        createdAt: Date.now(),
      });
      setStreamingMsgId(currentMsgId);

      // Build messages array for the API
      const conv = conversations.find(c => c.id === convId);
      const existingMessages = conv
        ? conv.messages.map(m => ({ role: m.role, content: m.content }))
        : [];
      const apiMessages = [
        ...existingMessages,
        {
          role: 'user',
          content: text,
          ...(images.length > 0 ? { images } : {}),
        },
      ];

      let accumulated = '';

      const handleToolCall = (toolCall: SSEToolCall) => {
        // Finalize current message as a tool_call turn
        updateMessageMeta(convId!, currentMsgId, { type: 'tool_call', toolName: toolCall.name });

        // Create a new assistant message for the next segment
        const newMsgId = generateId();
        addMessage(convId!, {
          id: newMsgId,
          role: 'assistant' as const,
          content: '',
          createdAt: Date.now(),
        });
        currentMsgId = newMsgId;
        accumulated = '';
        setStreamingMsgId(newMsgId);
      };

      const handleToolResult = () => {
        // No-op — message splitting is handled by handleToolCall
      };

      const handleChunk = (chunk: string) => {
        accumulated += chunk;
        updateMessageContent(convId!, currentMsgId, accumulated);
      };

      startStream(
        apiMessages,
        convId,
        handleChunk,
        () => {
          setStreamingMsgId(null);
        },
        handleToolCall,
        handleToolResult,
      );
    },
    [activeId, conversations, createConversation, addMessage, updateMessageContent, updateMessageMeta, startStream],
  );

  const handleLogout = useCallback(() => {
    logout();
    navigate('/login');
  }, [logout, navigate]);

  return (
    <div className="flex h-screen bg-dark-bg text-white overflow-hidden">
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        isOpen={sidebarOpen}
        userName={user?.name}
        userRole={user?.role}
        onSelectConversation={setActiveId}
        onNewChat={() => { createConversation(); }}
        onDeleteConversation={deleteConversation}
        onLogout={handleLogout}
        onClose={() => setSidebarOpen(false)}
      />
      <ChatArea
        conversation={activeConversation}
        isStreaming={isStreaming}
        streamingMessageId={streamingMsgId ?? undefined}
        userName={user?.name}
        onSendMessage={handleSendMessage}
        onStopStream={stopStream}
        onToggleSidebar={() => setSidebarOpen(prev => !prev)}
      />
    </div>
  );
}
