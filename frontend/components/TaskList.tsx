// components/TaskList.tsx
'use client';

import React, { useEffect, useState } from 'react';

interface Task {
    id: number;
    title: string;
    status: string;
    due_date?: string;
    priority: string;
}

interface TaskListProps {
    needsRefresh: boolean;
    onRefreshComplete: () => void;
}

const TaskList: React.FC<TaskListProps> = ({ needsRefresh, onRefreshComplete }) => {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(false);

    const fetchTasks = async () => {
        try {
            setLoading(true);
            const res = await fetch('http://localhost:8000/api/tasks');
            const data = await res.json();
            setTasks(data);
        } catch (err) {
            console.error('Error fetching tasks:', err);
        } finally {
            setLoading(false);
            onRefreshComplete();
        }
    };

    const updateTaskStatus = async (id: number, currentStatus: string) => {
        const newStatus = currentStatus === 'done' ? 'todo' : 'done';
        try {
            await fetch(`http://localhost:8000/api/tasks/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: newStatus }),
            });
            fetchTasks();
        } catch (err) {
            console.error('Failed to update task status:', err);
        }
    };

    const handleDelete = async (id: number) => {
        try {
            await fetch(`http://localhost:8000/api/tasks/${id}`, {
                method: 'DELETE',
            });
            fetchTasks();
        } catch (err) {
            console.error('Failed to delete task:', err);
        }
    };

    useEffect(() => {
        if (needsRefresh) {
            fetchTasks();
        }
    }, [needsRefresh]);

    return (
        <div className="p-4">
            <h2 className="text-xl font-bold mb-2">📋 Tasks</h2>

            {loading ? (
                <p>Loading...</p>
            ) : tasks.length === 0 ? (
                <p>No tasks available.</p>
            ) : (
                <ul className="space-y-2">
                    {tasks.map(task => (
                        <li
                            key={task.id}
                            className="p-3 bg-white dark:bg-gray-800 rounded shadow flex justify-between items-center"
                        >
                            <div>
                                <label className="inline-flex items-center space-x-2">
                                    <input
                                        type="checkbox"
                                        checked={task.status === 'done'}
                                        onChange={() => updateTaskStatus(task.id, task.status)}
                                    />
                                    <span
                                        className={`font-semibold ${
                                            task.status === 'done' ? 'line-through text-gray-400' : ''
                                        }`}
                                    >
                                        {task.title}
                                    </span>
                                </label>
                                <p className="text-sm text-gray-500">Status: {task.status}</p>
                                <p className="text-sm text-gray-500">Priority: {task.priority}</p>
                                {task.due_date && (
                                    <p className="text-sm text-gray-500">
                                        Due: {new Date(task.due_date).toLocaleString()}
                                    </p>
                                )}
                            </div>
                            <button
                                onClick={() => handleDelete(task.id)}
                                className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                            >
                                Delete
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default TaskList;
