import { api } from './api';

export interface UserDetail {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
  is_active: boolean;
  created_at: number;
  updated_at: number;
}

interface UserListResponse {
  items: UserDetail[];
  total: number;
}

export interface CreateUserData {
  email: string;
  name: string;
  password: string;
  role: string;
}

export interface UpdateUserData {
  email?: string;
  name?: string;
  role?: string;
  is_active?: boolean;
  password?: string;
}

export async function listUsers(): Promise<UserListResponse> {
  return api<UserListResponse>('/api/users');
}

export async function createUser(data: CreateUserData): Promise<UserDetail> {
  return api<UserDetail>('/api/users', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateUser(id: string, data: UpdateUserData): Promise<UserDetail> {
  return api<UserDetail>(`/api/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteUser(id: string): Promise<void> {
  await api(`/api/users/${id}`, { method: 'DELETE' });
}
