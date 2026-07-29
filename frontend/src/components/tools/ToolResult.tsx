"use client"

import { Check, Copy, Loader2 } from "lucide-react"
import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { RunResponse } from "@/lib/types"

interface ToolResultProps {
  result: RunResponse | null
  loading: boolean
  error: string | null
}

export function ToolResult({ result, loading, error }: ToolResultProps) {
  const [copied, setCopied] = useState(false)

  if (loading) {
    return (
      <Card className="mt-6">
        <CardContent className="flex items-center justify-center py-12">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          <span className="ml-2 text-muted-foreground">Génération en cours...</span>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="mt-6 border-destructive">
        <CardContent className="py-6 text-destructive">
          {error}
        </CardContent>
      </Card>
    )
  }

  if (!result) return null

  const handleCopy = () => {
    navigator.clipboard.writeText(result.output)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <Card className="mt-6">
      <CardHeader className="flex flex-row items-center justify-between pb-3">
        <div className="flex items-center gap-2">
          <CardTitle className="text-sm">Résultat</CardTitle>
          <Badge variant="outline" className="text-[10px]">
            {result.provider}/{result.model}
          </Badge>
          <Badge variant="secondary" className="text-[10px]">
            {result.duration_ms}ms
          </Badge>
        </div>
        <Button variant="ghost" size="icon" onClick={handleCopy}>
          {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
        </Button>
      </CardHeader>
      <CardContent>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {result.output}
          </ReactMarkdown>
        </div>
      </CardContent>
    </Card>
  )
}
