"use client"

import { usePathname } from "next/navigation"

export function MainContent({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const isKanban = pathname?.startsWith("/kanban")
  return (
    <main
      className={
        isKanban
          ? "mx-auto w-full px-4 py-8"
          : "mx-auto max-w-5xl px-4 py-8"
      }
    >
      {children}
    </main>
  )
}
