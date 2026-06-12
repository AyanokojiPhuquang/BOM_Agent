import { useState, useEffect, useCallback } from 'react';
import { cn } from '@/utils/cn';
import { useDriveSyncWS } from '@/hooks/useDriveSyncWS';
import {
  getAuthUrl,
  getAuthStatus,
  disconnectDrive,
  startSync,
  getJobs,
  retryFailed,
  listDriveFolders,
  type AuthStatus,
  type BatchJob,
  type DriveFolder,
} from '@/services/driveSync';

export function DriveSyncContent() {
  const [authStatus, setAuthStatus] = useState<AuthStatus | null>(null);
  const [isLoadingAuth, setIsLoadingAuth] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Folder picker state
  const [folderId, setFolderId] = useState('');
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState<string | null>(null);
  const [folders, setFolders] = useState<DriveFolder[]>([]);
  const [folderPath, setFolderPath] = useState<{ id: string; name: string }[]>([{ id: 'root', name: 'My Drive' }]);
  const [isLoadingFolders, setIsLoadingFolders] = useState(false);

  // Job history
  const [jobs, setJobs] = useState<BatchJob[]>([]);
  const [isLoadingJobs, setIsLoadingJobs] = useState(false);

  // WebSocket progress
  const { progress, lastEvent, isConnected: wsConnected } = useDriveSyncWS();

  // Auto-dismiss messages
  useEffect(() => {
    if (successMsg) {
      const t = setTimeout(() => setSuccessMsg(null), 4000);
      return () => clearTimeout(t);
    }
  }, [successMsg]);

  const fetchAuthStatus = useCallback(async () => {
    setIsLoadingAuth(true);
    try {
      const status = await getAuthStatus();
      setAuthStatus(status);
    } catch {
      setAuthStatus({ connected: false, google_email: null });
    } finally {
      setIsLoadingAuth(false);
    }
  }, []);

  const fetchJobs = useCallback(async () => {
    setIsLoadingJobs(true);
    try {
      const data = await getJobs();
      setJobs(data);
    } catch {
      // silently fail
    } finally {
      setIsLoadingJobs(false);
    }
  }, []);

  useEffect(() => {
    fetchAuthStatus();
    fetchJobs();
  }, [fetchAuthStatus, fetchJobs]);

  // Load root folders when connected
  useEffect(() => {
    if (authStatus?.connected) {
      loadFolders('root');
    }
  }, [authStatus?.connected]);

  const loadFolders = async (parentId: string) => {
    setIsLoadingFolders(true);
    try {
      const data = await listDriveFolders(parentId);
      setFolders(data.folders);
    } catch {
      setFolders([]);
    } finally {
      setIsLoadingFolders(false);
    }
  };

  const navigateToFolder = (folder: DriveFolder) => {
    setFolderPath(prev => [...prev, { id: folder.id, name: folder.name }]);
    setFolderId(folder.id);
    loadFolders(folder.id);
  };

  const navigateToBreadcrumb = (index: number) => {
    const target = folderPath[index];
    setFolderPath(prev => prev.slice(0, index + 1));
    setFolderId(index === 0 ? '' : target.id);
    loadFolders(target.id);
  };

  // Refresh jobs when batch completes
  useEffect(() => {
    if (lastEvent?.type === 'batch_complete') {
      fetchJobs();
      setSyncMessage(null);
    }
  }, [lastEvent, fetchJobs]);

  const handleConnect = async () => {
    setError(null);
    try {
      const { url } = await getAuthUrl();
      window.location.href = url;
    } catch {
      setError('Failed to get authorization URL');
    }
  };

  const handleDisconnect = async () => {
    setError(null);
    try {
      await disconnectDrive();
      setAuthStatus({ connected: false, google_email: null });
      setSuccessMsg('Google Drive disconnected');
    } catch {
      setError('Failed to disconnect');
    }
  };

  const handleStartSync = async () => {
    if (!folderId.trim()) return;
    setError(null);
    setSyncMessage(null);
    setIsSyncing(true);
    try {
      const result = await startSync(folderId.trim());
      setSyncMessage(result.message);
      setSuccessMsg(`Sync started: ${result.total_files} file(s) queued`);
      fetchJobs();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Sync failed');
    } finally {
      setIsSyncing(false);
    }
  };

  const handleRetryFailed = async (jobId: string) => {
    setError(null);
    try {
      const result = await retryFailed(jobId);
      setSuccessMsg(result.message);
      fetchJobs();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Retry failed');
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Google Drive Sync</h2>
        <p className="text-sm text-gray-400 mt-1">
          Connect Google Drive and bulk-import PDF datasheets into the product catalog.
        </p>
      </div>

      {/* Messages */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-300 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}
      {successMsg && (
        <div className="bg-green-500/10 border border-green-500/30 text-green-300 px-4 py-3 rounded-lg text-sm">
          {successMsg}
        </div>
      )}

      {/* Google Connection Card */}
      <div className="bg-dark-surface border border-dark-border rounded-xl p-5">
        <h3 className="text-sm font-semibold text-white mb-3">Google Drive Connection</h3>
        {isLoadingAuth ? (
          <p className="text-sm text-gray-500">Checking connection...</p>
        ) : authStatus?.connected ? (
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-2.5 h-2.5 rounded-full bg-green-400" />
              <div>
                <p className="text-sm text-white">Connected</p>
                {authStatus.google_email && (
                  <p className="text-xs text-gray-400">{authStatus.google_email}</p>
                )}
              </div>
            </div>
            <button
              onClick={handleDisconnect}
              className="px-3 py-1.5 text-sm text-red-400 border border-red-500/30 rounded-lg hover:bg-red-500/10 transition-colors"
            >
              Disconnect
            </button>
          </div>
        ) : (
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-400">No Google account connected</p>
            <button
              onClick={handleConnect}
              className="px-4 py-2 text-sm font-medium text-white bg-accent rounded-lg hover:bg-accent-hover transition-colors"
            >
              Connect Google Drive
            </button>
          </div>
        )}
      </div>

      {/* Folder Picker */}
      {authStatus?.connected && (
        <div className="bg-dark-surface border border-dark-border rounded-xl p-5">
          <h3 className="text-sm font-semibold text-white mb-3">Select Folder & Start Sync</h3>

          {/* Breadcrumb */}
          <div className="flex items-center gap-1 mb-3 text-xs text-gray-400 flex-wrap">
            {folderPath.map((item, i) => (
              <span key={item.id} className="flex items-center gap-1">
                {i > 0 && <span className="text-gray-600">/</span>}
                <button
                  onClick={() => navigateToBreadcrumb(i)}
                  className="hover:text-white transition-colors"
                >
                  {item.name}
                </button>
              </span>
            ))}
          </div>

          {/* Folder list */}
          <div className="border border-dark-border rounded-lg max-h-48 overflow-y-auto mb-3">
            {isLoadingFolders ? (
              <p className="text-sm text-gray-500 p-3">Loading folders...</p>
            ) : folders.length === 0 ? (
              <p className="text-sm text-gray-500 p-3">No subfolders found.</p>
            ) : (
              <div className="divide-y divide-dark-border">
                {folders.map(folder => (
                  <button
                    key={folder.id}
                    onClick={() => navigateToFolder(folder)}
                    className={cn(
                      'w-full flex items-center gap-2 px-3 py-2 text-left text-sm hover:bg-dark-hover transition-colors',
                      folderId === folder.id ? 'bg-accent/10 text-accent' : 'text-gray-300'
                    )}
                  >
                    <svg className="w-4 h-4 flex-shrink-0 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" />
                    </svg>
                    <span className="truncate">{folder.name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Selected folder + Sync button */}
          <div className="flex items-center gap-3">
            <div className="flex-1 px-3 py-2 bg-dark-bg border border-dark-border rounded-lg text-sm">
              {folderId ? (
                <span className="text-white">Selected: <span className="text-accent font-mono">{folderPath[folderPath.length - 1]?.name || folderId}</span></span>
              ) : (
                <span className="text-gray-500">Navigate and select a folder above</span>
              )}
            </div>
            <button
              onClick={handleStartSync}
              disabled={isSyncing || !folderId.trim()}
              className="px-4 py-2 text-sm font-medium text-white bg-accent rounded-lg hover:bg-accent-hover transition-colors disabled:opacity-50 whitespace-nowrap"
            >
              {isSyncing ? 'Starting...' : 'Start Sync'}
            </button>
          </div>
          {syncMessage && (
            <p className="text-xs text-gray-400 mt-2">{syncMessage}</p>
          )}
        </div>
      )}

      {/* Progress Bar */}
      {progress && (
        <div className="bg-dark-surface border border-dark-border rounded-xl p-5">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-semibold text-white">Sync Progress</h3>
            <div className="flex items-center gap-2">
              <div className={cn('w-2 h-2 rounded-full', wsConnected ? 'bg-green-400' : 'bg-yellow-400')} />
              <span className="text-xs text-gray-400">{wsConnected ? 'Live' : 'Reconnecting...'}</span>
            </div>
          </div>
          <div className="w-full bg-dark-bg rounded-full h-3 overflow-hidden">
            <div
              className="h-full bg-accent rounded-full transition-all duration-300"
              style={{ width: `${progress.total > 0 ? ((progress.completed + progress.failed) / progress.total) * 100 : 0}%` }}
            />
          </div>
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
            <span>{progress.completed} completed</span>
            {progress.failed > 0 && <span className="text-red-400">{progress.failed} failed</span>}
            <span>{progress.total} total</span>
          </div>
        </div>
      )}

      {/* Job History */}
      <div className="bg-dark-surface border border-dark-border rounded-xl p-5">
        <h3 className="text-sm font-semibold text-white mb-3">Sync History</h3>
        {isLoadingJobs ? (
          <p className="text-sm text-gray-500">Loading...</p>
        ) : jobs.length === 0 ? (
          <p className="text-sm text-gray-500">No sync jobs yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-dark-border">
                  <th className="px-3 py-2 text-left text-xs font-semibold text-gray-400 uppercase">Date</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-gray-400 uppercase">Folder</th>
                  <th className="px-3 py-2 text-left text-xs font-semibold text-gray-400 uppercase">Status</th>
                  <th className="px-3 py-2 text-right text-xs font-semibold text-gray-400 uppercase">Files</th>
                  <th className="px-3 py-2 text-right text-xs font-semibold text-gray-400 uppercase">Done</th>
                  <th className="px-3 py-2 text-right text-xs font-semibold text-gray-400 uppercase">Failed</th>
                  <th className="px-3 py-2 text-right text-xs font-semibold text-gray-400 uppercase">Skipped</th>
                  <th className="px-3 py-2 text-right text-xs font-semibold text-gray-400 uppercase">Products</th>
                  <th className="px-3 py-2 text-right text-xs font-semibold text-gray-400 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-border">
                {jobs.map((job) => (
                  <tr key={job.id} className="hover:bg-dark-hover transition-colors">
                    <td className="px-3 py-2 text-gray-300 whitespace-nowrap">
                      {new Date(job.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-3 py-2 text-gray-300 font-mono text-xs truncate max-w-[120px]" title={job.folder_id}>
                      {job.folder_id}
                    </td>
                    <td className="px-3 py-2">
                      <span className={cn(
                        'px-2 py-0.5 rounded text-xs font-medium',
                        job.status === 'completed' && 'bg-green-500/15 text-green-400',
                        job.status === 'processing' && 'bg-blue-500/15 text-blue-400',
                        job.status === 'failed' && 'bg-red-500/15 text-red-400',
                      )}>
                        {job.status}
                      </span>
                    </td>
                    <td className="px-3 py-2 text-right text-gray-300">{job.total_files}</td>
                    <td className="px-3 py-2 text-right text-gray-300">{job.completed_count}</td>
                    <td className="px-3 py-2 text-right text-gray-300">{job.failed_count}</td>
                    <td className="px-3 py-2 text-right text-gray-300">{job.skipped_count}</td>
                    <td className="px-3 py-2 text-right text-gray-300">{job.products_extracted}</td>
                    <td className="px-3 py-2 text-right">
                      {job.failed_count > 0 && job.status === 'completed' && (
                        <button
                          onClick={() => handleRetryFailed(job.id)}
                          className="text-xs text-accent hover:text-accent-hover transition-colors"
                        >
                          Retry Failed
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
