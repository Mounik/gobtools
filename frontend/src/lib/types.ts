export interface ToolInfo {
  slug: string
  name: string
  description: string
  icon: string
  provider: string
  model: string
  temperature: number
  category: string
}

export interface ToolDetail extends ToolInfo {
  prompt: string
}

export interface RunRequest {
  tool_slug: string
  input: string
  provider?: string
  model?: string
  temperature?: number
  max_tokens?: number
}

export interface RunResponse {
  id: string
  output: string
  provider: string
  model: string
  duration_ms: number
  tokens_in: number
  tokens_out: number
}

export interface HistoryEntry {
  id: string
  tool_slug: string
  input: string
  output: string
  created_at: string
  provider: string
  model: string
}

export interface PaginatedHistory {
  items: HistoryEntry[]
  total: number
  page: number
  page_size: number
}

export interface FavoriteItem {
  tool_slug: string
  name: string
  icon: string
}

export interface SettingsUpdate {
  provider?: string
  model?: string
  temperature?: number
  max_tokens?: number
  timeout?: number
}
