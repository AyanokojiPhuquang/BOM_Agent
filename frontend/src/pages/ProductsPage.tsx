import { useState, useEffect, useCallback, useRef } from 'react';
import { cn } from '@/utils/cn';
import {
  listProducts,
  bulkUpdateProducts,
  deleteProduct,
  syncFromExcelRefs,
  type ProductItem,
  type ProductUpdateData,
} from '@/services/products';

const EDITABLE_COLUMNS = [
  { key: 'code', label: 'Product Code', width: 'w-36' },
  { key: 'name', label: 'Name', width: 'w-44' },
  { key: 'brand', label: 'Brand', width: 'w-28' },
  { key: 'description', label: 'Description', width: 'w-64' },
  { key: 'data_rate', label: 'Data Rate', width: 'w-24' },
  { key: 'fiber_type', label: 'Fiber', width: 'w-28' },
  { key: 'wavelength', label: 'Wavelength', width: 'w-28' },
  { key: 'max_distance', label: 'Distance', width: 'w-24' },
  { key: 'connector', label: 'Connector', width: 'w-28' },
  { key: 'main_device', label: 'Main Device', width: 'w-28' },
  { key: 'category', label: 'Category', width: 'w-28' },
] as const;

type EditableField = (typeof EDITABLE_COLUMNS)[number]['key'];

