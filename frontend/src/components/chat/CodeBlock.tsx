import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { COPY_FEEDBACK_MS } from '@/constants';
import { CheckIcon, CopyIcon } from '@/components/icons';

interface CodeBlockProps {
  language: string;
  code: string;
}

export function CodeBlock({ language, code }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  function handleCopy() {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), COPY_FEEDBACK_MS);
  }

  return (
    <div className="rounded-lg overflow-hidden my-3 bg-[#1e1e2e] border border-dark-border">
      <div className="flex items-center justify-between px-4 py-2 bg-dark-surface text-gray-400 text-xs">
        <span className="font-mono">{language}</span>
        <button
          onClick={handleCopy}
          className="hover:text-white transition-colors flex items-center gap-1"
        >
          {copied ? (
            <>
              <CheckIcon />
              Copied!
            </>
          ) : (
            <>
              <CopyIcon />
              Copy
            </>
          )}
        </button>
      </div>
      <SyntaxHighlighter
        language={language}
        style={oneDark}
        customStyle={{ margin: 0, padding: '1rem', background: 'transparent', fontSize: '0.875rem' }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}
