"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { KanbanBoard, KanbanTask } from "@/lib/types"

export function useKanbanBoards() {
  return useQuery({
    queryKey: ["kanban-boards"],
    queryFn: api.listKanbanBoards,
  })
}

export function useKanbanBoard(id: string | null) {
  return useQuery({
    queryKey: ["kanban-board", id],
    queryFn: () => api.getKanbanBoard(id!),
    enabled: !!id,
  })
}

export function useCreateKanbanBoard() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: { name: string; tasks?: Partial<KanbanTask>[] }) =>
      api.createKanbanBoard(data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["kanban-boards"] })
    },
  })
}

export function useDeleteKanbanBoard() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: api.deleteKanbanBoard,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["kanban-boards"] })
    },
  })
}

export function useAddKanbanTask() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({
      boardId,
      data,
    }: {
      boardId: string
      data: Partial<KanbanTask>
    }) => api.addKanbanTask(boardId, data),
    onSuccess: (_, vars) => {
      qc.invalidateQueries({ queryKey: ["kanban-board", vars.boardId] })
    },
  })
}

export function useUpdateKanbanTask() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({
      taskId,
      data,
    }: {
      taskId: string
      data: Partial<KanbanTask>
    }) => api.updateKanbanTask(taskId, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["kanban-board"] })
    },
  })
}

export function useDeleteKanbanTask() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: api.deleteKanbanTask,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["kanban-board"] })
    },
  })
}
