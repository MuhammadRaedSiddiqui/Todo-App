/**
 * Tool call display component for visualizing AI tool executions.
 */
'use client';

interface ToolCallDisplayProps {
  toolName: string;
  toolCallId?: string;
}

export function ToolCallDisplay({ toolName, toolCallId }: ToolCallDisplayProps) {
  // Map tool names to user-friendly labels
  const toolLabels: Record<string, string> = {
    add_task: '➕ Created Task',
    list_tasks: '📋 Listed Tasks',
    update_task: '✏️ Updated Task',
    delete_task: '🗑️ Deleted Task',
    get_task: '🔍 Retrieved Task',
  };

  const label = toolLabels[toolName] || `🔧 ${toolName}`;

  return (
    <div className="mt-2 pt-2 border-t border-yellow-300">
      <div className="text-xs font-mono">
        <span className="font-semibold">{label}</span>
        {toolCallId && (
          <span className="ml-2 opacity-50">ID: {toolCallId.slice(0, 8)}</span>
        )}
      </div>
    </div>
  );
}
