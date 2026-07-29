"use client"

import { useParams, useRouter } from "next/navigation"
import { ArrowLeft, Loader2, Sparkles } from "lucide-react"
import { useState, useRef, useEffect } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { useTool } from "@/hooks/useTools"
import { useRunTool } from "@/hooks/useRunTool"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Skeleton } from "@/components/ui/skeleton"
import type { RunResponse } from "@/lib/types"

export default function ToolPage() {
  const params = useParams()
  const router = useRouter()
  const slug = params.slug as string
  const { data: tool, isLoading } = useTool(slug)
  const { mutateAsync: runTool, isPending } = useRunTool()
  const [input, setInput] = useState("")
  const [result, setResult] = useState<RunResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    textareaRef.current?.focus()
  }, [])

  const handleRun = async () => {
    if (!input.trim()) return
    setResult(null)
    setError(null)
    try {
      const res = await runTool({ tool_slug: slug, input })
      setResult(res)
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
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {result.output}
            </ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  )
}
