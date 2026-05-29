import { api } from './api';

export interface UserInstruction {
  id: string;
  content: string;
}

export interface UserInstructionsResponse {
  instructions: UserInstruction[];
  is_processing: boolean;
}

export async function listInstructions(): Promise<UserInstructionsResponse> {
  return api<UserInstructionsResponse>('/api/prompts/instructions');
}

export async function addInstruction(content: string): Promise<{ instruction: UserInstruction; message: string }> {
  return api<{ instruction: UserInstruction; message: string }>('/api/prompts/instructions', {
    method: 'POST',
    body: JSON.stringify({ content }),
  });
}

export async function deleteInstruction(id: string): Promise<{ message: string }> {
  return api<{ message: string }>(`/api/prompts/instructions/${id}`, { method: 'DELETE' });
}

export async function resetPrompt(): Promise<{ message: string }> {
  return api<{ message: string }>('/api/prompts/reset', { method: 'POST' });
}
