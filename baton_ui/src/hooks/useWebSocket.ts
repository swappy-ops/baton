import { useEffect, useRef } from 'react';
import { useStore } from '../stores/useStore';

export const useWebSocket = () => {
  const socketRef = useRef<WebSocket | null>(null);
  const { addTrace, updateWorkflow, addSuggestion } = useStore();

  useEffect(() => {
    const connect = () => {
      const socket = new WebSocket('ws://localhost:8000/ws');
      socketRef.current = socket;

      socket.onopen = () => {
        console.log('WebSocket Connected');
        addTrace({ 
          timestamp: new Date().toLocaleTimeString(), 
          category: 'EXECUTION', 
          message: 'Established Neural Bridge (WebSocket)' 
        });
      };

      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          const { type, data } = payload;

          switch (type) {
            case 'trace:new':
              addTrace(data);
              break;
            case 'workflow:update':
              updateWorkflow(data);
              break;
            case 'suggestion:new':
              addSuggestion(data);
              break;
            default:
              console.log('Unknown event type:', type);
          }
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };

      socket.onclose = () => {
        console.log('WebSocket Disconnected. Reconnecting...');
        setTimeout(connect, 3000);
      };
    };

    connect();

    return () => {
      socketRef.current?.close();
    };
  }, []);

  return socketRef.current;
};
