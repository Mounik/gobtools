"use client"

import { useParams, useRouter } from "next/navigation"
import { ArrowLeft, Loader2, Sparkles, ArrowRight, Upload, Footprints, Timer, Columns3 } from "lucide-react"
import { useState, useRef, useEffect, useCallback } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { useTool } from "@/hooks/useTools"
import { useRunTool } from "@/hooks/useRunTool"
import { useCreateKanbanBoard } from "@/hooks/useKanban"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Skeleton } from "@/components/ui/skeleton"
import type { RunResponse } from "@/lib/types"

function extractTasks(markdown: string): { title: string; description: string }[] {
  const tasks: { title: string; description: string }[] = []
  const lines = markdown.split("\n")
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]

    const checkbox = line.match(/^- \[.]\s+(?:\d+\.\s+)?\*\*(.+?)\*\*(.*)/)
    if (checkbox) {
      const title = checkbox[1].trim()
      let desc = checkbox[2].replace(/^[—–-]\s*/, "").trim()
      let j = i + 1
      while (j < lines.length && /^\s{2,}-?\s/.test(lines[j])) {
        const sub = lines[j].replace(/^\s{2,}-?\s*/, "").trim()
        if (sub) desc += (desc ? " " : "") + sub
        j++
      }
      if (title) tasks.push({ title, description: desc })
      continue
    }

    const table = line.match(/^\|.*\*\*(.+?)\*\*(.*?)\|/)
    if (table) {
      const title = table[1].trim()
      let desc = table[2].replace(/[—–-]\s*/, "").trim()
      if (desc.endsWith("|")) desc = desc.slice(0, -1).trim()
      if (title && !tasks.some((t) => t.title === title)) {
        tasks.push({ title, description: desc })
      }
    }
  }
  return tasks
}

