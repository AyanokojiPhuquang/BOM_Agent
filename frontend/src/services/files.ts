import { api, apiUpload } from './api';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface FolderItem {
  id: string;
  name: string;
  parent_id: string | null;
  created_by: string;
  created_at: number;
  updated_at: number;
}

export interface FileItem {
  id: string;
  name: string;
  original_name: string;
  mime_type: string;
  size: number;
  folder_id: string | null;
  status: string;
  uploaded_by: string;
  tags: string[];
  metadata: Record<string, string>;
  created_at: number;
  updated_at: number;
}

export interface FileListResponse {
  items: FileItem[];
  folders: FolderItem[];
  total: number;
  breadcrumb: FolderItem[];
}

export interface UpdateFileData {
  name?: string;
  folder_id?: string | null;
  tags?: string[];
  metadata?: Record<string, string>;
}

// ---------------------------------------------------------------------------
// File operations
// ---------------------------------------------------------------------------

export async function listFiles(
  folderId?: string | null,
  search?: string,
  limit = 100,
  offset = 0,
): Promise<FileListResponse> {
  const params = new URLSearchParams();
  if (folderId) params.set('folder_id', folderId);
  if (search) params.set('search', search);
  params.set('limit', String(limit));
  params.set('offset', String(offset));
  return api<FileListResponse>(`/api/file-manager/files?${params}`);
}

export async function getFile(id: string): Promise<FileItem> {
  return api<FileItem>(`/api/file-manager/files/${id}`);
}

export async function uploadFile(
  file: File,
  folderId?: string | null,
  tags?: string[],
  metadata?: Record<string, string>,
): Promise<FileItem> {
  const formData = new FormData();
  formData.append('file', file);
  if (folderId) formData.append('folder_id', folderId);
  if (tags?.length) formData.append('tags', JSON.stringify(tags));
  if (metadata && Object.keys(metadata).length) {
    formData.append('metadata', JSON.stringify(metadata));
  }
  return apiUpload<FileItem>('/api/file-manager/files/upload', formData);
}

export async function updateFile(id: string, data: UpdateFileData): Promise<FileItem> {
  return api<FileItem>(`/api/file-manager/files/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteFile(id: string): Promise<void> {
  return api(`/api/file-manager/files/${id}`, { method: 'DELETE' });
}

// ---------------------------------------------------------------------------
// Folder operations
// ---------------------------------------------------------------------------

export async function createFolder(
  name: string,
  parentId?: string | null,
): Promise<FolderItem> {
  return api<FolderItem>('/api/file-manager/folders', {
    method: 'POST',
    body: JSON.stringify({ name, parent_id: parentId ?? null }),
  });
}

export async function updateFolder(id: string, name: string): Promise<FolderItem> {
  return api<FolderItem>(`/api/file-manager/folders/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ name }),
  });
}

export async function deleteFolder(id: string): Promise<void> {
  return api(`/api/file-manager/folders/${id}`, { method: 'DELETE' });
}

// ---------------------------------------------------------------------------
// Preview helper
// ---------------------------------------------------------------------------

export function getFileDownloadUrl(id: string): string {
  return `/api/file-manager/files/${id}/download`;
}
