import json

from jinja2 import Template
from weasyprint import HTML

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
    def export(self, entry: dict, fmt: str) -> tuple[str, str, str]:
        context = {
            "tool_name": entry["tool_slug"].replace("-", " ").title(),
            "input": entry["input"],
            "output": entry["output"],
            "provider": entry["provider"],
            "model": entry["model"],
        }

        if fmt == "markdown":
            content = Template(MARKDOWN_TEMPLATE).render(**context)
            return content, f"{entry['tool_slug']}-export.md", "text/markdown"
        elif fmt == "txt":
            content = Template(TXT_TEMPLATE).render(**context)
            return content, f"{entry['tool_slug']}-export.txt", "text/plain"
        elif fmt == "json":
            data = {
                "tool": entry["tool_slug"],
                "input": entry["input"],
                "output": entry["output"],
                "provider": entry["provider"],
                "model": entry["model"],
                "created_at": entry["created_at"],
            }
            content = json.dumps(data, indent=2, ensure_ascii=False)
            return content, f"{entry['tool_slug']}-export.json", "application/json"
        elif fmt == "pdf":
            html_content = Template(MARKDOWN_TEMPLATE).render(**context)
            html_body = f"""<!DOCTYPE html>
<html><body style="font-family: sans-serif; max-width: 800px; margin: 2em auto;">
<pre style="white-space: pre-wrap;">{html_content}</pre>
</body></html>"""
            pdf_bytes = HTML(string=html_body).write_pdf()
            return pdf_bytes, f"{entry['tool_slug']}-export.pdf", "application/pdf"
        else:
            raise ValueError(f"Format non supporté : {fmt}")
