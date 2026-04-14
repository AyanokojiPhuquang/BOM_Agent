import { INPUT_CLASS } from '@/constants';
import { CloseIcon } from '@/components/icons';

interface MetadataEntry {
  key: string;
  value: string;
}

interface MetadataEditorProps {
  entries: MetadataEntry[];
  onChange: (entries: MetadataEntry[]) => void;
}

export function MetadataEditor({ entries, onChange }: MetadataEditorProps) {
  const updateEntry = (idx: number, field: 'key' | 'value', val: string) => {
    const next = [...entries];
    next[idx] = { ...next[idx], [field]: val };
    onChange(next);
  };

  const removeEntry = (idx: number) => {
    onChange(entries.filter((_, i) => i !== idx));
  };

  return (
    <div className="space-y-2">
      {entries.map((entry, idx) => (
        <div key={idx} className="flex items-center gap-2">
          <input
            type="text"
            value={entry.key}
            onChange={e => updateEntry(idx, 'key', e.target.value)}
            placeholder="Key"
            className={`flex-1 ${INPUT_CLASS}`}
          />
          <input
            type="text"
            value={entry.value}
            onChange={e => updateEntry(idx, 'value', e.target.value)}
            placeholder="Value"
            className={`flex-1 ${INPUT_CLASS}`}
          />
          <button
            type="button"
            onClick={() => removeEntry(idx)}
            className="p-1.5 text-gray-400 hover:text-red-400 rounded hover:bg-dark-hover transition-colors"
          >
            <CloseIcon />
          </button>
        </div>
      ))}
      <button
        type="button"
        onClick={() => onChange([...entries, { key: '', value: '' }])}
        className="text-sm text-accent hover:text-accent-hover transition-colors"
      >
        + Add metadata
      </button>
    </div>
  );
}
