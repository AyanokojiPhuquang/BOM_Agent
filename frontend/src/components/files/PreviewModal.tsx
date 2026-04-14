import { useEffect, useState } from 'react';
import { Modal } from '@/components/common/Modal';
import { getToken } from '@/services/api';
import type { FileItem } from '@/services/files';
import * as filesService from '@/services/files';

interface PreviewModalProps {
  file: FileItem;
  onClose: () => void;
}

export function PreviewModal({ file, onClose }: PreviewModalProps) {
  const [blobUrl, setBlobUrl] = useState<string | null>(null);
  const [loadError, setLoadError] = useState(false);

  useEffect(() => {
    let revoked = false;
    const token = getToken();
    fetch(filesService.getFileDownloadUrl(file.id), {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to load');
        return res.blob();
      })
      .then(blob => {
        if (revoked) return;
        setBlobUrl(URL.createObjectURL(blob));
      })
      .catch(() => setLoadError(true));

    return () => {
      revoked = true;
      if (blobUrl) URL.revokeObjectURL(blobUrl);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [file.id]);

  return (
    <Modal onClose={onClose} maxWidth="max-w-4xl" className="h-[85vh] flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">{file.original_name}</h2>
        <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors text-xl">&times;</button>
      </div>
      <div className="flex-1 rounded-lg overflow-hidden bg-dark-bg">
        {loadError ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            Failed to load preview
          </div>
        ) : blobUrl ? (
          <iframe src={blobUrl} className="w-full h-full" title="PDF Preview" />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            Loading preview...
          </div>
        )}
      </div>
    </Modal>
  );
}
