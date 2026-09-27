import os
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

import json
from pathlib import Path
from typing import List, Dict, Any
import pymupdf4llm
from tqdm import tqdm

CORPUS_PATH = Path("data/structured_corpus.jsonl")

def extract_paper(pdf_path: str, paper_meta: Dict[str, Any]) -> Dict[str, Any]:
    try:
        md_text = pymupdf4llm.to_markdown(pdf_path, show_progress=False)
    except Exception as e:
        print(f"⚠️ Ошибка парсинга {pdf_path}: {e}")
        return None

    return {
        "doc_id": paper_meta["id"],
        "title": paper_meta["title"],
        "url": paper_meta["url"],
        "text": md_text,
    }

def build_corpus(manifest: List[Dict[str, Any]], output_path: Path = CORPUS_PATH):
    failed = []
    count = 0
    
    with open(output_path, "w", encoding="utf-8") as f:
        for paper in tqdm(manifest, desc="Building corpus"):
            record = extract_paper(paper["pdf_path"], paper)
            if record is None:
                failed.append(paper["id"])
                continue
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    
    print(f"\n✅ Корпус создан: {count} статей из {len(manifest) - len(failed)}")
    if failed:
        print(f"❌ Не удалось обработать: {failed}")
    
    return count