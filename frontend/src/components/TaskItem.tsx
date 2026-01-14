/**
 * TaskItem component - displays a single task with actions.
 * Shows task title, description, completion status, and action buttons.
 */

'use client';

import { Task } from '@/lib/types';
import { toggleTaskComplete, deleteTask } from '@/lib/api/tasks';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

interface TaskItemProps {
  task: Task;
  userId: number;
  onTaskUpdated: () => void;
}

export default function TaskItem({ task, userId, onTaskUpdated }: TaskItemProps) {
  const [isUpdating, setIsUpdating] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const router = useRouter();

  const handleToggleComplete = async () => {
    setIsUpdating(true);
    try {
      await toggleTaskComplete(userId, task.id, !task.is_complete);
      onTaskUpdated();
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
      alert('Failed to update task. Please try again.');
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    setIsUpdating(true);
    try {
      await deleteTask(userId, task.id);
      onTaskUpdated();
      setShowDeleteConfirm(false);
    } catch (error) {
      console.error('Failed to delete task:', error);
      alert('Failed to delete task. Please try again.');
    } finally {
      setIsUpdating(false);
    }
  };

  const handleViewDetails = () => {
    router.push(`/tasks/${task.id}`);
  };

  return (
    <div className="border rounded-lg p-4 mb-3 bg-white shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        {/* Checkbox for completion */}
        <input
          type="checkbox"
          checked={task.is_complete}
          onChange={handleToggleComplete}
          disabled={isUpdating}
          className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />

        {/* Task content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-medium ${
              task.is_complete ? 'line-through text-gray-500' : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p className="mt-1 text-sm text-gray-600 line-clamp-2">
              {task.description}
            </p>
          )}
          <p className="mt-2 text-xs text-gray-400">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Action buttons */}
        <div className="flex gap-2">
          <button
            onClick={handleViewDetails}
            className="px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded"
            disabled={isUpdating}
          >
            View
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
            disabled={isUpdating}
          >
            Delete
          </button>
        </div>
      </div>

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
                disabled={isUpdating}
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white hover:bg-red-700 rounded"
                disabled={isUpdating}
              >
                {isUpdating ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
