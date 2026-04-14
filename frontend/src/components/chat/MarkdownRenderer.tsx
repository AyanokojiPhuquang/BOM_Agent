import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { CodeBlock } from './CodeBlock';
import { ImageLightbox } from '@/components/common/ImageLightbox';

const DATASHEETS_PREFIX = '/api/files/datasheets';

/**
 * Rewrite datasheet-relative image paths (e.g. /AOC/...) to the
 * backend static file endpoint so they resolve in the browser.
 * Uses relative paths so the Vite proxy (dev) or reverse proxy (prod) handles routing.
 */
function transformImageUrl(src: string): string {
  if (src.startsWith(DATASHEETS_PREFIX) || src.startsWith('http')) {
    return src;
  }
  // Paths starting with / that aren't already prefixed are datasheet-relative
  if (src.startsWith('/')) {
    return `${DATASHEETS_PREFIX}${src}`;
  }
  return src;
}

/**
 * Encode spaces in markdown image URLs so the parser can handle paths
 * with spaces (e.g. `/SFP/SFP-10G-T /file.png` → `/SFP/SFP-10G-T%20/file.png`).
 */
function fixImageUrls(markdown: string): string {
  return markdown.replace(
    /!\[([^\]]*)\]\(([^)]+)\)/g,
    (_, alt, url) => `![${alt}](${url.replace(/ /g, '%20')})`,
  );
}

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  return (
    <div className="break-words overflow-hidden">
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        img: ({ src, alt }) => (
          <ImageLightbox
            src={src ? transformImageUrl(src) : ''}
            alt={alt ?? ''}
            className="max-w-full h-auto rounded my-2"
          />
        ),
        code({ className, children, ...props }) {
          const match = /language-(\w+)/.exec(className ?? '');
          const codeString = String(children).replace(/\n$/, '');

          if (match && codeString.includes('\n')) {
            return <CodeBlock language={match[1]} code={codeString} />;
          }

          return (
            <code className="bg-dark-hover text-green-400 px-1.5 py-0.5 rounded text-sm font-mono break-all" {...props}>
              {children}
            </code>
          );
        },
        p: ({ children }) => <p className="mb-3 last:mb-0 leading-7">{children}</p>,
        ul: ({ children }) => <ul className="list-disc pl-6 mb-3 space-y-1">{children}</ul>,
        ol: ({ children }) => <ol className="list-decimal pl-6 mb-3 space-y-1">{children}</ol>,
        li: ({ children }) => <li className="leading-7">{children}</li>,
        h1: ({ children }) => <h1 className="text-2xl font-bold mt-6 mb-3">{children}</h1>,
        h2: ({ children }) => <h2 className="text-xl font-bold mt-5 mb-2">{children}</h2>,
        h3: ({ children }) => <h3 className="text-lg font-semibold mt-4 mb-2">{children}</h3>,
        blockquote: ({ children }) => (
          <blockquote className="border-l-4 border-gray-500 pl-4 italic text-gray-300 my-3">
            {children}
          </blockquote>
        ),
        table: ({ children }) => (
          <div className="overflow-x-auto mb-3">
            <table className="min-w-full border-collapse border border-dark-border">
              {children}
            </table>
          </div>
        ),
        th: ({ children }) => (
          <th className="border border-dark-border px-3 py-2 bg-dark-surface font-semibold text-left">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="border border-dark-border px-3 py-2">{children}</td>
        ),
        strong: ({ children }) => <strong className="font-bold text-white">{children}</strong>,
        a: ({ href, children }) => {
          // Render image links (e.g. [Image](/path/to/image.png)) as <img> tags
          if (href && /\.(png|jpe?g|gif|webp|svg)$/i.test(href)) {
            const alt = typeof children === 'string' ? children : 'Image';
            return (
              <ImageLightbox
                src={transformImageUrl(href)}
                alt={alt}
                className="max-w-full h-auto rounded my-2"
              />
            );
          }
          // Render .xlsx links as download buttons
          if (href && /\.xlsx$/i.test(href)) {
            return (
              <a
                href={href}
                download
                className="inline-block px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded transition-colors no-underline"
              >
                {children}
              </a>
            );
          }
          return (
            <a href={href} className="text-blue-400 hover:text-blue-300 underline break-all" target="_blank" rel="noopener noreferrer">
              {children}
            </a>
          );
        },
      }}
    >
      {fixImageUrls(content)}
    </ReactMarkdown>
    </div>
  );
}
