import { useState, useRef } from 'react';
import { Button } from '@/components/common/Button';
import { Modal } from '@/components/common/Modal';
import { TagInput } from '@/components/common/TagInput';
import { MetadataEditor } from '@/components/common/MetadataEditor';
import { formatSize } from '@/utils/format';
import { cn } from '@/utils/cn';
import * as filesService from '@/services/files';

interface UploadModalProps {
  folderId: string | null;
  onClose: () => void;
  onUploaded: () => void;
  onError: (msg: string) => void;
}

export function UploadModal({ folderId, onClose, onUploaded, onError }: UploadModalProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [tags, setTags] = useState<string[]>([]);
  const [metadata, setMetadata] = useState<{ key: string; value: string }[]>([]);
  const [saving, setSaving] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const addFiles = (newFiles: FileList | File[]) => {
    const arr = Array.from(newFiles);
    setFiles(prev => {
      const existing = new Set(prev.map(f => `${f.name}-${f.size}`));
      return [...prev, ...arr.filter(f => !existing.has(`${f.name}-${f.size}`))];
    });
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files.length) addFiles(e.dataTransfer.files);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (files.length === 0) return;
    setSaving(true);
    try {
      const meta: Record<string, string> = {};
      for (const { key, value } of metadata) {
        if (key.trim()) meta[key.trim()] = value;
      }
      for (const file of files) {
        await filesService.uploadFile(file, folderId, tags, meta);
      }
      onUploaded();
    } catch {
      onError('Failed to upload files');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal onClose={onClose} className="max-h-[90vh] overflow-y-auto">
      <h2 className="text-lg font-semibold text-white mb-4">Upload Files</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Drop zone */}
        <div
          className={cn(
            'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
            dragOver ? 'border-accent bg-accent/5' : 'border-dark-border hover:border-gray-500',
          )}
          onDragOver={e => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            onChange={e => { if (e.target.files?.length) { addFiles(e.target.files); e.target.value = ''; } }}
            className="hidden"
          />
          <div className="text-gray-400">
            <p>Drop files here or click to browse</p>
          </div>
        </div>

        {/* Selected files list */}
        {files.length > 0 && (
          <div className="max-h-40 overflow-y-auto rounded-lg border border-dark-border divide-y divide-dark-border">
            {files.map((file, i) => (
              <div key={`${file.name}-${file.size}`} className="flex items-center justify-between px-3 py-2 text-sm">
                <div className="text-white truncate mr-2">
                  <span className="font-medium">{file.name}</span>
                  <span className="text-gray-400 ml-2">{formatSize(file.size)}</span>
                </div>
                <button
                  type="button"
                  onClick={() => removeFile(i)}
                  className="text-gray-400 hover:text-red-400 shrink-0"
                  title="Remove"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Tags */}
        <div>
          <label className="block text-sm text-gray-400 mb-1">Tags</label>
          <TagInput tags={tags} onChange={setTags} />
        </div>

        {/* Metadata */}
        <div>
          <label className="block text-sm text-gray-400 mb-1">Metadata</label>
          <MetadataEditor entries={metadata} onChange={setMetadata} />
        </div>

        {/* Info note */}
        {files.length > 1 && (
          <p className="text-xs text-gray-400 italic">
            Tags and metadata will be applied to all selected files.
          </p>
        )}

        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" type="button" onClick={onClose}>Cancel</Button>
          <Button type="submit" disabled={saving || files.length === 0}>
            {saving ? 'Uploading...' : files.length > 1 ? `Upload ${files.length} Files` : 'Upload'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
