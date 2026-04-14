import { useState, useCallback, useEffect } from 'react';
import type { Conversation, Message, MessageType } from '@/types';
import * as convService from '@/services/conversations';

export function useConversations() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);

  // Load conversation list on mount
  useEffect(() => {
    convService.fetchConversations().then(list => {
      setConversations(list);
      if (list.length > 0) setActiveId(list[0].id);
    }).catch(err => console.error('Failed to load conversations', err));
  }, []);

  // Load full conversation (with messages) when activeId changes
  useEffect(() => {
    if (!activeId) return;
    const current = conversations.find(c => c.id === activeId);
    // Only fetch if we don't already have messages loaded
    if (current && current.messages.length > 0) return;

    convService.fetchConversation(activeId).then(full => {
      setConversations(prev =>
        prev.map(c => (c.id === full.id ? full : c))
      );
    }).catch(err => console.error('Failed to load conversation', err));
  }, [activeId]);

  const createConversation = useCallback(async () => {
    const conv = await convService.createConversation();
    setConversations(prev => [conv, ...prev]);
    setActiveId(conv.id);
    return conv.id;
  }, []);

  const addMessage = useCallback((convId: string, message: Message) => {
    setConversations(prev =>
      prev.map(c => {
        if (c.id !== convId) return c;
        const updated = { ...c, messages: [...c.messages, message], updatedAt: Date.now() };
        if (message.role === 'user' && c.messages.length === 0) {
          const text = message.content || 'Image shared';
          updated.title = text.length > 40 ? text.slice(0, 40) + '...' : text;
          // Update title on backend (fire and forget)
          convService.updateTitle(convId, updated.title).catch(err => console.error('Failed to update title', err));
        }
        return updated;
      })
    );
  }, []);

  const updateMessageContent = useCallback((convId: string, msgId: string, content: string) => {
    setConversations(prev =>
      prev.map(c => {
        if (c.id !== convId) return c;
        return {
          ...c,
          messages: c.messages.map(m => (m.id === msgId ? { ...m, content } : m)),
          updatedAt: Date.now(),
        };
      })
    );
  }, []);

  const updateMessageMeta = useCallback(
    (convId: string, msgId: string, meta: { type?: MessageType; toolName?: string }) => {
      setConversations(prev =>
        prev.map(c => {
          if (c.id !== convId) return c;
          return {
            ...c,
            messages: c.messages.map(m => (m.id === msgId ? { ...m, ...meta } : m)),
          };
        })
      );
    },
    [],
  );

  const deleteConversation = useCallback((convId: string) => {
    convService.deleteConversation(convId).catch(err => console.error('Failed to delete conversation', err));
    setConversations(prev => prev.filter(c => c.id !== convId));
    setActiveId(prev => (prev === convId ? null : prev));
  }, []);

  const activeConversation = conversations.find(c => c.id === activeId) ?? null;

  return {
    conversations,
    activeConversation,
    activeId,
    setActiveId,
    createConversation,
    addMessage,
    updateMessageContent,
    updateMessageMeta,
    deleteConversation,
  };
}
