interface ConfirmDialogProps {
  onConfirm: () => void;
  onCancel: () => void;
  confirmLabel?: string;
}

export function ConfirmDialog({ onConfirm, onCancel, confirmLabel = 'Confirm' }: ConfirmDialogProps) {
  return (
    <div className="flex items-center gap-1">
      <button
        onClick={onConfirm}
        className="px-2 py-1 text-xs bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 transition-colors"
      >
        {confirmLabel}
      </button>
      <button
        onClick={onCancel}
        className="px-2 py-1 text-xs text-gray-400 rounded hover:bg-dark-hover transition-colors"
      >
        Cancel
      </button>
    </div>
  );
}
