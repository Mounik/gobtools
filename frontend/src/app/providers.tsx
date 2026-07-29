"use client"

import type { ReactNode } from "react"
import { ThemeProvider } from "@/providers/ThemeProvider"
import { QueryProvider } from "@/providers/QueryProvider"

export function Providers({ children }: { children: ReactNode }) {
  return (
    <QueryProvider>
      <ThemeProvider>{children}</ThemeProvider>
    </QueryProvider>
  )
}
