"use client"

import Link from "next/link"
import { History, Wand2 } from "lucide-react"
import { ThemeToggle } from "./ThemeToggle"

export function NavBar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <Wand2 className="h-5 w-5" />
          <span>GobTools</span>
        </Link>
        <nav className="flex items-center gap-2">
          <Link
            href="/history"
            className="inline-flex items-center gap-1 rounded-md px-3 py-1.5 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
          >
            <History className="h-4 w-4" />
            Historique
          </Link>
          <ThemeToggle />
        </nav>
      </div>
    </header>
  )
}
