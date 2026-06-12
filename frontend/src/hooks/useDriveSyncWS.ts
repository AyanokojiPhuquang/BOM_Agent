import { useState, useEffect, useRef, useCallback } from 'react';
import { getToken } from '@/services/api';
import type { WSEvent } from '@/services/driveSync';

interface Progress {
  completed: number;
  failed: number;
  total: number;
}

export function useDriveSyncWS() {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [lastEvent, setLastEvent] = useState<WSEvent | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const attemptRef = useRef(0);

  const connect = useCallback(() => {
    const token = getToken();
    if (!token) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const ws = new WebSocket(`${protocol}//${host}/api/drive/ws?token=${token}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      attemptRef.current = 0;
    };

    ws.onmessage = (event) => {
      const data: WSEvent = JSON.parse(event.data);
      setLastEvent(data);
      if (data.type === 'task_update') {
        setProgress(data.progress);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      // Reconnect with exponential backoff (max 30s)
      const delay = Math.min(1000 * Math.pow(2, attemptRef.current), 30000);
      attemptRef.current += 1;
      reconnectTimeoutRef.current = setTimeout(connect, delay);
    };

    ws.onerror = () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) wsRef.current.close();
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
    };
  }, [connect]);

  return { progress, lastEvent, isConnected };
}
