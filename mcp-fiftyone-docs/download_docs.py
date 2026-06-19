"""download_docs.py — Download key FiftyOne docs and build a local search index."""
import json
import os
import re
import textwrap
from pathlib import Path
from urllib.parse import urljoin, urlparse

import html2text
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://docs.voxel51.com"
DOCS_DIR = Path("docs")
INDEX_FILE = Path("index.json")
CHAR_LIMIT = 25_000

# Key docs to download (extracted from the official docs sidebar)
URL_PATHS = [
    # Getting Started
    "getting_started/index.html",
    "getting_started/object_detection/index.html",
    "getting_started/object_detection/01_loading_datasets.html",
    "getting_started/object_detection/02_adding_detections.html",
    "getting_started/object_detection/03_finding_mistakes.html",
    "getting_started/object_detection/04_evaluating_detections.html",
    "getting_started/segmentation/index.html",
    "getting_started/segmentation/01_intro.html",
    "getting_started/segmentation/02_explore.html",
    "getting_started/segmentation/03_sam2.html",
    "getting_started/annotation/index.html",
    "getting_started/annotation/01_quickstart.html",
    "getting_started/annotation/04_annotation_2d.html",
    "getting_started/annotation/05_annotation_3d.html",
    "getting_started/depth_estimation/index.html",
    "getting_started/depth_estimation/01_loading_depth_data.html",
    "getting_started/depth_estimation/02_depth_estimation.html",
    "getting_started/model_evaluation/index.html",
    "getting_started/model_evaluation/01_basic_evaluation.html",
    "getting_started/model_evaluation/02_advanced_analysis.html",
    "getting_started/threed_visual_ai/index.html",
    "getting_started/threed_visual_ai/01_getting_started_3d.html",
    "getting_started/threed_visual_ai/02_loading_annotations.html",
    "getting_started/medical_imaging/index.html",
    "getting_started/medical_imaging/01_getting_started.html",
    # Tutorials
    "tutorials/index.html",
    "tutorials/evaluate_detections.html",
    "tutorials/evaluate_classifications.html",
    "tutorials/image_embeddings.html",
    "tutorials/cvat_annotation.html",
    "tutorials/labelbox_annotation.html",
    "tutorials/detectron2.html",
    "tutorials/uniqueness.html",
    "tutorials/classification_mistakes.html",
    "tutorials/detection_mistakes.html",
    "tutorials/clustering.html",
    "tutorials/anomaly_detection.html",
    "tutorials/zero_shot_classification.html",
    "tutorials/dinov3.html",
    "tutorials/yolov8.html",
    "tutorials/data_augmentation.html",
    # Recipes
    "recipes/index.html",
    "recipes/creating_views.html",
    "recipes/adding_detections.html",
    "recipes/adding_classifications.html",
    "recipes/convert_datasets.html",
    "recipes/merge_datasets.html",
    "recipes/custom_importer.html",
    "recipes/custom_exporter.html",
    "recipes/image_deduplication.html",
    "recipes/remove_duplicate_annos.html",
    # Cheat Sheets
    "cheat_sheets/index.html",
    "cheat_sheets/filtering_cheat_sheet.html",
    "cheat_sheets/views_cheat_sheet.html",
    "cheat_sheets/pandas_vs_fiftyone.html",
    # User Guide
    "user_guide/index.html",
    "user_guide/basics.html",
    "user_guide/import_datasets.html",
    "user_guide/using_datasets.html",
    "user_guide/using_views.html",
    "user_guide/evaluation.html",
    "user_guide/annotation.html",
    "user_guide/app.html",
    "user_guide/export_datasets.html",
    "user_guide/using_aggregations.html",
    # Brain / Zoo / Integrations
    "brain.html",
    "dataset_zoo/overview.html",
    "model_zoo/overview.html",
    "integrations/coco.html",
    "integrations/ultralytics.html",
    "integrations/huggingface.html",
    "integrations/cvat.html",
    "cli/index.html",
]


def fetch_page(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Remove nav / header / footer noise
    for selector in ["nav", "header", "footer", "#sidebar", ".toc"]:
        for tag in soup.select(selector):
            tag.decompose()
    # Prefer main content area
    main = soup.find("main") or soup.find("div", class_=re.compile("main|content|document")) or soup.find("body")
    if not main:
        main = soup
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    return h.handle(str(main))


def save_doc(path: str, markdown: str) -> Path:
    relative = path.replace(".html", ".md")
    out_path = DOCS_DIR / relative
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    return out_path


def build_index() -> list[dict]:
    index = []
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        rel_path = str(md_file.relative_to(DOCS_DIR)).replace("\\", "/")
        # Derive title from first H1
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else rel_path
        index.append({
            "path": rel_path,
            "title": title,
            "category": rel_path.split("/")[0],
            "content": content,
        })
    return index


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    print(f"Downloading {len(URL_PATHS)} pages from {BASE_URL} ...")
    for path in URL_PATHS:
        url = urljoin(BASE_URL, path)
        try:
            html = fetch_page(url)
            md = html_to_markdown(html)
            out = save_doc(path, md)
            print(f"  [OK] {out}")
        except Exception as exc:
            print(f"  [ERR] {path}: {exc}")

    print("\nBuilding index.json ...")
    index = build_index()
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [OK] Indexed {len(index)} documents -> {INDEX_FILE}")


if __name__ == "__main__":
    main()
