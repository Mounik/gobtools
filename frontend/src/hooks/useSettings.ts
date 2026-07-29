"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import type { SettingsUpdate } from "@/lib/types"

const STORAGE_KEY = "gobtools-settings"

function getSettings(): Record<string, unknown> {
  if (typeof window === "undefined") return {}
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}")
  } catch {
    return {}
  }
}

function saveSettings(settings: Record<string, unknown>) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
}

export function useSettings() {
  return useQuery({
    queryKey: ["settings"],
    queryFn: () => getSettings(),
  })
}

export function useUpdateSettings() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (update: SettingsUpdate) => {
      const current = getSettings()
      const next = { ...current, ...update }
      saveSettings(next)
      return next
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["settings"] })
    },
  })
}
