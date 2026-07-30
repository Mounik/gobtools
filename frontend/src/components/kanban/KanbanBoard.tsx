"use client"

import { useState } from "react"
import {
  DragDropContext,
  Droppable,
  Draggable,
  type DropResult,
} from "@hello-pangea/dnd"
import { Plus, Trash2, GripVertical } from "lucide-react"
import type { KanbanBoard as KanbanBoardType, KanbanTask } from "@/lib/types"
import { useUpdateKanbanTask, useDeleteKanbanTask, useAddKanbanTask, useDeleteKanbanBoard } from "@/hooks/useKanban"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

const COLUMNS = [
  { id: "todo", label: "📋 À faire", color: "border-t-blue-500" },
  { id: "in_progress", label: "🔧 En cours", color: "border-t-amber-500" },
  { id: "done", label: "✅ Terminé", color: "border-t-emerald-500" },
] as const

const PRIORITY_LABELS: Record<string, string> = {
  critical: "🔴 Critique",
  high: "🟡 Haute",
  medium: "🟢 Moyenne",
  low: "⚪ Basse",
}

type Props = {
  board: KanbanBoardType
}

export default function KanbanBoardView({ board }: Props) {
  const updateTask = useUpdateKanbanTask()
  const deleteTask = useDeleteKanbanTask()
  const addTask = useAddKanbanTask()
  const deleteBoard = useDeleteKanbanBoard()
  const [newTaskTitle, setNewTaskTitle] = useState<Record<string, string>>({})
  const [editingTask, setEditingTask] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState("")
  const [editDesc, setEditDesc] = useState("")

  const tasksByColumn = (colId: string) =>
    board.tasks
      .filter((t) => t.column === colId)
      .sort((a, b) => a.position - b.position)

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return
    const { draggableId, destination } = result
    const task = board.tasks.find((t) => t.id === draggableId)
    if (!task) return

    const targetCol = destination.droppableId
    const targetPos = destination.index

    updateTask.mutate({
      taskId: draggableId,
      data: { column: targetCol as KanbanTask["column"], position: targetPos },
    })
  }

  const handleAddTask = (column: string) => {
    const title = newTaskTitle[column]?.trim()
    if (!title) return
    addTask.mutate(
      { boardId: board.id, data: { title, column: column as KanbanTask["column"], priority: "medium" } },
      { onSuccess: () => setNewTaskTitle((prev) => ({ ...prev, [column]: "" })) },
    )
  }

  const handleDeleteBoard = () => {
    if (confirm("Supprimer ce tableau Kanban ?")) {
      deleteBoard.mutate(board.id)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">{board.name}</h1>
        <Button variant="destructive" size="sm" onClick={handleDeleteBoard}>
          <Trash2 className="mr-1 h-4 w-4" /> Supprimer
        </Button>
      </div>

      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          {COLUMNS.map((col) => (
            <div
              key={col.id}
              className={`rounded-xl border border-t-4 bg-card shadow-sm ${col.color}`}
            >
              <div className="border-b px-4 py-3 font-semibold text-sm">
                {col.label}{" "}
                <span className="text-muted-foreground font-normal">
                  ({tasksByColumn(col.id).length})
                </span>
              </div>

              <Droppable droppableId={col.id}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className={`min-h-[200px] space-y-2 p-3 transition-colors ${
                      snapshot.isDraggingOver ? "bg-muted/50" : ""
                    }`}
                  >
                    {tasksByColumn(col.id).map((task, index) => (
                      <Draggable key={task.id} draggableId={task.id} index={index}>
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            className={`rounded-lg border bg-card p-3 text-sm shadow-sm transition-shadow ${
                              snapshot.isDragging ? "shadow-lg ring-2 ring-primary" : ""
                            }`}
                          >
                            <div className="flex items-start gap-2">
                              <div
                                {...provided.dragHandleProps}
                                className="mt-0.5 shrink-0 cursor-grab text-muted-foreground"
                              >
                                <GripVertical className="h-4 w-4" />
                              </div>
                              <div className="min-w-0 flex-1">
                                {editingTask === task.id ? (
                                  <div className="space-y-2">
                                    <Input
                                      value={editTitle}
                                      onChange={(e) => setEditTitle(e.target.value)}
                                      className="h-8 text-sm"
                                      autoFocus
                                    />
                                    <Textarea
                                      value={editDesc}
                                      onChange={(e) => setEditDesc(e.target.value)}
                                      className="min-h-[60px] text-xs"
                                      placeholder="Description..."
                                    />
                                    <div className="flex gap-1">
                                      <Button
                                        size="sm"
                                        variant="default"
                                        className="h-7 text-xs"
                                        onClick={() => {
                                          updateTask.mutate({
                                            taskId: task.id,
                                            data: { title: editTitle, description: editDesc },
                                          })
                                          setEditingTask(null)
                                        }}
                                      >
                                        OK
                                      </Button>
                                      <Button
                                        size="sm"
                                        variant="ghost"
                                        className="h-7 text-xs"
                                        onClick={() => setEditingTask(null)}
                                      >
                                        Annuler
                                      </Button>
                                    </div>
                                  </div>
                                ) : (
                                  <>
                                    <div
                                      className="cursor-pointer font-medium"
                                      onClick={() => {
                                        setEditingTask(task.id)
                                        setEditTitle(task.title)
                                        setEditDesc(task.description)
                                      }}
                                    >
                                      {task.title}
                                    </div>
                                    {task.description && (
                                      <p className="mt-1 text-xs text-muted-foreground line-clamp-2">
                                        {task.description}
                                      </p>
                                    )}
                                    <div className="mt-1 flex items-center gap-2">
                                      <span className="text-[10px] text-muted-foreground">
                                        {PRIORITY_LABELS[task.priority] || task.priority}
                                      </span>
                                      <button
                                        className="ml-auto text-muted-foreground hover:text-destructive"
                                        onClick={() => deleteTask.mutate(task.id)}
                                      >
                                        <Trash2 className="h-3 w-3" />
                                      </button>
                                    </div>
                                  </>
                                )}
                              </div>
                            </div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>

              <div className="border-t p-3">
                <div className="flex gap-2">
                  <Input
                    value={newTaskTitle[col.id] || ""}
                    onChange={(e) =>
                      setNewTaskTitle((prev) => ({ ...prev, [col.id]: e.target.value }))
                    }
                    placeholder="Nouvelle tâche..."
                    className="h-8 text-xs"
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleAddTask(col.id)
                    }}
                  />
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-8 shrink-0"
                    onClick={() => handleAddTask(col.id)}
                    disabled={!newTaskTitle[col.id]?.trim()}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </DragDropContext>
    </div>
  )
}
