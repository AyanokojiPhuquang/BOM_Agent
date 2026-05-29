import { useState, useEffect, useCallback } from 'react';
import { listInstructions, addInstruction, deleteInstruction, resetPrompt, type UserInstruction } from '@/services/prompts';
import { cn } from '@/utils/cn';

export function PromptsContent() {
  const [instructions, setInstructions] = useState<UserInstruction[]>([]);
  const [newInstruction, setNewInstruction] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchInstructions = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await listInstructions();
      setInstructions(data.instructions);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load instructions');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => { fetchInstructions(); }, [fetchInstructions]);

  const handleAdd = async () => {
    if (!newInstruction.trim()) return;
    setIsProcessing(true);
    setMessage(null);
    setError(null);
    try {
      const result = await addInstruction(newInstruction.trim());
      setInstructions(prev => [...prev, result.instruction]);
      setNewInstruction('');
      setMessage(result.message);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to add instruction');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDelete = async (id: string) => {
    setIsProcessing(true);
    setMessage(null);
    setError(null);
    try {
      await deleteInstruction(id);
      setInstructions(prev => prev.filter(i => i.id !== id));
      setMessage('Instruction removed');
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to delete instruction');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = async () => {
    if (!confirm('Reset all custom instructions? The AI will revert to default behavior.')) return;
    setIsProcessing(true);
    setMessage(null);
    setError(null);
    try {
      await resetPrompt();
      setInstructions([]);
      setMessage('AI behavior reset to default');
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to reset');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white">AI Behavior Settings</h2>
        <p className="text-gray-400 mt-1">
          Add custom instructions to control how the AI responds. For example: greeting style, tone of voice, language preferences, or specific rules.
        </p>
      </div>

      {/* Messages */}
      {message && (
        <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm">
          {message}
        </div>
      )}
      {error && (
        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Processing indicator */}
      {isProcessing && (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-accent/10 border border-accent/20 text-accent text-sm">
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          AI is updating behavior settings...
        </div>
      )}

      {/* Add new instruction */}
      <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-3">Add Instruction</h3>
        <div className="flex gap-3">
          <textarea
            value={newInstruction}
            onChange={e => setNewInstruction(e.target.value)}
            placeholder="E.g.: Always greet the customer warmly in Vietnamese. Use formal tone. When listing products, always include the price if available."
            className="flex-1 px-4 py-3 rounded-lg bg-dark-bg border border-dark-border text-white text-sm placeholder-gray-500 focus:outline-none focus:border-accent resize-none"
            rows={3}
            disabled={isProcessing}
          />
          <button
            onClick={handleAdd}
            disabled={!newInstruction.trim() || isProcessing}
            className={cn(
              'px-6 py-3 rounded-lg text-sm font-medium transition-colors self-end',
              newInstruction.trim() && !isProcessing
                ? 'bg-accent text-white hover:bg-accent/90'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
            )}
          >
            Add
          </button>
        </div>
      </div>

      {/* Active instructions */}
      <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">
            Active Instructions ({instructions.length})
          </h3>
          {instructions.length > 0 && (
            <button
              onClick={handleReset}
              disabled={isProcessing}
              className="px-3 py-1.5 rounded-lg text-sm font-medium text-red-400 border border-red-400/30 hover:bg-red-400/10 transition-colors"
            >
              Reset All
            </button>
          )}
        </div>

        {instructions.length > 0 ? (
          <div className="space-y-3">
            {instructions.map(inst => (
              <div
                key={inst.id}
                className="flex items-start gap-3 p-4 rounded-lg bg-dark-bg border border-dark-border/50"
              >
                <div className="flex-1 text-sm text-gray-300 leading-relaxed">
                  {inst.content}
                </div>
                <button
                  onClick={() => handleDelete(inst.id)}
                  disabled={isProcessing}
                  className="flex-shrink-0 text-red-400 hover:text-red-300 text-xs px-2 py-1 rounded hover:bg-red-500/10 transition-colors"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p>No custom instructions yet.</p>
            <p className="text-xs mt-1">Add instructions above to customize AI behavior.</p>
          </div>
        )}
      </div>
    </div>
  );
}
