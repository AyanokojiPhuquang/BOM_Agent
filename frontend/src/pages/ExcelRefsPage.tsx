import { useState, useEffect, useCallback, useRef } from 'react';
import { cn } from '@/utils/cn';
import {
  listExcelFiles,
  deleteExcelFile,
  syncExcel,
  type ExcelFileItem,
} from '@/services/products';
import { api } from '@/services/api';

interface ExcelProductRef {
  product_code: string;
  description: string;
}

interface ExcelFileDetail {
  id: string;
  filename: string;
  file_size: number;
  total_rows: number;
  created_at: string;
  products: ExcelProductRef[];
}

export function ExcelRefsContent() {
  const [files, setFiles] = useState<ExcelFileItem[]>([]);
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);
  const [fileDetail, setFileDetail] = useState<ExcelFileDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingDetail, setIsLoadingDetail] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Inline editing
  const [editingCell, setEditingCell] = useState<{ index: number; field: 'product_code' | 'description' } | null>(null);
  const [pendingChanges, setPendingChanges] = useState<Map<number, Partial<ExcelProductRef>>>(new Map());
  const [isSaving, setIsSaving] = useState(false);
  const editInputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

  const fetchFiles = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await listExcelFiles();
      setFiles(data.files);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load files');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => { fetchFiles(); }, [fetchFiles]);

  useEffect(() => {
    if (successMsg) {
      const t = setTimeout(() => setSuccessMsg(null), 4000);
      return () => clearTimeout(t);
    }
  }, [successMsg]);

  useEffect(() => {
    if (editingCell && editInputRef.current) {
      editInputRef.current.focus();
    }
  }, [editingCell]);

  const fetchFileDetail = async (fileId: string) => {
    setIsLoadingDetail(true);
    setSelectedFileId(fileId);
    setPendingChanges(new Map());
    try {
      const data = await api<ExcelFileDetail>(`/api/products/excel-files/${fileId}`);
      setFileDetail(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load file detail');
    } finally {
      setIsLoadingDetail(false);
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputFiles = e.target.files;
    if (!inputFiles || inputFiles.length === 0) return;

    setIsSyncing(true);
    setError(null);
    setSuccessMsg(null);

    try {
      const result = await syncExcel(inputFiles);
      setSuccessMsg(result.message);
      await fetchFiles();
      if (result.file_id) {
        await fetchFileDetail(result.file_id);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsSyncing(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDeleteFile = async (fileId: string, filename: string) => {
    if (!confirm(`Xóa file "${filename}" và tất cả dữ liệu liên quan?`)) return;
    try {
      await deleteExcelFile(fileId);
      if (selectedFileId === fileId) {
        setSelectedFileId(null);
        setFileDetail(null);
      }
      await fetchFiles();
      setSuccessMsg(`Đã xóa "${filename}".`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Delete failed');
    }
  };

  // Inline editing handlers
  const startEditing = (index: number, field: 'product_code' | 'description') => {
    setEditingCell({ index, field });
  };

  const handleCellChange = (index: number, field: 'product_code' | 'description', value: string) => {
    if (!fileDetail) return;
    const original = fileDetail.products[index][field];
    if (value === original) {
      setEditingCell(null);
      return;
    }

    const existing = pendingChanges.get(index) || {};
    const updated = { ...existing, [field]: value };
    const newMap = new Map(pendingChanges);
    newMap.set(index, updated);
    setPendingChanges(newMap);

    // Update local display
    setFileDetail(prev => {
      if (!prev) return prev;
      const newProducts = [...prev.products];
      newProducts[index] = { ...newProducts[index], [field]: value };
      return { ...prev, products: newProducts };
    });
    setEditingCell(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent, index: number, field: 'product_code' | 'description', value: string) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleCellChange(index, field, value);
    } else if (e.key === 'Escape') {
      setEditingCell(null);
    }
  };

  const saveAllChanges = async () => {
    if (!fileDetail || pendingChanges.size === 0) return;
    setIsSaving(true);
    setError(null);

    try {
      // Send the full updated product list to backend
      const updatedProducts = fileDetail.products.map((p, i) => {
        const changes = pendingChanges.get(i);
        return changes ? { ...p, ...changes } : p;
      });

      await api(`/api/products/excel-files/${fileDetail.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ products: updatedProducts }),
      });

      setPendingChanges(new Map());
      setSuccessMsg(`Đã lưu ${pendingChanges.size} thay đổi.`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Save failed');
    } finally {
      setIsSaving(false);
    }
  };

  const discardChanges = () => {
    setPendingChanges(new Map());
    if (selectedFileId) fetchFileDetail(selectedFileId);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">Excel Reference Files</h2>
          <p className="text-sm text-gray-400 mt-1">
            Upload file Excel chứa cột P/N và Descriptions. Dữ liệu sẽ được dùng để sync mô tả vào tab Products.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <input
            ref={fileInputRef}
            type="file"
            accept=".xlsx,.xls"
            multiple
            onChange={handleUpload}
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isSyncing}
            className="px-4 py-2 text-sm font-medium text-white bg-accent rounded-lg hover:bg-accent-hover transition-colors disabled:opacity-50"
          >
            {isSyncing ? 'Đang xử lý...' : 'Upload Excel'}
          </button>
        </div>
      </div>

      {/* Messages */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-300 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}
      {successMsg && (
        <div className="bg-green-500/10 border border-green-500/30 text-green-300 px-4 py-3 rounded-lg text-sm">
          {successMsg}
        </div>
      )}

      <div className="flex gap-6">
        {/* File list (left) */}
        <div className="w-64 flex-shrink-0">
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Files ({files.length})</h3>
          {isLoading ? (
            <p className="text-gray-500 text-sm">Loading...</p>
          ) : files.length === 0 ? (
            <p className="text-gray-500 text-sm">Chưa có file nào.</p>
          ) : (
            <div className="space-y-1">
              {files.map(f => (
                <div
                  key={f.id}
                  className={cn(
                    'flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-colors',
                    selectedFileId === f.id ? 'bg-accent/15 border border-accent/30' : 'bg-dark-surface border border-dark-border hover:bg-dark-hover'
                  )}
                  onClick={() => fetchFileDetail(f.id)}
                >
                  <div className="min-w-0">
                    <p className="text-sm text-white truncate">{f.filename}</p>
                    <p className="text-xs text-gray-500">{f.total_rows} rows • {(f.file_size / 1024).toFixed(0)} KB</p>
                  </div>
                  <button
                    onClick={(e) => { e.stopPropagation(); handleDeleteFile(f.id, f.filename); }}
                    className="text-gray-500 hover:text-red-400 transition-colors ml-2 flex-shrink-0"
                    title="Xóa"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* File detail table (right) */}
        <div className="flex-1 min-w-0">
          {!selectedFileId ? (
            <div className="text-center py-12 bg-dark-surface border border-dark-border rounded-xl">
              <p className="text-gray-400">Chọn một file Excel ở bên trái để xem nội dung.</p>
            </div>
          ) : isLoadingDetail ? (
            <div className="text-center py-12">
              <svg className="animate-spin h-8 w-8 mx-auto text-accent" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            </div>
          ) : fileDetail ? (
            <div>
              {/* Save bar */}
              {pendingChanges.size > 0 && (
                <div className="flex items-center justify-between mb-3 px-3 py-2 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
                  <span className="text-sm text-yellow-400">{pendingChanges.size} thay đổi chưa lưu</span>
                  <div className="flex gap-2">
                    <button onClick={discardChanges} className="px-3 py-1 text-sm text-gray-300 border border-dark-border rounded hover:bg-dark-hover">
                      Hủy
                    </button>
                    <button onClick={saveAllChanges} disabled={isSaving} className="px-3 py-1 text-sm font-medium text-white bg-accent rounded hover:bg-accent-hover disabled:opacity-50">
                      {isSaving ? 'Đang lưu...' : 'Lưu'}
                    </button>
                  </div>
                </div>
              )}

              {/* Table */}
              <div className="border border-dark-border rounded-xl overflow-hidden">
                <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
                  <table className="w-full text-sm">
                    <thead className="sticky top-0 z-10">
                      <tr className="bg-dark-surface border-b border-dark-border">
                        <th className="px-3 py-2.5 text-left text-xs font-semibold text-gray-400 uppercase w-10">#</th>
                        <th className="px-3 py-2.5 text-left text-xs font-semibold text-gray-400 uppercase w-48">Product Code (P/N)</th>
                        <th className="px-3 py-2.5 text-left text-xs font-semibold text-gray-400 uppercase">Description</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-dark-border">
                      {fileDetail.products.map((product, index) => (
                        <tr key={index} className={cn(
                          'hover:bg-dark-hover transition-colors',
                          pendingChanges.has(index) && 'bg-yellow-500/5'
                        )}>
                          <td className="px-3 py-1.5 text-gray-500 text-xs">{index + 1}</td>
                          <td className="px-3 py-1.5">
                            {editingCell?.index === index && editingCell?.field === 'product_code' ? (
                              <input
                                ref={editInputRef as React.RefObject<HTMLInputElement>}
                                type="text"
                                defaultValue={product.product_code}
                                className="w-full px-2 py-1 bg-dark-bg border border-accent rounded text-white text-xs focus:outline-none"
                                onBlur={e => handleCellChange(index, 'product_code', e.target.value)}
                                onKeyDown={e => handleKeyDown(e, index, 'product_code', (e.target as HTMLInputElement).value)}
                              />
                            ) : (
                              <div
                                onClick={() => startEditing(index, 'product_code')}
                                className="cursor-pointer text-gray-300 hover:text-white hover:bg-dark-bg/50 px-1 py-0.5 rounded text-xs font-mono"
                                title="Click to edit"
                              >
                                {product.product_code || <span className="text-gray-600 italic">—</span>}
                              </div>
                            )}
                          </td>
                          <td className="px-3 py-1.5">
                            {editingCell?.index === index && editingCell?.field === 'description' ? (
                              <textarea
                                ref={editInputRef as React.RefObject<HTMLTextAreaElement>}
                                defaultValue={product.description}
                                rows={2}
                                className="w-full px-2 py-1 bg-dark-bg border border-accent rounded text-white text-xs resize-none focus:outline-none"
                                onBlur={e => handleCellChange(index, 'description', e.target.value)}
                                onKeyDown={e => handleKeyDown(e, index, 'description', (e.target as HTMLTextAreaElement).value)}
                              />
                            ) : (
                              <div
                                onClick={() => startEditing(index, 'description')}
                                className="cursor-pointer text-gray-300 hover:text-white hover:bg-dark-bg/50 px-1 py-0.5 rounded text-xs truncate max-w-xl"
                                title={product.description || '(empty - click to edit)'}
                              >
                                {product.description || <span className="text-gray-600 italic">—</span>}
                              </div>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