export function ProductsContent() {
  const [products, setProducts] = useState<ProductItem[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Inline editing state
  const [editingCell, setEditingCell] = useState<{ id: string; field: EditableField } | null>(null);
  const [pendingChanges, setPendingChanges] = useState<Map<string, ProductUpdateData>>(new Map());
  const [isSaving, setIsSaving] = useState(false);
  const editInputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<string | null>(null);

  const PAGE_SIZE = 50;

  const fetchProducts = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listProducts({ search: search || undefined, page, page_size: PAGE_SIZE });
      setProducts(data.products);
      setTotal(data.total);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load products');
    } finally {
      setIsLoading(false);
    }
  }, [search, page]);

  useEffect(() => { fetchProducts(); }, [fetchProducts]);

  // Auto-dismiss messages
  useEffect(() => {
    if (successMsg) {
      const t = setTimeout(() => setSuccessMsg(null), 4000);
      return () => clearTimeout(t);
    }
  }, [successMsg]);

  // Focus input when editing
  useEffect(() => {
    if (editingCell && editInputRef.current) {
      editInputRef.current.focus();
    }
  }, [editingCell]);

  // --- Inline Editing ---

  const startEditing = (id: string, field: EditableField) => {
    setEditingCell({ id, field });
  };

  const handleCellChange = (id: string, field: EditableField, value: string) => {
    const product = products.find(p => p.id === id);
    if (!product) return;

    const originalValue = product[field] || '';
    if (value === originalValue) {
      setEditingCell(null);
      return;
    }

    // Track change
    const existing = pendingChanges.get(id) || {};
    const updated = { ...existing, [field]: value };
    const newMap = new Map(pendingChanges);
    newMap.set(id, updated);
    setPendingChanges(newMap);

    // Update local display
    setProducts(prev => prev.map(p => p.id === id ? { ...p, [field]: value } : p));
    setEditingCell(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent, id: string, field: EditableField, value: string) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleCellChange(id, field, value);
    } else if (e.key === 'Escape') {
      setEditingCell(null);
    }
  };

  const saveAllChanges = async () => {
    if (pendingChanges.size === 0) return;
    setIsSaving(true);
    setError(null);

    try {
      const items = Array.from(pendingChanges.entries()).map(([id, changes]) => ({ id, changes }));
      const result = await bulkUpdateProducts(items);
      setSuccessMsg(`Saved ${result.updated} product(s) successfully.`);
      if (result.errors.length > 0) {
        setError(`Some updates failed: ${result.errors.join(', ')}`);
      }
      setPendingChanges(new Map());
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Save failed');
    } finally {
      setIsSaving(false);
    }
  };

  const discardChanges = () => {
    setPendingChanges(new Map());
    fetchProducts();
  };

  const handleDeleteProduct = async (id: string, code: string) => {
    if (!confirm(`Delete product "${code}"?`)) return;
    try {
      await deleteProduct(id);
      await fetchProducts();
      setSuccessMsg(`Product "${code}" deleted.`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Delete failed');
    }
  };

  const handleExcelSync = async () => {
    setIsSyncing(true);
    setError(null);
    setSyncResult(null);

    try {
      const result = await syncFromExcelRefs();
      setSyncResult(result.message);
      if (result.updated > 0) {
        await fetchProducts();
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Sync failed');
    } finally {
      setIsSyncing(false);
    }
  };

  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">Product Catalog</h2>
          <p className="text-sm text-gray-400 mt-1">
            {total} product(s) extracted from uploaded datasheets. Click any cell to edit.
          </p>
        </div>
        {pendingChanges.size > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-yellow-400">{pendingChanges.size} unsaved change(s)</span>
            <button
              onClick={discardChanges}
              className="px-3 py-1.5 text-sm text-gray-300 border border-dark-border rounded-lg hover:bg-dark-hover transition-colors"
            >
              Discard
            </button>
            <button
              onClick={saveAllChanges}
              disabled={isSaving}
              className="px-4 py-1.5 text-sm font-medium text-white bg-accent rounded-lg hover:bg-accent-hover transition-colors disabled:opacity-50"
            >
              {isSaving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        )}
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
      {syncResult && (
        <div className="bg-blue-500/10 border border-blue-500/30 text-blue-300 px-4 py-3 rounded-lg text-sm">
          {syncResult}
        </div>
      )}

      {/* Excel Sync */}
      <div className="bg-dark-surface border border-dark-border rounded-xl p-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-white">Đồng bộ mô tả từ Excel</h3>
            <p className="text-xs text-gray-500 mt-0.5">Cập nhật mô tả sản phẩm từ dữ liệu đã upload ở tab "Excel Refs".</p>
          </div>
          <button
            onClick={handleExcelSync}
            disabled={isSyncing}
            className="px-4 py-2 text-sm font-medium text-white bg-accent rounded-lg hover:bg-accent-hover transition-colors disabled:opacity-50 whitespace-nowrap"
          >
            {isSyncing ? 'Đang đồng bộ...' : 'Sync từ Excel'}
          </button>
        </div>
      </div>

      {/* Search & Pagination */}
      <div className="flex items-center gap-3">
        <input
          type="text"
          value={search}
          onChange={e => { setSearch(e.target.value); setPage(1); }}
          placeholder="Search by code, name, brand..."
          className="w-80 px-3 py-2 bg-dark-surface border border-dark-border rounded-lg text-white placeholder-gray-500 text-sm focus:outline-none focus:border-accent"
        />
        <span className="text-sm text-gray-500">
          Page {page} of {totalPages || 1}
        </span>
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page <= 1}
          className="px-2 py-1 text-sm text-gray-400 border border-dark-border rounded hover:bg-dark-hover disabled:opacity-30"
        >
          ←
        </button>
        <button
          onClick={() => setPage(p => Math.min(totalPages, p + 1))}
          disabled={page >= totalPages}
          className="px-2 py-1 text-sm text-gray-400 border border-dark-border rounded hover:bg-dark-hover disabled:opacity-30"
        >
          →
        </button>
      </div>

      {/* Data Table */}
      {isLoading ? (
        <div className="text-center py-12">
          <svg className="animate-spin h-8 w-8 mx-auto text-accent" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        </div>
      ) : products.length === 0 ? (
        <div className="text-center py-12 bg-dark-surface border border-dark-border rounded-xl">
          <h3 className="text-lg font-medium text-white mt-4">No products found</h3>
          <p className="mt-2 text-gray-400">Upload PDF datasheets to get started.</p>
        </div>
      ) : (
        <div className="border border-dark-border rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-dark-surface border-b border-dark-border">
                  {EDITABLE_COLUMNS.map(col => (
                    <th key={col.key} className={cn('px-3 py-2.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider', col.width)}>
                      {col.label}
                    </th>
                  ))}
                  <th className="px-3 py-2.5 text-right text-xs font-semibold text-gray-400 uppercase w-16">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-border">
                {products.map(product => (
                  <tr key={product.id} className={cn(
                    'hover:bg-dark-hover transition-colors',
                    pendingChanges.has(product.id) && 'bg-yellow-500/5'
                  )}>
                    {EDITABLE_COLUMNS.map(col => {
                      const isEditing = editingCell?.id === product.id && editingCell?.field === col.key;
                      const value = product[col.key] || '';

                      return (
                        <td key={col.key} className={cn('px-3 py-2', col.width)}>
                          {isEditing ? (
                            col.key === 'description' ? (
                              <textarea
                                ref={editInputRef as React.RefObject<HTMLTextAreaElement>}
                                defaultValue={value}
                                rows={2}
                                className="w-full px-2 py-1 bg-dark-bg border border-accent rounded text-white text-xs resize-none focus:outline-none"
                                onBlur={e => handleCellChange(product.id, col.key, e.target.value)}
                                onKeyDown={e => handleKeyDown(e, product.id, col.key, (e.target as HTMLTextAreaElement).value)}
                              />
                            ) : (
                              <input
                                ref={editInputRef as React.RefObject<HTMLInputElement>}
                                type="text"
                                defaultValue={value}
                                className="w-full px-2 py-1 bg-dark-bg border border-accent rounded text-white text-xs focus:outline-none"
                                onBlur={e => handleCellChange(product.id, col.key, e.target.value)}
                                onKeyDown={e => handleKeyDown(e, product.id, col.key, (e.target as HTMLInputElement).value)}
                              />
                            )
                          ) : (
                            <div
                              onClick={() => startEditing(product.id, col.key)}
                              className="cursor-pointer min-h-[1.5rem] text-gray-300 hover:text-white hover:bg-dark-bg/50 px-1 py-0.5 rounded truncate"
                              title={value || '(empty - click to edit)'}
                            >
                              {value || <span className="text-gray-600 italic">—</span>}
                            </div>
                          )}
                        </td>
                      );
                    })}
                    <td className="px-3 py-2 text-right">
                      <button
                        onClick={() => handleDeleteProduct(product.id, product.code)}
                        className="text-gray-500 hover:text-red-400 transition-colors"
                        title="Delete"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
