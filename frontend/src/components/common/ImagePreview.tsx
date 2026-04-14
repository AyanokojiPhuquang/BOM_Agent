import type { ImageAttachment } from '@/types';

interface ImagePreviewProps {
  images: ImageAttachment[];
  onRemove: (id: string) => void;
}

export function ImagePreview({ images, onRemove }: ImagePreviewProps) {
  if (images.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 p-2 pb-0">
      {images.map(img => (
        <div key={img.id} className="relative group">
          <img
            src={img.dataUrl}
            alt={img.name}
            className="h-16 w-16 rounded-lg object-cover border border-dark-border"
          />
          <button
            onClick={() => onRemove(img.id)}
            className="absolute -top-1.5 -right-1.5 w-5 h-5 bg-red-500 text-white rounded-full text-xs flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
