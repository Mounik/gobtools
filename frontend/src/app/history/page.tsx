"use client"

import { useState } from "react"
import { Copy, Trash2, ArrowLeft, Search, X } from "lucide-react"
import Link from "next/link"
import { useHistory, useDeleteHistory } from "@/hooks/useHistory"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"

export default function HistoryPage() {
  const [search, setSearch] = useState("")
  const [page, setPage] = useState(1)
  const { data, isLoading } = useHistory(page, search || undefined)
  const { mutate: deleteEntry } = useDeleteHistory()
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
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
        <h1 className="text-2xl font-bold">Historique</h1>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          value={search}
          onChange={(e) => {
            setSearch(e.target.value)
            setPage(1)
          }}
          placeholder="Rechercher dans l'historique..."
          className="h-10 pl-9 pr-9"
        />
        {search && (
          <Button
            variant="ghost"
            size="icon"
            className="absolute right-1 top-1/2 h-8 w-8 -translate-y-1/2"
            onClick={() => setSearch("")}
          >
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : data && data.items.length > 0 ? (
        <>
          <div className="space-y-3">
            {data.items.map((entry) => (
              <Card key={entry.id}>
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <CardTitle className="text-sm capitalize">
                        {entry.tool_slug}
                      </CardTitle>
                      <Badge variant="outline" className="text-[10px]">
                        {entry.provider}
                      </Badge>
                    </div>
                    <div className="flex gap-1">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8"
                        onClick={() => handleCopy(entry.output, entry.id)}
                      >
                        {copiedId === entry.id ? (
                          <span className="text-xs text-green-500">OK</span>
                        ) : (
                          <Copy className="h-4 w-4" />
                        )}
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 text-destructive hover:text-destructive"
                        onClick={() => deleteEntry(entry.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="mb-1 text-xs text-muted-foreground line-clamp-1">
                    {entry.input}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {new Date(entry.created_at).toLocaleDateString()}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>

          {data.total > data.page_size && (
            <div className="flex items-center justify-center gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                Précédent
              </Button>
              <span className="text-sm text-muted-foreground">
                Page {data.page} sur {Math.ceil(data.total / data.page_size)}
              </span>
              <Button
                variant="outline"
                size="sm"
                disabled={data.page * data.page_size >= data.total}
                onClick={() => setPage((p) => p + 1)}
              >
                Suivant
              </Button>
            </div>
          )}
        </>
      ) : (
        <div className="py-12 text-center text-muted-foreground">
          {search ? "Aucun historique ne correspond à votre recherche." : "Aucun historique. Lancez un outil pour commencer !"}
        </div>
      )}
    </div>
  )
}
