"use client"

import { useParams, useRouter } from "next/navigation"
import { ArrowLeft, Loader2 } from "lucide-react"
import { useKanbanBoard } from "@/hooks/useKanban"
import KanbanBoardView from "@/components/kanban/KanbanBoard"
import { Skeleton } from "@/components/ui/skeleton"

export default function KanbanBoardPage() {
  const params = useParams()
  const router = useRouter()
  const boardId = params.id as string
  const { data: board, isLoading } = useKanbanBoard(boardId)

  return (
    <div className="space-y-6">
      <button
        onClick={() => router.push("/kanban")}
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4" />
        Tous les tableaux
      </button>

      {isLoading ? (
        <div className="space-y-4">
          <Skeleton className="h-8 w-48" />
          <div className="grid grid-cols-3 gap-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <Skeleton key={i} className="h-64 rounded-xl" />
            ))}
          </div>
        </div>
      ) : board ? (
        <KanbanBoardView board={board} />
      ) : (
        <div className="py-12 text-center text-muted-foreground">
          Tableau introuvable
        </div>
      )}
    </div>
  )
}
