import type {
  FavoriteItem,
  HistoryEntry,
  PaginatedHistory,
  RunRequest,
  RunResponse,
  ToolDetail,
  ToolInfo,
} from "./types"

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"
const USER_ID = "00000000-0000-0000-0000-000000000001"

async function fetchApi<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  return res.json()
}

export const api = {
  uploadPdf: async (file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    const res = await fetch(`${API_BASE}/upload/pdf`, {
      method: "POST",
      body: formData,
    })
    if (!res.ok) {
      const text = await res.text()
      throw new Error(text || res.statusText)
    }
    return res.json() as Promise<{ filename: string; text: string; length: number }>
  },
  listTools: () => fetchApi<ToolInfo[]>("/tools"),

  getTool: (slug: string) => fetchApi<ToolDetail>(`/tools/${slug}`),

  runTool: (req: RunRequest) =>
    fetchApi<RunResponse>("/run", {
      method: "POST",
      body: JSON.stringify(req),
    }),

  listHistory: (page = 1, pageSize = 20, search?: string) => {
    const params = new URLSearchParams({
      user_id: USER_ID,
      page: String(page),
      page_size: String(pageSize),
    })
    if (search) params.set("search", search)
    return fetchApi<PaginatedHistory>(`/history?${params}`)
  },

  deleteHistory: (id: string) =>
    fetchApi<{ ok: boolean }>(`/history/${id}?user_id=${USER_ID}`, {
      method: "DELETE",
    }),

  listFavorites: () =>
    fetchApi<FavoriteItem[]>(`/favorites?user_id=${USER_ID}`),

  addFavorite: (toolSlug: string) =>
    fetchApi<{ ok: boolean }>(
      `/favorites?user_id=${USER_ID}`,
      {
        method: "POST",
        body: JSON.stringify({ tool_slug: toolSlug }),
      }
    ),

  removeFavorite: (toolSlug: string) =>
    fetchApi<{ ok: boolean }>(
      `/favorites/${toolSlug}?user_id=${USER_ID}`,
      { method: "DELETE" }
    ),
}
