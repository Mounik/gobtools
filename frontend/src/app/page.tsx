"use client"

import { useTools } from "@/hooks/useTools"
import { ToolCard } from "@/components/tools/ToolCard"
import { Skeleton } from "@/components/ui/skeleton"

export default function HomePage() {
  const { data: tools, isLoading } = useTools()

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight">GobTools</h1>
        <p className="mt-2 text-muted-foreground">
          Une collection d&apos;outils simples propulsés par l&apos;IA
        </p>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-28 w-full rounded-xl" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {tools?.map((tool) => (
            <ToolCard key={tool.slug} tool={tool} />
          ))}
        </div>
      )}
    </div>
  )
}
