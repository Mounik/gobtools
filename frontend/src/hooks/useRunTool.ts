"use client"

import { useMutation } from "@tanstack/react-query"
import { api } from "@/lib/api"
import type { RunRequest, RunResponse } from "@/lib/types"

export function useRunTool() {
  return useMutation<RunResponse, Error, RunRequest>({
    mutationFn: api.runTool,
  })
}
