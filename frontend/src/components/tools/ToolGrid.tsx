import { Skeleton } from "@/components/ui/skeleton"
import { ToolCard } from "./ToolCard"
import type { ToolInfo } from "@/lib/types"

interface ToolGridProps {
  tools: ToolInfo[]
  loading: boolean
}

export function ToolGrid({ tools, loading }: ToolGridProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="rounded-xl border p-6">
            <Skeleton className="mb-2 h-5 w-32" />
            <Skeleton className="mb-4 h-8 w-full" />
            <div className="flex gap-2">
              <Skeleton className="h-5 w-16 rounded-full" />
              <Skeleton className="h-5 w-14 rounded-full" />
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (tools.length === 0) {
    return (
      <div className="py-12 text-center text-muted-foreground">
        Aucun outil trouvé.
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {tools.map((tool) => (
        <ToolCard key={tool.slug} tool={tool} />
      ))}
    </div>
  )
}
