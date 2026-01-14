/**
 * Tasks page - main task list view.
 * Displays all tasks for authenticated user with create functionality.
 */

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';
import { listTasks, createTask } from '@/lib/api/tasks';
import { Task, TaskCreate, TaskUpdate } from '@/lib/types';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [error, setError] = useState('');
  const [userId, setUserId] = useState<number | null>(null);
  const router = useRouter();

  // Get user ID from localStorage (set during login)
  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id');
    if (!storedUserId) {
      router.push('/login');
      return;
    }
    setUserId(parseInt(storedUserId, 10));
  }, [router]);

  // Fetch tasks when userId is available
  useEffect(() => {
    if (userId) {
      fetchTasks();
    }
  }, [userId]);

  const fetchTasks = async () => {
    if (!userId) return;

    setIsLoading(true);
    setError('');

    try {
      const fetchedTasks = await listTasks(userId);
      setTasks(fetchedTasks);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
      setError('Failed to load tasks. Please try again.');

      // If unauthorized, redirect to login
      if (err instanceof Error && err.message.includes('401')) {
        localStorage.removeItem('user_id');
        localStorage.removeItem('access_token');
        router.push('/login');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTask = async (taskData: TaskCreate | TaskUpdate) => {
    if (!userId) return;

    try {
      await createTask(userId, taskData as TaskCreate);
      setShowCreateForm(false);
      await fetchTasks(); // Refresh task list
    } catch (err) {
      throw err; // Let TaskForm handle the error
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user_id');
    localStorage.removeItem('access_token');
    router.push('/login');
  };

  if (!userId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Add Task button */}
        {!showCreateForm && (
          <div className="mb-6">
            <button
              onClick={() => setShowCreateForm(true)}
              className="px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition-colors"
            >
              + Add Task
            </button>
          </div>
        )}

        {/* Create task form */}
        {showCreateForm && (
          <div className="mb-6 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Create New Task</h2>
            <TaskForm
              onSubmit={handleCreateTask}
              onCancel={() => setShowCreateForm(false)}
              submitLabel="Create Task"
            />
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Loading state */}
        {isLoading && (
          <div className="text-center py-12">
            <p className="text-gray-500">Loading tasks...</p>
          </div>
        )}

        {/* Task list */}
        {!isLoading && (
          <TaskList tasks={tasks} userId={userId} onTaskUpdated={fetchTasks} />
        )}
      </main>
    </div>
  );
}
