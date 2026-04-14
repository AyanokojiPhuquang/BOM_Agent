import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/common/Button';
import { ErrorBanner } from '@/components/common/ErrorBanner';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { StatusBadge } from '@/components/common/StatusBadge';
import { BackArrowIcon, EditIcon, TrashIcon } from '@/components/icons';
import { UserFormModal } from '@/components/users/UserFormModal';
import { useModal } from '@/hooks/useModal';
import { useConfirmDelete } from '@/hooks/useConfirmDelete';
import type { UserDetail } from '@/services/users';
import * as usersService from '@/services/users';

type ModalMode = { type: 'create' } | { type: 'edit'; user: UserDetail };

/** Standalone page (kept for backward compat, redirects handled by router) */
export function UserManagementPage() {
  const navigate = useNavigate();
  return (
    <div className="h-screen bg-dark-bg flex flex-col">
      <header className="flex items-center justify-between px-6 py-4 border-b border-dark-border bg-dark-surface">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/chat')}
            className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-dark-hover transition-colors"
          >
            <BackArrowIcon />
          </button>
          <h1 className="text-xl font-semibold text-white">User Management</h1>
        </div>
      </header>
      <div className="flex-1 overflow-auto">
        <UserManagementContent />
      </div>
    </div>
  );
}

/** Embeddable content used by AdminSettingsPage tabs */
export function UserManagementContent() {
  const [users, setUsers] = useState<UserDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const { modal, open: openModal, close: closeModal } = useModal<ModalMode>();
  const deleteConfirm = useConfirmDelete();

  const fetchUsers = useCallback(async () => {
    try {
      const data = await usersService.listUsers();
      setUsers(data.items);
    } catch {
      setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchUsers(); }, [fetchUsers]);

  const handleDelete = async (id: string) => {
    try {
      await usersService.deleteUser(id);
      setUsers(prev => prev.filter(u => u.id !== id));
      deleteConfirm.cancel();
    } catch {
      setError('Failed to delete user');
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">User Management</h2>
        <Button onClick={() => openModal({ type: 'create' })}>Add User</Button>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError('')} />}

      {loading ? (
        <div className="text-gray-400 text-center py-12">Loading...</div>
      ) : users.length === 0 ? (
        <div className="text-gray-500 text-center py-12">No users found</div>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-dark-border">
          <table className="w-full text-sm text-left">
            <thead className="bg-dark-surface text-gray-400 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Email</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Created</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border">
              {users.map(user => (
                <tr key={user.id} className="bg-dark-bg hover:bg-dark-hover transition-colors">
                  <td className="px-4 py-3 text-white font-medium">{user.name}</td>
                  <td className="px-4 py-3 text-gray-300">{user.email}</td>
                  <td className="px-4 py-3">
                    <StatusBadge variant={user.role === 'admin' ? 'info' : 'neutral'}>
                      {user.role}
                    </StatusBadge>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge variant={user.is_active ? 'success' : 'error'}>
                      {user.is_active ? 'Active' : 'Inactive'}
                    </StatusBadge>
                  </td>
                  <td className="px-4 py-3 text-gray-400">
                    {new Date(user.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => openModal({ type: 'edit', user })}
                        className="p-1.5 text-gray-400 hover:text-white rounded hover:bg-dark-hover transition-colors"
                        title="Edit"
                      >
                        <EditIcon />
                      </button>
                      {deleteConfirm.isConfirming(user.id) ? (
                        <ConfirmDialog
                          onConfirm={() => handleDelete(user.id)}
                          onCancel={deleteConfirm.cancel}
                        />
                      ) : (
                        <button
                          onClick={() => deleteConfirm.requestDelete(user.id)}
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

      {/* Modal */}
      {modal.type !== 'closed' && (
        <UserFormModal
          mode={modal as ModalMode}
          onClose={closeModal}
          onSaved={() => { closeModal(); fetchUsers(); }}
          onError={setError}
        />
      )}
    </div>
  );
}
