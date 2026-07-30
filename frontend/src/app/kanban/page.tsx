"use client"

import { useState } from "react"
import { ArrowLeft, Plus, Trash2, ExternalLink } from "lucide-react"
import Link from "next/link"
import { useKanbanBoards, useCreateKanbanBoard, useDeleteKanbanBoard } from "@/hooks/useKanban"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

export default function KanbanPage() {
  const { data: boards, isLoading } = useKanbanBoards()
  const createBoard = useCreateKanbanBoard()
  const deleteBoard = useDeleteKanbanBoard()
  const [newName, setNewName] = useState("")

  const handleCreate = () => {
    const name = newName.trim()
    if (!name) return
    createBoard.mutate({ name }, {
      onSuccess: () => setNewName(""),
    })
  }

  return (
    <div className="space-y-6">
      <Link
        href="/"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4" />
        Retour aux outils
      </Link>

      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Tableaux Kanban</h1>
      </div>

      <div className="flex gap-2">
        <Input
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="Nom du nouveau tableau..."
          className="max-w-sm"
          onKeyDown={(e) => { if (e.key === "Enter") handleCreate() }}
        />
        <Button onClick={handleCreate} disabled={!newName.trim() || createBoard.isPending}>
          <Plus className="mr-2 h-4 w-4" />
          Créer
        </Button>
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-20 w-full rounded-xl" />
          ))}
        </div>
      ) : boards && boards.length > 0 ? (
        <div className="space-y-3">
          {boards.map((board) => (
            <Card key={board.id}>
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base">{board.name}</CardTitle>
                  <div className="flex gap-1">
                    <Link href={`/kanban/${board.id}`}>
                      <Button variant="outline" size="sm">
                        <ExternalLink className="mr-1 h-4 w-4" /> Ouvrir
                      </Button>
                    </Link>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-destructive"
                      onClick={() => deleteBoard.mutate(board.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-xs text-muted-foreground">
                  Créé le {new Date(board.created_at).toLocaleDateString()}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="py-12 text-center text-muted-foreground">
          Aucun tableau. Lance un outil puis crée un Kanban depuis le résultat !
        </div>
      )}
    </div>
  )
}
