# from langchain.tools import tool
from ddgs import DDGS
import trafilatura
from config import Settings
from pathlib import Path

settings = Settings()

def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n\n[truncated to {limit} characters]"

# @tool
def web_search(query: str) -> list[dict]:
    """Search in the web and return compact results with title, url, and snippet."""
    try:
        results = DDGS().text(query, max_results=settings.max_search_results)
        normalized: list[dict[str, str]] = []
        for item in results:
            normalized.append(
                {
                    "title": str(item.get("title", "")).strip(),
                    "url": str(item.get("href", "")).strip(),
                    "snippet": str(item.get("body", "")).strip(),
                }
            )
        print(f"Founed {len(normalized)} web sites")
        if not normalized:
            return [{"title": "No results", "url": "", "snippet": f"No results found for query: {query}"}]
        return normalized
    except Exception as e:
        return [
            {
                "title": "Search error",
                "url": "",
                "snippet": f"web_search failed for query '{query}': {e}",
            }
        ]

# @tool
def read_url(url: str) -> str:
    "Приймає URL і повертає текст сторінки"
    """Fetch a URL and extract the page content. Returns a compact, truncated text payload or a readable error."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return f"Could not download URL: {url}"
        

        extracted = trafilatura.extract(downloaded)
        if not extracted:
                return f"Could not extract meaningful text from URL: {url}"
        
        return _truncate(extracted, settings.max_url_content_length)
    except Exception as e:
         return _truncate(f"read_url failed for '{url}': {e}", settings.max_url_content_length)

# @tool
def write_report(filename: str, content: str) -> str:
    """Write the final Markdown report to the output directory and return the absolute path."""
    try:
        safe_name = Path(filename).name
        if not safe_name.endswith(".md"):
            safe_name += ".md"

        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict) and "text" in block:
                    text_parts.append(block["text"])
                else:
                    text_parts.append(str(block))
            content = "\n".join(text_parts)

        output_path = Path(settings.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        output_path = output_path / safe_name
        output_path.write_text(content, encoding="utf-8")
        return str(output_path.resolve())
    except Exception as e:
         return f"write_report failed for file '{filename}' in folder '{settings.output_dir}': {e}"    