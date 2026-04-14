import { useState } from 'react';
import { Button } from '@/components/common/Button';
import { Modal } from '@/components/common/Modal';
import { FormInput } from '@/components/common/FormInput';
import type { UserDetail, CreateUserData, UpdateUserData } from '@/services/users';
import * as usersService from '@/services/users';

type Mode = { type: 'create' } | { type: 'edit'; user: UserDetail };

interface UserFormModalProps {
  mode: Mode;
  onClose: () => void;
  onSaved: () => void;
  onError: (msg: string) => void;
}

export function UserFormModal({ mode, onClose, onSaved, onError }: UserFormModalProps) {
  const isEdit = mode.type === 'edit';
  const [name, setName] = useState(isEdit ? mode.user.name : '');
  const [email, setEmail] = useState(isEdit ? mode.user.email : '');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState(isEdit ? mode.user.role : 'user');
  const [isActive, setIsActive] = useState(isEdit ? mode.user.is_active : true);
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (isEdit) {
        const data: UpdateUserData = { name, email, role, is_active: isActive };
        if (password) data.password = password;
        await usersService.updateUser(mode.user.id, data);
      } else {
        const data: CreateUserData = { name, email, password, role };
        await usersService.createUser(data);
      }
      onSaved();
    } catch {
      onError(isEdit ? 'Failed to update user' : 'Failed to create user');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal onClose={onClose} maxWidth="max-w-md">
      <h2 className="text-lg font-semibold text-white mb-4">{isEdit ? 'Edit User' : 'Add User'}</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <FormInput
          label="Name"
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <FormInput
          label="Email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <FormInput
          label={`Password${isEdit ? ' (leave blank to keep current)' : ''}`}
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required={!isEdit}
        />
        <FormInput
          as="select"
          label="Role"
          value={role}
          onChange={e => setRole(e.target.value as 'user' | 'admin')}
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </FormInput>
        {isEdit && (
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="is_active"
              checked={isActive}
              onChange={e => setIsActive(e.target.checked)}
              className="rounded border-dark-border bg-dark-bg text-accent focus:ring-accent"
            />
            <label htmlFor="is_active" className="text-sm text-gray-400">Active</label>
          </div>
        )}
        <div className="flex justify-end gap-3 pt-2">
          <Button variant="ghost" type="button" onClick={onClose}>Cancel</Button>
          <Button type="submit" disabled={saving}>
            {saving ? 'Saving...' : isEdit ? 'Update' : 'Create'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
