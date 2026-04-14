import { useState, useCallback } from 'react';

type Closed = { type: 'closed' };

export function useModal<T extends { type: string }>() {
  const [modal, setModal] = useState<T | Closed>({ type: 'closed' });

  const open = useCallback((m: T) => setModal(m), []);
  const close = useCallback(() => setModal({ type: 'closed' }), []);

  return { modal, open, close } as const;
}
