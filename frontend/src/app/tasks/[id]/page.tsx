/**
 * Task detail page - view and edit a single task.
 * Displays full task information with edit and delete functionality.
 */

'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import TaskForm from '@/components/TaskForm';
import { getTask, updateTask, deleteTask, toggleTaskComplete } from '@/lib/api/tasks';
import { Task, TaskUpdate } from '@/lib/types';

export default function TaskDetailPage() {
  const [task, setTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState('');
  const [userId, setUserId] = useState<number | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const router = useRouter();
  const params = useParams();
  const taskId = parseInt(params.id as string, 10);

  // Get user ID from localStorage
  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id');
    if (!storedUserId) {
      router.push('/login');
      return;
    }
    setUserId(parseInt(storedUserId, 10));
  }, [router]);

  // Fetch task when userId is available
  useEffect(() => {
    if (userId) {
      fetchTask();
    }
  }, [userId, taskId]);

  const fetchTask = async () => {
    if (!userId) return;

    setIsLoading(true);
    setError('');

    try {
      const fetchedTask = await getTask(userId, taskId);
      setTask(fetchedTask);
    } catch (err) {
      console.error('Failed to fetch task:', err);
      setError('Failed to load task. Please try again.');

      // If not found or unauthorized, redirect to tasks list
      if (err instanceof Error && (err.message.includes('404') || err.message.includes('403'))) {
        setTimeout(() => router.push('/tasks'), 2000);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateTask = async (taskData: TaskUpdate) => {
    if (!userId || !task) return;

    try {
      await updateTask(userId, task.id, taskData);
      setIsEditing(false);
      await fetchTask(); // Refresh task data
    } catch (err) {
      throw err; // Let TaskForm handle the error
    }
  };

  const handleToggleComplete = async () => {
    if (!userId || !task) return;

    try {
      await toggleTaskComplete(userId, task.id, !task.is_complete);
      await fetchTask(); // Refresh task data
    } catch (err) {
      console.error('Failed to toggle completion:', err);
      setError('Failed to update task. Please try again.');
    }
  };

  const handleDelete = async () => {
    if (!userId || !task) return;

    setIsDeleting(true);
    try {
      await deleteTask(userId, task.id);
      router.push('/tasks');
    } catch (err) {
      console.error('Failed to delete task:', err);
      setError('Failed to delete task. Please try again.');
      setIsDeleting(false);
    }
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
          <button
            onClick={() => router.push('/tasks')}
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            ← Back to Tasks
          </button>
          <h1 className="text-2xl font-bold text-gray-900">Task Details</h1>
          <div className="w-24"></div> {/* Spacer for centering */}
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Error message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Loading state */}
        {isLoading && (
          <div className="text-center py-12">
            <p className="text-gray-500">Loading task...</p>
          </div>
        )}

        {/* Task content */}
        {!isLoading && task && (
          <div className="bg-white rounded-lg shadow-md p-6">
            {isEditing ? (
              <>
                <h2 className="text-xl font-semibold mb-4">Edit Task</h2>
                <TaskForm
                  initialData={{ title: task.title, description: task.description }}
                  onSubmit={handleUpdateTask}
                  onCancel={() => setIsEditing(false)}
                  submitLabel="Save Changes"
                />
              </>
            ) : (
              <>
                {/* Task header */}
                <div className="flex items-start justify-between mb-6">
                  <div className="flex items-start gap-3 flex-1">
                    <input
                      type="checkbox"
                      checked={task.is_complete}
                      onChange={handleToggleComplete}
                      className="mt-1 h-6 w-6 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <div className="flex-1">
                      <h2
                        className={`text-2xl font-bold ${
                          task.is_complete ? 'line-through text-gray-500' : 'text-gray-900'
                        }`}
                      >
                        {task.title}
                      </h2>
                      <p className="mt-2 text-sm text-gray-500">
                        Created: {new Date(task.created_at).toLocaleString()}
                      </p>
                      {task.updated_at !== task.created_at && (
                        <p className="text-sm text-gray-500">
                          Updated: {new Date(task.updated_at).toLocaleString()}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Task description */}
                <div className="mb-6">
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">Description</h3>
                  {task.description ? (
                    <p className="text-gray-700 whitespace-pre-wrap">{task.description}</p>
                  ) : (
                    <p className="text-gray-400 italic">No description provided</p>
                  )}
                </div>

                {/* Action buttons */}
                <div className="flex gap-3 justify-end pt-4 border-t">
                  <button
                    onClick={() => setIsEditing(true)}
                    className="px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-md"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => setShowDeleteConfirm(true)}
                    className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-md"
                  >
                    Delete
                  </button>
                </div>
              </>
            )}
          </div>
        )}

        {/* Delete confirmation dialog */}
        {showDeleteConfirm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-sm mx-4">
              <h3 className="text-lg font-semibold mb-2">Delete Task?</h3>
              <p className="text-gray-600 mb-4">
                Are you sure you want to delete this task? This action cannot be undone.
              </p>
              <div className="flex gap-3 justify-end">
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded"
                  disabled={isDeleting}
                >
                  Cancel
                </button>
                <button
                  onClick={handleDelete}
                  className="px-4 py-2 bg-red-600 text-white hover:bg-red-700 rounded"
                  disabled={isDeleting}
                >
                  {isDeleting ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
