import type { Conversation, Message } from '@/types';
import { api } from './api';

interface ConversationSummary {
  id: string;
  title: string;
  createdAt: number;
  updatedAt: number;
}

interface ConversationDetail {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
}

interface ConversationListResponse {
  items: ConversationSummary[];
}

export async function fetchConversations(): Promise<Conversation[]> {
  const data = await api<ConversationListResponse>('/api/conversations');
  return data.items.map(item => ({
    ...item,
    messages: [],
  }));
}

export async function fetchConversation(id: string): Promise<Conversation> {
  return api<ConversationDetail>(`/api/conversations/${id}`);
}

export async function createConversation(): Promise<Conversation> {
  return api<ConversationDetail>('/api/conversations', { method: 'POST' });
}

export async function deleteConversation(id: string): Promise<void> {
  await api(`/api/conversations/${id}`, { method: 'DELETE' });
}

export async function updateTitle(id: string, title: string): Promise<Conversation> {
  return api<ConversationDetail>(`/api/conversations/${id}/title`, {
    method: 'PUT',
    body: JSON.stringify({ title }),
  });
}
