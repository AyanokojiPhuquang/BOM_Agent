import { useState, useEffect, useCallback } from 'react';
import { listPrompts, updatePrompt, revertPrompt, type PromptItem } from '@/services/prompts';
import { cn } from '@/utils/cn';

export function PromptsContent() {
  const [prompts, setPrompts] = useState<PromptItem[]>([]);
  const [selected, setSelected] = useState<PromptItem | null>(null);
  const [editContent, setEditContent] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchPrompts = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await listPrompts();
      setPrompts(data.prompts);
      if (data.prompts.length > 0 && !selected) {
        setSelected(data.prompts[0]);
        setEditContent(data.prompts[0].content);
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load prompts');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => { fetchPrompts(); }, [fetchPrompts]);

  const handleSelect = (prompt: PromptItem) => {
    setSelected(prompt);
    setEditContent(prompt.content);
    setMessage(null);
    setError(null);
  };

  const handleSave = async () => {
    if (!selected) return;
    setIsSaving(true);
    setMessage(null);
    setError(null);
    try {
      const updated = await updatePrompt(selected.path, editContent);
      setSelected(updated);
      setPrompts(prev => prev.map(p => p.path === updated.path ? updated : p));
      setMessage('Prompt saved successfully!');
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to save');
    } finally {
      setIsSaving(false);
    }
  };

  const handleRevert = async () => {
    if (!selected) return;
    if (!confirm('Revert this prompt to the original version? Your changes will be lost.')) return;
    setIsSaving(true);
    setMessage(null);
    setError(null);
    try {
      const reverted = await revertPrompt(selected.path);
      setSelected(reverted);
      setEditContent(reverted.content);
      setPrompts(prev => prev.map(p => p.path === reverted.path ? reverted : p));
      setMessage('Prompt reverted to original!');
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to revert');
    } finally {
      setIsSaving(false);
    }
  };

  const hasChanges = selected && editContent !== selected.content;

  const categories = [...new Set(prompts.map(p => p.category))];

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Prompt Management</h2>
        <p className="text-gray-400 mt-1">View and edit agent prompts. Changes take effect immediately.</p>
      </div>

      {message && (
        <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm">{message}</div>
      )}
      {error && (
        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
      )}

      <div className="flex gap-4 h-[70vh]">
        {/* Sidebar - prompt list */}
        <div className="w-64 flex-shrink-0 bg-dark-surface border border-dark-border rounded-xl overflow-auto">
          {categories.map(cat => (
            <div key={cat}>
              <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase">{cat}</div>
              {prompts.filter(p => p.category === cat).map(prompt => (
                <button
                  key={prompt.path}
                  onClick={() => handleSelect(prompt)}
                  className={cn(
                    'w-full text-left px-3 py-2 text-sm transition-colors',
                    selected?.path === prompt.path
                      ? 'bg-accent/15 text-accent'
                      : 'text-gray-300 hover:bg-dark-hover'
                  )}
                >
                  {prompt.name}
                </button>
              ))}
            </div>
          ))}
        </div>

        {/* Editor */}
        <div className="flex-1 flex flex-col bg-dark-surface border border-dark-border rounded-xl overflow-hidden">
          {selected ? (
            <>
              <div className="flex items-center justify-between px-4 py-3 border-b border-dark-border">
                <div className="flex items-center gap-2">
                <div>
                  <span className="text-white font-medium">{selected.name}</span>
                  <span className="text-gray-500 text-xs ml-2">{selected.path}</span>
                  {selected.is_modified && <span className="text-yellow-400 text-xs ml-2">(modified)</span>}
                </div>
              </div>
              <div className="flex items-center gap-2">
                {selected.has_original && selected.is_modified && (
                  <button
                    onClick={handleRevert}
                    disabled={isSaving}
                    className="px-3 py-1.5 rounded-lg text-sm font-medium text-yellow-400 border border-yellow-400/30 hover:bg-yellow-400/10 transition-colors"
                  >
                    Revert
                  </button>
                )}
                <button
                  onClick={handleSave}
                  disabled={!hasChanges || isSaving}
                  className={cn(
                    'px-4 py-1.5 rounded-lg text-sm font-medium transition-colors',
                    hasChanges
                      ? 'bg-accent text-white hover:bg-accent/90'
                      : 'bg-gray-600 text-gray-400 cursor-not-allowed'
                  )}
                >
                  {isSaving ? 'Saving...' : 'Save'}
                </button>
              </div>
              </div>
              <textarea
                value={editContent}
                onChange={e => setEditContent(e.target.value)}
                className="flex-1 p-4 bg-dark-bg text-gray-200 text-sm font-mono leading-6 resize-none focus:outline-none"
                spellCheck={false}
              />
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-gray-500">
              Select a prompt to edit
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
