import { useState, useEffect, useCallback, useRef } from 'react';
import { cn } from '@/utils/cn';
import {
  uploadDatasheetsFolder,
  listDatasheets,
  deleteAllDatasheets,
  deleteProduct,
  uploadPdfDatasheets,
  listUploadedPdfs,
  deleteUploadedPdf,
  addDatasheetFromUrl,
  type DatasheetProduct,
  type PdfFileItem,
} from '@/services/datasheets';

export function DatasheetsContent() {
  const [products, setProducts] = useState<DatasheetProduct[]>([]);
  const [categories, setCategories] = useState<Record<string, number>>({});
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [replaceOnUpload, setReplaceOnUpload] = useState(false);
  const [isUploadingPdf, setIsUploadingPdf] = useState(false);
  const [pdfFiles, setPdfFiles] = useState<PdfFileItem[]>([]);
  const [datasheetUrl, setDatasheetUrl] = useState('');
  const [isFetchingUrl, setIsFetchingUrl] = useState(false);
  const folderInputRef = useRef<HTMLInputElement>(null);
  const pdfInputRef = useRef<HTMLInputElement>(null);

  const fetchDatasheets = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listDatasheets();
      setProducts(data.products);
      setCategories(data.categories);
      setTotal(data.total);
      const pdfs = await listUploadedPdfs();
      setPdfFiles(pdfs.files);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load datasheets');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDatasheets();
  }, [fetchDatasheets]);

  const handleFolderSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setIsUploading(true);
    setUploadResult(null);
    setError(null);

    try {
      const result = await uploadDatasheetsFolder(files, replaceOnUpload);
      setUploadResult(result.message);
      await fetchDatasheets();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Upload failed');
    } finally {
      setIsUploading(false);
      // Reset input
      if (folderInputRef.current) {
        folderInputRef.current.value = '';
      }
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete ALL datasheets? This cannot be undone.')) {
      return;
    }

    setError(null);
    try {
      const result = await deleteAllDatasheets();
      setUploadResult(result.message);
      await fetchDatasheets();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Delete failed');
    }
  };

  const handleDeleteProduct = async (code: string) => {
    if (!confirm(`Delete product "${code}" and its datasheet?`)) return;
    try {
      await deleteProduct(code);
      await fetchDatasheets();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Delete failed');
    }
  };

  const handlePdfUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setIsUploadingPdf(true);
    setUploadResult(null);
    setError(null);

    try {
      const result = await uploadPdfDatasheets(files);
      let msg = result.message;
      if (result.errors.length > 0) {
        msg += ` Errors: ${result.errors.join('; ')}`;
      }
      setUploadResult(msg);
      await fetchDatasheets();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'PDF upload failed');
    } finally {
      setIsUploadingPdf(false);
      if (pdfInputRef.current) pdfInputRef.current.value = '';
    }
  };

  const handleAddFromUrl = async () => {
    const url = datasheetUrl.trim();
    if (!url) return;

    setIsFetchingUrl(true);
    setUploadResult(null);
    setError(null);

    try {
      const result = await addDatasheetFromUrl(url);
      setUploadResult(result.message);
      setDatasheetUrl('');
      await fetchDatasheets();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to fetch datasheet from URL');
    } finally {
      setIsFetchingUrl(false);
    }
  };

  const filteredProducts = products.filter(p => {
    const matchesCategory = filterCategory === 'all' || p.category === filterCategory;
    const matchesSearch = !searchQuery ||
      p.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.category.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white">Datasheets Management</h2>
        <p className="text-gray-400 mt-1">
          Upload product datasheets folder to enable BOM generation. Without datasheets, the agent cannot create BOMs.
        </p>
      </div>

      {/* Upload Folder Section - hidden for now */}
      {false && <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Upload Datasheets Folder</h3>
        <p className="text-sm text-gray-400 mb-4">
          Select the datasheets folder from your computer. It should contain subfolders organized by product family
          (e.g. SFP/, QSFP/, AOC/), each with product folders containing .md files.
        </p>

        <div className="flex items-center gap-4 flex-wrap">
          <label className={cn(
            'inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm cursor-pointer transition-colors',
            isUploading
              ? 'bg-gray-600 text-gray-300 cursor-not-allowed'
              : 'bg-accent text-white hover:bg-accent/90'
          )}>
            {isUploading ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Uploading...
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                Choose Folder
              </>
            )}
            <input
              ref={folderInputRef}
              type="file"
              // @ts-expect-error webkitdirectory is not in the type defs
              webkitdirectory=""
              directory=""
              multiple
              onChange={handleFolderSelect}
              disabled={isUploading}
              className="hidden"
            />
          </label>

          <label className="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">
            <input
              type="checkbox"
              checked={replaceOnUpload}
              onChange={e => setReplaceOnUpload(e.target.checked)}
              className="rounded border-gray-600 bg-dark-bg text-accent focus:ring-accent"
            />
            Replace existing datasheets
          </label>

          {total > 0 && (
            <button
              onClick={handleDelete}
              className="ml-auto px-4 py-2 rounded-lg text-sm font-medium text-red-400 border border-red-400/30 hover:bg-red-400/10 transition-colors"
            >
              Delete All
            </button>
          )}
        </div>

        {/* Status messages */}
        {uploadResult && (
          <div className="mt-4 p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm">
            {uploadResult}
          </div>
        )}
        {error && (
          <div className="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            {error}
          </div>
        )}
      </div>}

      {/* PDF Upload Section */}
      <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Upload PDF Datasheets</h3>
        <p className="text-sm text-gray-400 mb-4">
          Upload PDF files containing product specifications. They will be converted to markdown automatically.
        </p>

        <div className="flex items-center gap-4 flex-wrap">
          <label className={cn(
            'inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm cursor-pointer transition-colors',
            isUploadingPdf
              ? 'bg-gray-600 text-gray-300 cursor-not-allowed'
              : 'bg-accent/80 text-white hover:bg-accent'
          )}>
            {isUploadingPdf ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Processing...
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                Upload PDFs
              </>
            )}
            <input
              ref={pdfInputRef}
              type="file"
              accept=".pdf"
              multiple
              onChange={handlePdfUpload}
              disabled={isUploadingPdf}
              className="hidden"
            />
          </label>
        </div>
      </div>

      {/* Add from Product URL Section */}
      <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Add Datasheet from Product URL</h3>
        <p className="text-sm text-gray-400 mb-4">
          Paste a product page URL. The system uses AI to locate the datasheet download link on the page,
          downloads it, and extracts the product specifications automatically.
        </p>

        <div className="flex items-center gap-3 flex-wrap">
          <input
            type="url"
            placeholder="https://example.com/products/my-product"
            value={datasheetUrl}
            onChange={e => setDatasheetUrl(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !isFetchingUrl && datasheetUrl.trim()) {
                handleAddFromUrl();
              }
            }}
            disabled={isFetchingUrl}
            className="flex-1 min-w-[280px] px-3 py-2 rounded-lg bg-dark-bg border border-dark-border text-white text-sm placeholder-gray-500 focus:outline-none focus:border-accent disabled:opacity-50"
          />
          <button
            onClick={handleAddFromUrl}
            disabled={isFetchingUrl || !datasheetUrl.trim()}
            className={cn(
              'inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm transition-colors',
              isFetchingUrl || !datasheetUrl.trim()
                ? 'bg-gray-600 text-gray-300 cursor-not-allowed'
                : 'bg-accent/80 text-white hover:bg-accent'
            )}
          >
            {isFetchingUrl ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Finding datasheet...
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                </svg>
                Fetch from URL
              </>
            )}
          </button>
        </div>
      </div>

      {/* Global status messages */}
      {uploadResult && (
        <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm">
          {uploadResult}
        </div>
      )}
      {error && (
        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Stats */}
      {total > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-dark-surface border border-dark-border rounded-xl p-4">
            <div className="text-2xl font-bold text-white">{total}</div>
            <div className="text-sm text-gray-400">Total Products</div>
          </div>
          <div className="bg-dark-surface border border-dark-border rounded-xl p-4">
            <div className="text-2xl font-bold text-white">{Object.keys(categories).length}</div>
            <div className="text-sm text-gray-400">Categories</div>
          </div>
          {Object.entries(categories).slice(0, 2).map(([cat, count]) => (
            <div key={cat} className="bg-dark-surface border border-dark-border rounded-xl p-4">
              <div className="text-2xl font-bold text-white">{count}</div>
              <div className="text-sm text-gray-400">{cat}</div>
            </div>
          ))}
        </div>
      )}

      {/* Product List */}
      {total > 0 && (
        <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
          <div className="flex items-center gap-4 mb-4 flex-wrap">
            <h3 className="text-lg font-semibold text-white">Products ({filteredProducts.length})</h3>

            {/* Search */}
            <input
              type="text"
              placeholder="Search products..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="px-3 py-1.5 rounded-lg bg-dark-bg border border-dark-border text-white text-sm placeholder-gray-500 focus:outline-none focus:border-accent"
            />

            {/* Category filter */}
            <select
              value={filterCategory}
              onChange={e => setFilterCategory(e.target.value)}
              className="px-3 py-1.5 rounded-lg bg-dark-bg border border-dark-border text-white text-sm focus:outline-none focus:border-accent"
            >
              <option value="all">All Categories</option>
              {Object.keys(categories).sort().map(cat => (
                <option key={cat} value={cat}>{cat} ({categories[cat]})</option>
              ))}
            </select>
          </div>

          {/* Table */}
          <div className="overflow-auto max-h-96">
            <table className="w-full text-sm">
              <thead className="text-gray-400 border-b border-dark-border">
                <tr>
                  <th className="text-left py-2 px-3 font-medium">Code</th>
                  <th className="text-left py-2 px-3 font-medium">Category</th>
                  <th className="text-left py-2 px-3 font-medium">Datasheet Path</th>
                  <th className="text-right py-2 px-3 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="text-gray-300">
                {filteredProducts.map(p => (
                  <tr key={p.datasheet_path} className="border-b border-dark-border/50 hover:bg-dark-hover/50">
                    <td className="py-2 px-3 font-mono text-white">{p.code}</td>
                    <td className="py-2 px-3">
                      <span className="px-2 py-0.5 rounded-full text-xs bg-accent/10 text-accent">
                        {p.category}
                      </span>
                    </td>
                    <td className="py-2 px-3 text-gray-500 text-xs">{p.datasheet_path}</td>
                    <td className="py-2 px-3 text-right">
                      <button
                        onClick={() => handleDeleteProduct(p.code)}
                        className="text-red-400 hover:text-red-300 text-xs hover:bg-red-500/10 px-2 py-1 rounded transition-colors"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Uploaded PDFs */}
      {pdfFiles.length > 0 && (
        <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Uploaded PDFs ({pdfFiles.length})</h3>
          <div className="overflow-auto max-h-64">
            <table className="w-full text-sm">
              <thead className="text-gray-400 border-b border-dark-border">
                <tr>
                  <th className="text-left py-2 px-3 font-medium">Filename</th>
                  <th className="text-left py-2 px-3 font-medium">Category</th>
                  <th className="text-right py-2 px-3 font-medium">Size</th>
                  <th className="text-right py-2 px-3 font-medium">Action</th>
                </tr>
              </thead>
              <tbody className="text-gray-300">
                {pdfFiles.map(f => (
                  <tr key={f.download_url} className="border-b border-dark-border/50 hover:bg-dark-hover/50">
                    <td className="py-2 px-3 font-mono text-white text-xs">{f.filename}</td>
                    <td className="py-2 px-3">
                      <span className="px-2 py-0.5 rounded-full text-xs bg-accent/10 text-accent">{f.category}</span>
                    </td>
                    <td className="py-2 px-3 text-right text-gray-400">{(f.size / 1024).toFixed(0)} KB</td>
                    <td className="py-2 px-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => {
                            const token = localStorage.getItem('starlink_token');
                            fetch(f.download_url, { headers: token ? { Authorization: `Bearer ${token}` } : {} })
                              .then(res => res.blob())
                              .then(blob => {
                                const url = URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = f.filename;
                                a.click();
                                URL.revokeObjectURL(url);
                              });
                          }}
                          className="text-accent hover:text-accent-hover text-xs px-2 py-1 rounded hover:bg-accent/10 transition-colors"
                        >
                          Download
                        </button>
                        <button
                          onClick={async () => {
                            if (!confirm(`Delete PDF "${f.filename}"?`)) return;
                            try {
                              await deleteUploadedPdf(f.download_url);
                              await fetchDatasheets();
                            } catch (e: unknown) {
                              setError(e instanceof Error ? e.message : 'Delete failed');
                            }
                          }}
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
        </div>
      )}

      {/* Empty state */}
      {!isLoading && total === 0 && (
        <div className="text-center py-12 bg-dark-surface border border-dark-border rounded-xl">
          <svg className="mx-auto h-12 w-12 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
          </svg>
          <h3 className="mt-4 text-lg font-medium text-white">No datasheets uploaded</h3>
          <p className="mt-2 text-gray-400 max-w-md mx-auto">
            Upload a datasheets folder to enable BOM generation.
            The agent cannot create BOMs without product specifications.
          </p>
        </div>
      )}
    </div>
  );
}
