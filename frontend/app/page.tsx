// app/page.tsx
'use client';

import { useState, useCallback } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import Chat from '../components/Chat';
import TaskList from '../components/TaskList';

interface Message {
    sender: 'user' | 'agent';
    text: string;
}

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [tasksNeedRefresh, setTasksNeedRefresh] = useState(true);

    // const handleNewMessage = useCallback((msg: any) => {
    //     if (msg.type === 'refresh') {
    //         setTasksNeedRefresh(true);
    //     } else if (msg.type === 'agent_response') {
    //         setMessages((prev) => [...prev, { sender: 'agent', text: msg.content }]);
    //     }
    // }, []);

    const handleNewMessage = useCallback((msg: any) => {
    if (msg.type === 'refresh') {
        setTasksNeedRefresh(true);
    } else if (msg.type === 'task_list') {
        const formatted = msg.tasks.map((t: any) =>
            `• ${t.title} (${t.status}, ${t.priority})`
        ).join('\n');

        setMessages((prev) => [
            ...prev,
            { sender: 'agent', text: `📋 Filtered Tasks:\n${formatted || "No tasks found."}` }
        ]);
    } else if (msg.type === 'agent_response') {
        setMessages((prev) => [...prev, { sender: 'agent', text: msg.content }]);
    }
}, []);


    const { sendMessage } = useWebSocket(handleNewMessage);

    const handleUserMessage = (text: string) => {
        setMessages((prev) => [...prev, { sender: 'user', text }]);
        sendMessage(text);
    };

    return (
        <main className="flex h-screen bg-gray-100 dark:bg-gray-900">
            <div className="w-2/3 overflow-y-auto">
                <TaskList
                    needsRefresh={tasksNeedRefresh}
                    onRefreshComplete={() => setTasksNeedRefresh(false)}
                />
            </div>
            <div className="w-1/3 border-l border-gray-300 dark:border-gray-700">
                <Chat messages={messages} onSendMessage={handleUserMessage} />
            </div>
        </main>
    );
}
