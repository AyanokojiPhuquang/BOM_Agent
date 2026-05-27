import { api } from './api';

export interface PromptItem {
  path: string;
  name: string;
  category: string;
  content: string;
  has_original: boolean;
  is_modified: boolean;
}

export interface PromptListResponse {
  prompts: PromptItem[];
}

export async function listPrompts(): Promise<PromptListResponse> {
  return api<PromptListResponse>('/api/prompts/');
}

export async function updatePrompt(path: string, content: string): Promise<PromptItem> {
  return api<PromptItem>(`/api/prompts/${path}`, {
    method: 'PUT',
    body: JSON.stringify({ content }),
  });
}

export async function revertPrompt(path: string): Promise<PromptItem> {
  return api<PromptItem>(`/api/prompts/${path}/revert`, { method: 'POST' });
}
