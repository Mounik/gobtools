import json
from uuid import UUID

from jinja2 import Template
from weasyprint import HTML

from app.repositories.history_repo import HistoryRepository

MARKDOWN_TEMPLATE = """# {{ tool_name }}

**Entrée :** {{ input }}

**Sortie :**
{{ output }}

---
*Généré par GobTools via {{ provider }}/{{ model }}*
"""

TXT_TEMPLATE = """{{ tool_name }}
{{ "=" * (tool_name|length) }}

Entrée :
{{ input }}

Sortie :
{{ output }}

Généré par GobTools via {{ provider }}/{{ model }}
"""


class ExportService:
    def __init__(self, history_repo: HistoryRepository):
        self.history_repo = history_repo

    async def export(
        self, history_id: UUID, user_id: UUID, fmt: str
    ) -> tuple[str, str, str]:
        items, _ = await self.history_repo.list_by_user(user_id, page=1, page_size=1000)
        entry = next((h for h in items if h.id == history_id), None)
        if entry is None:
            raise ValueError("Entrée d'historique introuvable")

        context = {
            "tool_name": entry.tool_slug.replace("-", " ").title(),
            "input": entry.input,
            "output": entry.output,
            "provider": entry.provider,
            "model": entry.model,
        }

        if fmt == "markdown":
            content = Template(MARKDOWN_TEMPLATE).render(**context)
            return content, f"{entry.tool_slug}-export.md", "text/markdown"
        elif fmt == "txt":
            content = Template(TXT_TEMPLATE).render(**context)
            return content, f"{entry.tool_slug}-export.txt", "text/plain"
        elif fmt == "json":
            data = {
                "tool": entry.tool_slug,
                "input": entry.input,
                "output": entry.output,
                "provider": entry.provider,
                "model": entry.model,
                "created_at": entry.created_at.isoformat(),
            }
            content = json.dumps(data, indent=2, ensure_ascii=False)
            return content, f"{entry.tool_slug}-export.json", "application/json"
        elif fmt == "pdf":
            html_content = Template(MARKDOWN_TEMPLATE).render(**context)
            html_body = f"""<!DOCTYPE html>
<html><body style="font-family: sans-serif; max-width: 800px; margin: 2em auto;">
<pre style="white-space: pre-wrap;">{html_content}</pre>
</body></html>"""
            pdf_bytes = HTML(string=html_body).write_pdf()
            return pdf_bytes, f"{entry.tool_slug}-export.pdf", "application/pdf"
        else:
            raise ValueError(f"Format non supporté : {fmt}")
