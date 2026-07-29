import io

import fitz


def extract_text_from_pdf(content: bytes, max_pages: int = 50) -> str:
    doc = fitz.open(stream=content, filetype="pdf")
    pages = min(len(doc), max_pages)
    text_parts: list[str] = []
    for i in range(pages):
        page = doc.load_page(i)
        text = page.get_text().strip()
        if text:
            text_parts.append(f"--- Page {i + 1} ---\n{text}")
    doc.close()
    return "\n\n".join(text_parts)
