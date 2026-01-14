/**
 * TaskList component - displays a list of tasks.
 * Shows all tasks or empty state message.
 */

'use client';

import { Task } from '@/lib/types';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  userId: number;
  onTaskUpdated: () => void;
}

export default function TaskList({ tasks, userId, onTaskUpdated }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          userId={userId}
          onTaskUpdated={onTaskUpdated}
        />
      ))}
    </div>
  );
}
