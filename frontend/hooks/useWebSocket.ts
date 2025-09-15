
// hooks/useWebSocket.ts
import { useState, useEffect, useCallback } from 'react';

const WS_URL = 'ws://localhost:8000/ws/chat';

export const useWebSocket = (onMessage: (message: any) => void) => {
    const [ws, setWs] = useState<WebSocket | null>(null);
const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        const socket = new WebSocket(WS_URL);
        socket.onopen = () => {
            console.log('✅ WebSocket Connected');
            setIsConnected(true);
        };
        socket.onmessage = (event) => {
            const message = event.data;
            try {
                if (message === 'refresh_tasks') {
                    onMessage({ type: 'refresh' });
                } else {
                    onMessage(JSON.parse(message));
                }
            } catch (error) {
                console.error('❌ Error parsing message:', error);
            }
        };
        socket.onclose = () => {
            console.log('🔌 WebSocket Disconnected');
            setIsConnected(false);
        };
        setWs(socket);

        return () => {
            socket.close();
        };
    }, [onMessage]);

    const sendMessage = useCallback((message: string) => {
        if (ws?.readyState === WebSocket.OPEN) {
            ws.send(message);
        }
    }, [ws]);

    return { sendMessage };
};
