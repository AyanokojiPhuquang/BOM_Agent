import { useState, useRef, useCallback, type KeyboardEvent } from 'react';
import type { ImageAttachment } from '@/types';
import { ImagePreview } from '@/components/common/ImagePreview';
import { generateId } from '@/utils/id';
import { cn } from '@/utils/cn';
import { AI_DISCLAIMER, TEXTAREA_MAX_HEIGHT } from '@/constants';
import { AttachIcon, StopIcon, SendIcon } from '@/components/icons';

interface ChatInputProps {
  onSend: (text: string, images: ImageAttachment[]) => void;
  disabled?: boolean;
  onStop?: () => void;
}

export function ChatInput({ onSend, disabled = false, onStop }: ChatInputProps) {
  const [text, setText] = useState('');
  const [attachments, setAttachments] = useState<ImageAttachment[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const autoResize = useCallback(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, TEXTAREA_MAX_HEIGHT) + 'px';
  }, []);

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function handleSend() {
    const trimmed = text.trim();
    if (!trimmed && attachments.length === 0) return;
    if (disabled) return;

    onSend(trimmed, attachments);
    setText('');
    setAttachments([]);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  }

  function handleImageSelect(e: React.ChangeEvent<HTMLInputElement>) {
    const files = e.target.files;
    if (!files) return;

    Array.from(files).forEach(file => {
      const reader = new FileReader();
      reader.onload = (ev) => {
        setAttachments(prev => [
          ...prev,
          {
            id: generateId(),
            dataUrl: ev.target!.result as string,
            name: file.name,
            size: file.size,
          },
        ]);
      };
      reader.readAsDataURL(file);
    });

    // Reset file input
    e.target.value = '';
  }

  function removeAttachment(id: string) {
    setAttachments(prev => prev.filter(a => a.id !== id));
  }

  const canSend = (text.trim() || attachments.length > 0) && !disabled;

  return (
    <div className="border-t border-dark-border bg-dark-bg p-4">
      <div className="max-w-3xl mx-auto">
        <div className="bg-dark-surface rounded-2xl border border-dark-border overflow-hidden">
          <ImagePreview images={attachments} onRemove={removeAttachment} />

          <div className="flex items-end gap-2 p-3">
            {/* Attach button */}
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex-shrink-0 p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-dark-hover"
              disabled={disabled}
            >
              <AttachIcon />
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={handleImageSelect}
              className="hidden"
            />

            {/* Textarea */}
            <textarea
              ref={textareaRef}
              value={text}
              onChange={e => { setText(e.target.value); autoResize(); }}
              onKeyDown={handleKeyDown}
              placeholder="Type a message..."
              rows={1}
              className="flex-1 bg-transparent text-white placeholder-gray-500 focus:outline-none text-sm leading-6 py-2"
              disabled={disabled}
            />

            {/* Send / Stop button */}
            {disabled && onStop ? (
              <button
                onClick={onStop}
                className="flex-shrink-0 p-2 bg-red-500/20 text-red-400 hover:bg-red-500/30 rounded-lg transition-colors"
              >
                <StopIcon />
              </button>
            ) : (
              <button
                onClick={handleSend}
                disabled={!canSend}
                className={cn(
                  'flex-shrink-0 p-2 rounded-lg transition-colors',
                  canSend
                    ? 'bg-accent text-white hover:bg-accent-hover'
                    : 'text-gray-500 cursor-not-allowed'
                )}
              >
                <SendIcon />
              </button>
            )}
          </div>
        </div>
        <p className="text-xs text-gray-500 text-center mt-2">{AI_DISCLAIMER}</p>
      </div>
    </div>
  );
}
