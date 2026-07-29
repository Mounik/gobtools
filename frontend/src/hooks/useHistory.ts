"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useHistory(page = 1, search?: string) {
  return useQuery({
    queryKey: ["history", page, search],
    queryFn: () => api.listHistory(page, 20, search),
  })
}

export function useDeleteHistory() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: api.deleteHistory,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["history"] })
    },
  })
}
