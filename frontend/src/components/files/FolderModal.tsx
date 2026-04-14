import { useState } from 'react';
import { Button } from '@/components/common/Button';
import { Modal } from '@/components/common/Modal';
import { FormInput } from '@/components/common/FormInput';
import type { FolderItem } from '@/services/files';
import * as filesService from '@/services/files';

interface FolderModalProps {
  folder?: FolderItem;
  parentId: string | null;
  onClose: () => void;
  onSaved: () => void;
  onError: (msg: string) => void;
}

export function FolderModal({ folder, parentId, onClose, onSaved, onError }: FolderModalProps) {
  const isRename = !!folder;
  const [name, setName] = useState(folder?.name ?? '');
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (isRename && folder) {
        await filesService.updateFolder(folder.id, name);
      } else {
        await filesService.createFolder(name, parentId);
      }
      onSaved();
    } catch {
      onError(isRename ? 'Failed to rename folder' : 'Failed to create folder');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal onClose={onClose} maxWidth="max-w-sm">
      <h2 className="text-lg font-semibold text-white mb-4">
        {isRename ? 'Rename Folder' : 'New Folder'}
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <FormInput
          label="Name"
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          required
          autoFocus
        />
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" type="button" onClick={onClose}>Cancel</Button>
          <Button type="submit" disabled={saving}>
            {saving ? 'Saving...' : isRename ? 'Rename' : 'Create'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
