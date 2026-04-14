import { useEffect, type ReactNode } from 'react';
import { cn } from '@/utils/cn';
import { Z_INDEX } from '@/constants';

interface ModalProps {
  onClose: () => void;
  maxWidth?: string;
  className?: string;
  children: ReactNode;
}

export function Modal({ onClose, maxWidth = 'max-w-lg', className, children }: ModalProps) {
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose();
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 flex items-center justify-center bg-black/60"
      style={{ zIndex: Z_INDEX.MODAL }}
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className={cn(
          'bg-dark-surface border border-dark-border rounded-xl w-full mx-4 p-6',
          maxWidth,
          className,
        )}
        onClick={e => e.stopPropagation()}
      >
        {children}
      </div>
    </div>
  );
}
