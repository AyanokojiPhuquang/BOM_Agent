import { api } from './api';

export interface PromptItem {
  path: string;
  name: string;
  category: string;
  content: string;
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
