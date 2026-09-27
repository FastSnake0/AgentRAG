import arxiv
from pathlib import Path
from urllib.request import urlretrieve  # добавляем импорт

PDF_DIR = Path("data/pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)

def download_papers(query: str, max_results: int = 20):
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    manifest = []
    for result in client.results(search):
        paper_id = result.get_short_id()
        pdf_path = PDF_DIR / f"{paper_id}.pdf"
        # Скачиваем PDF по прямой ссылке
        urlretrieve(result.pdf_url, str(pdf_path))
        manifest.append({
            "id": paper_id,
            "title": result.title,
            "url": result.entry_id,
            "pdf_path": str(pdf_path),
        })
    return manifest