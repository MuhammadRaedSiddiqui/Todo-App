/**
 * TaskForm component - form for creating and editing tasks.
 * Handles title and description input with validation.
 */

'use client';

import { useState } from 'react';
import { TaskCreate, TaskUpdate } from '@/lib/types';

interface TaskFormProps {
  initialData?: TaskUpdate;
  onSubmit: (data: TaskCreate | TaskUpdate) => Promise<void>;
  onCancel: () => void;
  submitLabel?: string;
}

export default function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  submitLabel = 'Create Task',
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate title
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length > 200) {
      setError('Title must not exceed 200 characters');
      return;
    }

    if (description && description.length > 2000) {
      setError('Description must not exceed 2000 characters');
      return;
    }

    setIsSubmitting(true);

    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || null,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save task');
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter task title"
          disabled={isSubmitting}
          required
        />
        <p className="mt-1 text-xs text-gray-500">{title.length}/200 characters</p>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={2000}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter task description"
          disabled={isSubmitting}
        />
        <p className="mt-1 text-xs text-gray-500">{description.length}/2000 characters</p>
      </div>

      <div className="flex gap-3 justify-end">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
          disabled={isSubmitting}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-md disabled:bg-blue-300"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Saving...' : submitLabel}
        </button>
      </div>
    </form>
  );
}
