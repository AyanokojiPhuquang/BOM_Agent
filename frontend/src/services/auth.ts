import type { User } from '@/types';
import { api, setToken, clearToken, getToken } from './api';

interface LoginResponse {
  user: User;
  token: string;
}

export async function login(email: string, password: string): Promise<User> {
  const data = await api<LoginResponse>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  setToken(data.token);
  return data.user;
}

export async function logout(): Promise<void> {
  try {
    await api('/api/auth/logout', { method: 'POST' });
  } finally {
    clearToken();
  }
}

export async function getUser(): Promise<User | null> {
  if (!getToken()) return null;
  try {
    return await api<User>('/api/auth/me');
  } catch {
    clearToken();
    return null;
  }
}
