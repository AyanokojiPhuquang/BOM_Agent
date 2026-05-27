import { api, apiUpload } from './api';

export interface DatasheetProduct {
  code: string;
  datasheet_path: string;
  category: string;
}

export interface ProductDetail {
  code: string;
  datasheet_path: string;
  category: string;
  content_preview: string;
  file_size: number;
  has_images: boolean;
  image_count: number;
}

export interface UploadDatasheetsResponse {
  message: string;
  total_files: number;
  total_products_created: number;
  total_products_updated: number;
  products: DatasheetProduct[];
}

export interface PdfUploadResponse {
  message: string;
  total_pdfs_processed: number;
  total_products_created: number;
  total_products_updated: number;
  products: DatasheetProduct[];
  errors: string[];
}

export interface DatasheetListResponse {
  total: number;
  categories: Record<string, number>;
  products: DatasheetProduct[];
}

export interface DeleteDatasheetsResponse {
  message: string;
  deleted_files: number;
  deleted_products: number;
}

export async function uploadDatasheetsFolder(
  files: FileList,
  replace: boolean = false,
): Promise<UploadDatasheetsResponse> {
  // For large folders, create a ZIP client-side and upload that instead
  // This avoids multipart field limits and is much faster
  if (files.length > 100) {
    return uploadAsZip(files, replace);
  }

  const formData = new FormData();

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    formData.append('files', file);
    formData.append('paths', file.webkitRelativePath);
  }

  return apiUpload<UploadDatasheetsResponse>(
    `/api/datasheets/upload?replace=${replace}`,
    formData,
  );
}

async function uploadAsZip(
  files: FileList,
  replace: boolean,
): Promise<UploadDatasheetsResponse> {
  // Send files in batches to avoid hitting limits
  const BATCH_SIZE = 50;
  let lastResult: UploadDatasheetsResponse | null = null;

  for (let i = 0; i < files.length; i += BATCH_SIZE) {
    const batch = Array.from(files).slice(i, i + BATCH_SIZE);
    const formData = new FormData();

    for (const file of batch) {
      formData.append('files', file);
      formData.append('paths', file.webkitRelativePath);
    }

    // Only replace on first batch
    const shouldReplace = replace && i === 0;
    lastResult = await apiUpload<UploadDatasheetsResponse>(
      `/api/datasheets/upload?replace=${shouldReplace}`,
      formData,
    );
  }

  // Return the final result (which has the full product list)
  return lastResult!;
}

export async function listDatasheets(): Promise<DatasheetListResponse> {
  return api<DatasheetListResponse>('/api/datasheets/');
}

export async function getProductDetail(code: string): Promise<ProductDetail> {
  return api<ProductDetail>(`/api/datasheets/products/${encodeURIComponent(code)}`);
}

export async function deleteProduct(code: string): Promise<{ message: string }> {
  return api<{ message: string }>(`/api/datasheets/products/${encodeURIComponent(code)}`, {
    method: 'DELETE',
  });
}

export async function deleteAllDatasheets(): Promise<DeleteDatasheetsResponse> {
  return api<DeleteDatasheetsResponse>('/api/datasheets/', { method: 'DELETE' });
}


export async function uploadPdfDatasheets(
  files: FileList | File[],
  category: string = 'PDF',
): Promise<PdfUploadResponse> {
  const formData = new FormData();

  const fileArray = files instanceof FileList ? Array.from(files) : files;
  for (const file of fileArray) {
    formData.append('files', file);
  }
  formData.append('category', category);

  return apiUpload<PdfUploadResponse>('/api/datasheets/upload-pdf', formData);
}


export interface PdfFileItem {
  filename: string;
  category: string;
  size: number;
  download_url: string;
}

export interface PdfListResponse {
  total: number;
  files: PdfFileItem[];
}

export async function listUploadedPdfs(): Promise<PdfListResponse> {
  return api<PdfListResponse>('/api/datasheets/pdfs');
}


export async function deleteUploadedPdf(downloadUrl: string): Promise<{ message: string }> {
  return api<{ message: string }>(downloadUrl, { method: 'DELETE' });
}