export default function ToolPage() {
  const params = useParams()
  const router = useRouter()
  const slug = params.slug as string
  const { data: tool, isLoading } = useTool(slug)
  const { mutateAsync: runTool, isPending } = useRunTool()
  const createKanban = useCreateKanbanBoard()
  const [input, setInput] = useState("")
  const [result, setResult] = useState<RunResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [countdown, setCountdown] = useState(0)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const countdownRef = useRef<ReturnType<typeof setInterval>>(null)

  const sendToTool = useCallback((targetSlug: string, content: string) => {
    sessionStorage.setItem("magic-todo-result", content)
    router.push(`/tools/${targetSlug}`)
  }, [router])

  useEffect(() => {
    if (slug === "taskmaster" || slug === "premier-pas") {
      const prefill = sessionStorage.getItem("magic-todo-result")
      if (prefill) {
        setInput(prefill)
        sessionStorage.removeItem("magic-todo-result")
      }
    }
  }, [slug])

  useEffect(() => {
    textareaRef.current?.focus()
  }, [])

  useEffect(() => {
    if (slug === "magic-todo" && result && countdown > 0) {
      countdownRef.current = setInterval(() => {
        setCountdown((c) => {
          if (c <= 1) {
            clearInterval(countdownRef.current!)
            sendToTool("taskmaster", result.output)
            return 0
          }
          return c - 1
        })
      }, 1000)
      return () => clearInterval(countdownRef.current!)
    }
  }, [slug, result, countdown, sendToTool])

  const handleRun = async () => {
    if (!input.trim()) return
    setResult(null)
    setError(null)
    try {
      const res = await runTool({ tool_slug: slug, input })
      setResult(res)
      if (slug === "magic-todo") setCountdown(5)
    } catch (e) {
      setError(e instanceof Error ? e.message : "Une erreur est survenue")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      e.preventDefault()
      handleRun()
    }
  }

  const handlePdfUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    setError(null)
    try {
      const { text } = await api.uploadPdf(file)
      setInput((prev) => (prev ? `${prev}\n\n${text}` : text))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur lors de l'upload")
    } finally {
      setUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ""
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-32 w-full" />
      </div>
    )
  }

  if (!tool) {
    return (
      <div className="py-12 text-center text-muted-foreground">
        Outil introuvable
      </div>
    )
  }

  const tasks = result ? extractTasks(result.output) : []

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <button
        onClick={() => router.push("/")}
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4" />
        Retour
      </button>

      <div className="flex items-center gap-3">
        <Sparkles className="h-6 w-6 text-primary" />
        <div>
          <h1 className="text-xl font-bold">{tool.name}</h1>
          <p className="text-sm text-muted-foreground">{tool.description}</p>
        </div>
      </div>

      <div className="space-y-3">
        <Textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Décrivez votre tâche..."
          className="min-h-[120px] resize-y text-base"
        />
        <div className="flex items-center gap-2">
          <Button
            onClick={handleRun}
            disabled={isPending || !input.trim()}
            size="lg"
            className="px-8"
          >
            {isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Génération...
              </>
            ) : (
              "Lancer"
            )}
          </Button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handlePdfUpload}
            className="hidden"
          />
          <Button
            variant="outline"
            size="icon"
            disabled={uploading}
            onClick={() => fileInputRef.current?.click()}
            title="Importer un PDF"
          >
            {uploading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Upload className="h-4 w-4" />
            )}
          </Button>
          <span className="text-xs text-muted-foreground">
            Ctrl+Enter pour envoyer
          </span>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
          {error}
        </div>
      )}

      {result && (
        <div className="rounded-xl border bg-card p-6 shadow-sm">
          {slug === "magic-todo" && countdown > 0 && (
            <div className="mb-4 flex items-center justify-between rounded-lg border border-primary/30 bg-primary/5 px-4 py-3 text-sm">
              <span className="flex items-center gap-2">
                <Timer className="h-4 w-4 text-primary" />
                Envoi automatique vers Task Master dans <strong>{countdown}s</strong>
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => { setCountdown(0); clearInterval(countdownRef.current!) }}
              >
                Annuler
              </Button>
            </div>
          )}
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {result.output}
            </ReactMarkdown>
          </div>
          {slug === "magic-todo" && tasks.length > 0 && (
            <div className="mt-4 space-y-3 border-t pt-4">
              <p className="text-xs font-medium text-muted-foreground">
                Décomposer chaque tâche avec Premier Pas&nbsp;:
              </p>
              <div className="flex flex-wrap gap-2">
                {tasks.map((task, i) => (
                  <Button
                    key={i}
                    variant="outline"
                    size="sm"
                    onClick={() => sendToTool("premier-pas", task.title)}
                    className="text-xs"
                  >
                    <Footprints className="mr-1 h-3 w-3" />
                    {task.title.length > 30 ? task.title.slice(0, 30) + "…" : task.title}
                  </Button>
                ))}
              </div>
              <div className="flex gap-2 pt-2">
                <Button
                  variant="secondary"
                  onClick={() => sendToTool("taskmaster", result.output)}
                >
                  <ArrowRight className="mr-2 h-4 w-4" />
                  Ordonnancer avec Task Master
                </Button>
              </div>
            </div>
          )}
          {slug === "taskmaster" && tasks.length > 0 && (
            <div className="mt-4 border-t pt-4">
              <Button
                variant="secondary"
                onClick={() => {
                  createKanban.mutate(
                    {
                      name: `Planning - ${new Date().toLocaleDateString()}`,
                      tasks: tasks.map((t) => ({
                        title: t.title,
                        description: t.description,
                        column: "todo" as const,
                        priority: "medium" as const,
                      })),
                    },
                    {
                      onSuccess: (board) => router.push(`/kanban/${board.id}`),
                    },
                  )
                }}
                disabled={createKanban.isPending}
              >
                <Columns3 className="mr-2 h-4 w-4" />
                {createKanban.isPending ? "Création..." : "Créer un tableau Kanban"}
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
