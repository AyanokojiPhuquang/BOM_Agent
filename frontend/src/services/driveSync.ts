import { api } from './api';

export interface AuthStatus {
  connected: boolean;
  google_email: string | null;
}

export interface BatchJob {
  id: string;
  user_id: string;
  folder_id: string;
  status: string;
  total_files: number;
  completed_count: number;
  failed_count: number;
  skipped_count: number;
  products_extracted: number;
  started_at: string;
  completed_at: string | null;
  created_at: string;
}

export interface BatchTask {
  id: string;
  drive_file_id: string;
  file_name: string;
  file_size: number;
  status: string;
  attempt_count: number;
  error_message: string | null;
  products_extracted: number;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface BatchJobDetail {
  job: BatchJob;
  tasks: BatchTask[];
}

export interface SyncStartResponse {
  job_id: string;
  status: string;
  total_files: number;
  skipped_count: number;
  message: string;
}

export interface TaskUpdateEvent {
  type: 'task_update';
  batch_job_id: string;
  task_id: string;
  status: string;
  file_name: string;
  progress: { completed: number; failed: number; total: number };
}

export interface BatchCompleteEvent {
  type: 'batch_complete';
  batch_job_id: string;
  summary: { total_files: number; completed: number; failed: number; skipped: number; products_extracted: number };
}

export type WSEvent = TaskUpdateEvent | BatchCompleteEvent;

export async function getAuthUrl(): Promise<{ url: string }> {
  return api<{ url: string }>('/api/drive/auth/url');
}

export async function getAuthStatus(): Promise<AuthStatus> {
  return api<AuthStatus>('/api/drive/auth/status');
}

export async function disconnectDrive(): Promise<{ message: string }> {
  return api<{ message: string }>('/api/drive/auth/disconnect', { method: 'POST' });
}

export async function startSync(folderId: string): Promise<SyncStartResponse> {
  return api<SyncStartResponse>('/api/drive/sync/start', {
    method: 'POST',
    body: JSON.stringify({ folder_id: folderId }),
  });
}

export async function getJobs(): Promise<BatchJob[]> {
  return api<BatchJob[]>('/api/drive/sync/jobs');
}

export async function getJobDetail(jobId: string): Promise<BatchJobDetail> {
  return api<BatchJobDetail>(`/api/drive/sync/jobs/${jobId}`);
}

export async function retryFailed(jobId: string): Promise<{ retried_count: number; message: string }> {
  return api<{ retried_count: number; message: string }>(`/api/drive/sync/jobs/${jobId}/retry-failed`, { method: 'POST' });
}


export interface DriveFolder {
  id: string;
  name: string;
}

export async function listDriveFolders(parentId: string = 'root'): Promise<{ folders: DriveFolder[]; parent_id: string }> {
  return api<{ folders: DriveFolder[]; parent_id: string }>(`/api/drive/folders?parent_id=${encodeURIComponent(parentId)}`);
}
