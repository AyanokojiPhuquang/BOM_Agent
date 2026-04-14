import { useState } from 'react';
import { Button } from '@/components/common/Button';
import { Modal } from '@/components/common/Modal';
import { FormInput } from '@/components/common/FormInput';
import { TagInput } from '@/components/common/TagInput';
import { MetadataEditor } from '@/components/common/MetadataEditor';
import type { FileItem, UpdateFileData } from '@/services/files';
import * as filesService from '@/services/files';

interface EditFileModalProps {
  file: FileItem;
  onClose: () => void;
  onSaved: () => void;
  onError: (msg: string) => void;
}

export function EditFileModal({ file, onClose, onSaved, onError }: EditFileModalProps) {
  const [name, setName] = useState(file.name);
  const [tags, setTags] = useState<string[]>(file.tags);
  const [metadata, setMetadata] = useState<{ key: string; value: string }[]>(
    Object.entries(file.metadata).map(([key, value]) => ({ key, value }))
  );
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const meta: Record<string, string> = {};
      for (const { key, value } of metadata) {
        if (key.trim()) meta[key.trim()] = value;
      }
      const data: UpdateFileData = { name, tags, metadata: meta };
      await filesService.updateFile(file.id, data);
      onSaved();
    } catch {
      onError('Failed to update file');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal onClose={onClose} className="max-h-[90vh] overflow-y-auto">
      <h2 className="text-lg font-semibold text-white mb-4">Edit File</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <FormInput
          label="Name"
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />

        <div>
          <label className="block text-sm text-gray-400 mb-1">Original filename</label>
          <p className="text-sm text-gray-500">{file.original_name}</p>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">Tags</label>
          <TagInput tags={tags} onChange={setTags} />
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">Metadata</label>
          <MetadataEditor entries={metadata} onChange={setMetadata} />
        </div>

        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" type="button" onClick={onClose}>Cancel</Button>
          <Button type="submit" disabled={saving}>
            {saving ? 'Saving...' : 'Save'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
