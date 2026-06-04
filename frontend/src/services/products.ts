import { api, apiUpload } from './api';

export interface ProductItem {
  id: string;
  code: string;
  name: string;
  brand: string;
  description: string;
  data_rate: string;
  fiber_type: string;
  wavelength: string;
  max_distance: string;
  connector: string;
  main_device: string;
  category: string;
  datasheet_path: string | null;
  pdf_url: string | null;
  raw_specs: string;
  status: number;
  created_at: string;
  updated_at: string;
}

export interface ProductListResponse {
  total: number;
  products: ProductItem[];
}

export interface ProductUpdateData {
  code?: string;
  name?: string;
  brand?: string;
  description?: string;
  data_rate?: string;
  fiber_type?: string;
  wavelength?: string;
  max_distance?: string;
  connector?: string;
  main_device?: string;
  category?: string;
  raw_specs?: string;
}

export interface BulkUpdateItem {
  id: string;
  changes: ProductUpdateData;
}

export interface BulkUpdateResponse {
  updated: number;
  errors: string[];
}

export async function listProducts(params?: {
  search?: string;
  category?: string;
  page?: number;
  page_size?: number;
}): Promise<ProductListResponse> {
  const searchParams = new URLSearchParams();
  if (params?.search) searchParams.set('search', params.search);
  if (params?.category) searchParams.set('category', params.category);
  if (params?.page) searchParams.set('page', String(params.page));
  if (params?.page_size) searchParams.set('page_size', String(params.page_size));

  const query = searchParams.toString();
  return api<ProductListResponse>(`/api/products/${query ? `?${query}` : ''}`);
}

export async function updateProduct(id: string, data: ProductUpdateData): Promise<ProductItem> {
  return api<ProductItem>(`/api/products/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export async function bulkUpdateProducts(items: BulkUpdateItem[]): Promise<BulkUpdateResponse> {
  return api<BulkUpdateResponse>('/api/products/bulk-update', {
    method: 'POST',
    body: JSON.stringify({ items }),
  });
}

export async function deleteProduct(id: string): Promise<{ message: string }> {
  return api<{ message: string }>(`/api/products/${id}`, { method: 'DELETE' });
}


export interface ExcelSyncResponse {
  total_rows_read: number;
  matched: number;
  updated: number;
  not_found: string[];
  message: string;
  file_id: string;
}

export interface ExcelFileItem {
  id: string;
  filename: string;
  file_size: number;
  total_rows: number;
  created_at: string;
}

export interface ExcelFileListResponse {
  total: number;
  files: ExcelFileItem[];
}

export async function syncExcel(files: FileList): Promise<ExcelSyncResponse> {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  return apiUpload<ExcelSyncResponse>('/api/products/upload-excel', formData);
}

export async function syncFromExcelRefs(): Promise<ExcelSyncResponse> {
  return api<ExcelSyncResponse>('/api/products/sync-excel', { method: 'POST' });
}

export async function listExcelFiles(): Promise<ExcelFileListResponse> {
  return api<ExcelFileListResponse>('/api/products/excel-files');
}

export async function deleteExcelFile(fileId: string): Promise<{ message: string }> {
  return api<{ message: string }>(`/api/products/excel-files/${fileId}`, { method: 'DELETE' });
}
