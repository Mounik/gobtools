import Link from "next/link"
import {
  Sparkles,
  ListChecks,
  Scale,
  Timer,
  Files,
  CookingPot,
  Brain,
  Text,
  Languages,
  SpellCheck,
  type LucideIcon,
} from "lucide-react"
import type { ToolInfo } from "@/lib/types"

const iconMap: Record<string, LucideIcon> = {
  "list-checks": ListChecks,
  sparkles: Sparkles,
  scale: Scale,
  timer: Timer,
  files: Files,
  "cooking-pot": CookingPot,
  brain: Brain,
  text: Text,
  languages: Languages,
  "spell-check": SpellCheck,
}

const iconBg: Record<string, string> = {
  "list-checks": "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400",
  sparkles: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400",
  scale: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
  timer: "bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-400",
  files: "bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-400",
  "cooking-pot": "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400",
  brain: "bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400",
  text: "bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400",
  languages: "bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-400",
  "spell-check": "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
}

interface ToolCardProps {
  tool: ToolInfo
}

export function ToolCard({ tool }: ToolCardProps) {
  const Icon = iconMap[tool.icon] || Sparkles
  const bg = iconBg[tool.icon] || "bg-muted"

  return (
    <Link
      href={`/tools/${tool.slug}`}
      className="group flex items-center gap-4 rounded-xl border bg-card p-4 shadow-sm transition-all hover:shadow-md hover:border-primary/30"
    >
      <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-lg ${bg}`}>
        <Icon className="h-6 w-6" />
      </div>
      <div className="min-w-0">
        <h3 className="font-semibold">{tool.name}</h3>
        <p className="truncate text-sm text-muted-foreground">
          {tool.description}
        </p>
      </div>
    </Link>
  )
}
