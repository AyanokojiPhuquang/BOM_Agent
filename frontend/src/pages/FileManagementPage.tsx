import { useCallback, useEffect, useState } from 'react';
import { Button } from '@/components/common/Button';
import { ErrorBanner } from '@/components/common/ErrorBanner';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { StatusBadge } from '@/components/common/StatusBadge';
import { FileIcon } from '@/components/common/FileIcon';
import { FolderIcon, EditIcon, TrashIcon, EyeIcon } from '@/components/icons';
import { UploadModal } from '@/components/files/UploadModal';
import { EditFileModal } from '@/components/files/EditFileModal';
import { PreviewModal } from '@/components/files/PreviewModal';
import { FolderModal } from '@/components/files/FolderModal';
import { useModal } from '@/hooks/useModal';
import { useConfirmDelete } from '@/hooks/useConfirmDelete';
import { formatSize } from '@/utils/format';
import type { FileItem, FolderItem } from '@/services/files';
import * as filesService from '@/services/files';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type ModalMode =
  | { type: 'upload' }
  | { type: 'edit'; file: FileItem }
  | { type: 'preview'; file: FileItem }
  | { type: 'newFolder' }
  | { type: 'renameFolder'; folder: FolderItem };

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function FileManagementContent() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [folders, setFolders] = useState<FolderItem[]>([]);
  const [breadcrumb, setBreadcrumb] = useState<FolderItem[]>([]);
  const [currentFolderId, setCurrentFolderId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');

  const { modal, open: openModal, close: closeModal } = useModal<ModalMode>();
  const fileDelete = useConfirmDelete();
  const folderDelete = useConfirmDelete();

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const data = await filesService.listFiles(currentFolderId, search || undefined);
      setFiles(data.items);
      setFolders(data.folders);
      setBreadcrumb(data.breadcrumb);
    } catch {
      setError('Failed to load files');
    } finally {
      setLoading(false);
    }
  }, [currentFolderId, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const navigateToFolder = (folderId: string | null) => {
    setCurrentFolderId(folderId);
    setSearch('');
    fileDelete.cancel();
    folderDelete.cancel();
  };

  const handleDeleteFile = async (id: string) => {
    try {
      await filesService.deleteFile(id);
      setFiles(prev => prev.filter(f => f.id !== id));
      fileDelete.cancel();
    } catch {
      setError('Failed to delete file');
    }
  };

  const handleDeleteFolder = async (id: string) => {
    try {
      await filesService.deleteFolder(id);
      setFolders(prev => prev.filter(f => f.id !== id));
      folderDelete.cancel();
    } catch {
      setError('Folder is not empty or could not be deleted');
    }
  };

  const handleModalSaved = () => { closeModal(); fetchData(); };

  const fileStatusVariant = (status: string) =>
    status === 'ready' ? 'success' : status === 'error' ? 'error' : 'warning';

  return (
    <div className="p-6">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-1 text-sm text-gray-400 mb-4">
        <button onClick={() => navigateToFolder(null)} className="hover:text-white transition-colors">
          Home
        </button>
        {breadcrumb.map(folder => (
          <span key={folder.id} className="flex items-center gap-1">
            <span className="text-gray-600">/</span>
            <button onClick={() => navigateToFolder(folder.id)} className="hover:text-white transition-colors">
              {folder.name}
            </button>
          </span>
        ))}
      </nav>

      {/* Action bar */}
      <div className="flex items-center justify-between mb-4 gap-4">
        <div className="flex items-center gap-2">
          <Button onClick={() => openModal({ type: 'upload' })}>Upload Files</Button>
          <Button variant="ghost" onClick={() => openModal({ type: 'newFolder' })}>New Folder</Button>
        </div>
        <input
          type="text"
          placeholder="Search files..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="px-3 py-2 rounded-lg bg-dark-bg border border-dark-border text-white text-sm focus:outline-none focus:border-accent w-64"
        />
      </div>

      {/* Error */}
      {error && <ErrorBanner message={error} onDismiss={() => setError('')} />}

      {/* Table */}
      {loading ? (
        <div className="text-gray-400 text-center py-12">Loading...</div>
      ) : folders.length === 0 && files.length === 0 ? (
        <div className="text-gray-500 text-center py-12">No files or folders</div>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-dark-border">
          <table className="w-full text-sm text-left">
            <thead className="bg-dark-surface text-gray-400 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Size</th>
                <th className="px-4 py-3">Tags</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Modified</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border">
              {/* Folders */}
              {folders.map(folder => (
                <tr key={`folder-${folder.id}`} className="bg-dark-bg hover:bg-dark-hover transition-colors">
                  <td className="px-4 py-3">
                    <button
                      onClick={() => navigateToFolder(folder.id)}
                      className="flex items-center gap-2 text-white font-medium hover:text-accent transition-colors"
                    >
                      <FolderIcon className="text-yellow-400" />
                      {folder.name}
                    </button>
                  </td>
                  <td className="px-4 py-3 text-gray-400">Folder</td>
                  <td className="px-4 py-3 text-gray-400">-</td>
                  <td className="px-4 py-3 text-gray-400">-</td>
                  <td className="px-4 py-3 text-gray-400">-</td>
                  <td className="px-4 py-3 text-gray-400">
                    {new Date(folder.updated_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => openModal({ type: 'renameFolder', folder })}
                        className="p-1.5 text-gray-400 hover:text-white rounded hover:bg-dark-hover transition-colors"
                        title="Rename"
                      >
                        <EditIcon />
                      </button>
                      {folderDelete.isConfirming(folder.id) ? (
                        <ConfirmDialog
                          onConfirm={() => handleDeleteFolder(folder.id)}
                          onCancel={folderDelete.cancel}
                        />
                      ) : (
                        <button
                          onClick={() => folderDelete.requestDelete(folder.id)}
                          className="p-1.5 text-gray-400 hover:text-red-400 rounded hover:bg-dark-hover transition-colors"
                          title="Delete"
                        >
                          <TrashIcon />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}

              {/* Files */}
              {files.map(file => (
                <tr key={`file-${file.id}`} className="bg-dark-bg hover:bg-dark-hover transition-colors">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2 text-white font-medium">
                      <FileIcon mimeType={file.mime_type} />
                      {file.name}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-gray-400 text-xs">{file.mime_type}</td>
                  <td className="px-4 py-3 text-gray-400">{formatSize(file.size)}</td>
                  <td className="px-4 py-3">
                    <div className="flex flex-wrap gap-1">
                      {file.tags.slice(0, 3).map(tag => (
                        <span key={tag} className="inline-block px-1.5 py-0.5 rounded text-xs bg-accent/20 text-accent">
                          {tag}
                        </span>
                      ))}
                      {file.tags.length > 3 && (
                        <span className="text-xs text-gray-400">+{file.tags.length - 3}</span>
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge variant={fileStatusVariant(file.status)}>
                      {file.status}
                    </StatusBadge>
                  </td>
                  <td className="px-4 py-3 text-gray-400">
                    {new Date(file.updated_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex items-center justify-end gap-2">
                      {file.mime_type === 'application/pdf' && (
                        <button
                          onClick={() => openModal({ type: 'preview', file })}
                          className="p-1.5 text-gray-400 hover:text-white rounded hover:bg-dark-hover transition-colors"
                          title="Preview"
                        >
                          <EyeIcon />
                        </button>
                      )}
                      <button
                        onClick={() => openModal({ type: 'edit', file })}
                        className="p-1.5 text-gray-400 hover:text-white rounded hover:bg-dark-hover transition-colors"
                        title="Edit"
                      >
                        <EditIcon />
                      </button>
                      {fileDelete.isConfirming(file.id) ? (
                        <ConfirmDialog
                          onConfirm={() => handleDeleteFile(file.id)}
                          onCancel={fileDelete.cancel}
                        />
                      ) : (
                        <button
                          onClick={() => fileDelete.requestDelete(file.id)}
                          className="p-1.5 text-gray-400 hover:text-red-400 rounded hover:bg-dark-hover transition-colors"
                          title="Delete"
                        >
                          <TrashIcon />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Modals */}
      {modal.type === 'upload' && (
        <UploadModal
          folderId={currentFolderId}
          onClose={closeModal}
          onUploaded={handleModalSaved}
          onError={setError}
        />
      )}
      {modal.type === 'edit' && (
        <EditFileModal
          file={modal.file}
          onClose={closeModal}
          onSaved={handleModalSaved}
          onError={setError}
        />
      )}
      {modal.type === 'preview' && (
        <PreviewModal
          file={modal.file}
          onClose={closeModal}
        />
      )}
      {modal.type === 'newFolder' && (
        <FolderModal
          parentId={currentFolderId}
          onClose={closeModal}
          onSaved={handleModalSaved}
          onError={setError}
        />
      )}
      {modal.type === 'renameFolder' && (
        <FolderModal
          folder={modal.folder}
          parentId={currentFolderId}
          onClose={closeModal}
          onSaved={handleModalSaved}
          onError={setError}
        />
      )}
    </div>
  );
}
