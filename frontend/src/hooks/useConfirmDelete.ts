import { useState, useCallback } from 'react';

export function useConfirmDelete() {
  const [pendingId, setPendingId] = useState<string | null>(null);

  const requestDelete = useCallback((id: string) => setPendingId(id), []);
  const cancel = useCallback(() => setPendingId(null), []);
  const isConfirming = useCallback((id: string) => pendingId === id, [pendingId]);

  return { pendingId, requestDelete, cancel, isConfirming } as const;
}
