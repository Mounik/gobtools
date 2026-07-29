"use client"

import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"

export function useTools() {
  return useQuery({
    queryKey: ["tools"],
    queryFn: api.listTools,
    staleTime: 1000 * 60 * 5,
  })
}

export function useTool(slug: string) {
  return useQuery({
    queryKey: ["tool", slug],
    queryFn: () => api.getTool(slug),
    enabled: !!slug,
    staleTime: 1000 * 60 * 5,
  })
}
