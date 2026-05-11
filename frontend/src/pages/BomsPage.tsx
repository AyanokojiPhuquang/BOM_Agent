import { useState, useEffect, useCallback } from 'react';
import { listBoms, deleteBom, type BomFileItem } from '@/services/boms';

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(epochMs: number): string {
  return new Date(epochMs).toLocaleString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function extractCustomerName(filename: string): string {
  // Format: 20260507_054920_fpt_telecom.xlsx
  const parts = filename.replace('.xlsx', '').split('_');
  if (parts.length > 2) {
    return parts.slice(2).join(' ').replace(/\b\w/g, c => c.toUpperCase());
  }
  return filename;
}

export function BomsContent() {
  const [boms, setBoms] = useState<BomFileItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const fetchBoms = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listBoms();
      setBoms(data.items);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load BOMs');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBoms();
  }, [fetchBoms]);

  const handleDelete = async (filename: string) => {
    if (!confirm(`Delete BOM "${filename}"?`)) return;
    setError(null);
    try {
      const result = await deleteBom(filename);
      setMessage(result.message);
      await fetchBoms();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Delete failed');
    }
  };

  const handleDownload = async (url: string, filename: string) => {
    try {
      const token = localStorage.getItem('starlink_token');
      const res = await fetch(url, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!res.ok) throw new Error('Download failed');
      const blob = await res.blob();
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      a.click();
      URL.revokeObjectURL(a.href);
    } catch {
      setError('Failed to download file');
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white">BOM History</h2>
        <p className="text-gray-400 mt-1">
          View and download previously generated Bills of Materials.
        </p>
      </div>

      {/* Messages */}
      {message && (
        <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm">
          {message}
        </div>
      )}
      {error && (
        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* BOM List */}
      {!isLoading && boms.length > 0 && (
        <div className="bg-dark-surface border border-dark-border rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="text-gray-400 border-b border-dark-border bg-dark-bg/50">
              <tr>
                <th className="text-left py-3 px-4 font-medium">Customer</th>
                <th className="text-left py-3 px-4 font-medium">Filename</th>
                <th className="text-left py-3 px-4 font-medium">Created</th>
                <th className="text-right py-3 px-4 font-medium">Size</th>
                <th className="text-right py-3 px-4 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody className="text-gray-300">
              {boms.map(bom => (
                <tr key={bom.filename} className="border-b border-dark-border/50 hover:bg-dark-hover/50">
                  <td className="py-3 px-4 text-white font-medium">
                    {extractCustomerName(bom.filename)}
                  </td>
                  <td className="py-3 px-4 font-mono text-xs text-gray-500">
                    {bom.filename}
                  </td>
                  <td className="py-3 px-4 text-gray-400">
                    {formatDate(bom.created_at)}
                  </td>
                  <td className="py-3 px-4 text-right text-gray-400">
                    {formatFileSize(bom.size)}
                  </td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => handleDownload(bom.download_url, bom.filename)}
                        className="text-accent hover:text-accent-hover text-xs px-2 py-1 rounded hover:bg-accent/10 transition-colors"
                      >
                        Download
                      </button>
                      <button
                        onClick={() => handleDelete(bom.filename)}
                        className="text-red-400 hover:text-red-300 text-xs px-2 py-1 rounded hover:bg-red-500/10 transition-colors"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Empty state */}
      {!isLoading && boms.length === 0 && (
        <div className="text-center py-12 bg-dark-surface border border-dark-border rounded-xl">
          <svg className="mx-auto h-12 w-12 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 className="mt-4 text-lg font-medium text-white">No BOMs generated yet</h3>
          <p className="mt-2 text-gray-400 max-w-md mx-auto">
            BOMs will appear here after you generate them through the chat interface.
          </p>
        </div>
      )}

      {/* Loading */}
      {isLoading && (
        <div className="text-center py-12">
          <svg className="animate-spin h-8 w-8 mx-auto text-accent" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        </div>
      )}
    </div>
  );
}
