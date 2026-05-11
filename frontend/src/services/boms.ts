import { api } from './api';

export interface BomFileItem {
  filename: string;
  size: number;
  created_at: number;
  download_url: string;
}

export interface BomListResponse {
  total: number;
  items: BomFileItem[];
}

export async function listBoms(): Promise<BomListResponse> {
  return api<BomListResponse>('/api/boms/');
}

export async function deleteBom(filename: string): Promise<{ message: string }> {
  return api<{ message: string }>(`/api/boms/${encodeURIComponent(filename)}`, {
    method: 'DELETE',
  });
}
