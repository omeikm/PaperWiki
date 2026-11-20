from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


def parse_note_metadata(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    title_match = re.search(r"-\s*\*\*Title:\*\*\s*(.+)", text)
    venue_match = re.search(r"-\s*\*\*Venue & Year:\*\*\s*(.+)", text)
    tags_match = re.search(r"-\s*\*\*Tags:\*\*\s*(.+)", text)

    title = title_match.group(1).strip() if title_match else md_path.stem
    venue_year = venue_match.group(1).strip() if venue_match else ""
    tags = tags_match.group(1).strip() if tags_match else ""

    year_match = re.search(r"\b(19|20)\d{2}\b", venue_year)
    year = year_match.group(0) if year_match else ""

    return {
        "id": md_path.stem,
        "filename": md_path.name,
        "path": md_path.as_posix(),
        "title": title,
        "year": year,
        "venue_and_year": venue_year,
        "tags": tags,
    }


def write_wiki_index(notes_meta: list[dict], index_path: Path) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# LLM Wiki Index",
        "",
        "> 由 `scripts/harness_step1_wiki.py` 自動根據 `notes/` 產出與同步。",
        "",
        f"- 收錄筆記數：{len(notes_meta)}",
        "",
        "| filename | year | title | note_path |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for item in notes_meta:
        safe_title = item["title"].replace("|", "\\|")
        lines.append(
            f"| `{item['filename']}` | {item['year']} | {safe_title} | `{item['path']}` |"
        )
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def check_count_phrases(synthesis_text: str, total_notes: int) -> list[str]:
    warnings: list[str] = []
    # 檢查常見中文數量詞如「前四篇」、「前五篇」、「共五篇」
    cn_num_map = {
        "一": 1, "二": 2, "兩": 2, "三": 3, "四": 4,
        "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
    }
    for match in re.finditer(r"(前|共)([一二兩三四五六七八九十\d]+)篇", synthesis_text):
        kind, raw_num = match.group(1), match.group(2)
        if raw_num.isdigit():
            num = int(raw_num)
        else:
            num = cn_num_map.get(raw_num, -1)
        if num == -1:
            continue
        if kind == "共" and num != total_notes:
            warnings.append(
                f"數量詞提示：文內出現「{match.group(0)}」，但目前 notes/ 共有 {total_notes} 篇。"
            )
        elif kind == "前" and num >= total_notes:
            warnings.append(
                f"數量詞提示：文內出現「{match.group(0)}」，但目前 notes/ 共有 {total_notes} 篇。"
            )
    return warnings


def run_step1(
    notes_dir: Path = Path("notes"),
    wiki_dir: Path = Path("wiki"),
    log_path: Path = Path("logs/step1_wiki_check.json"),
) -> dict:
    note_files = sorted(notes_dir.glob("*.md"))
    notes_meta = [parse_note_metadata(p) for p in note_files]
    valid_filenames = {m["filename"] for m in notes_meta}

    index_path = wiki_dir / "index.md"
    manifest_path = wiki_dir / "manifest.json"
    synthesis_path = wiki_dir / "synthesis.md"

    write_wiki_index(notes_meta, index_path)

    checks: list[dict] = []
    errors: list[str] = []
    warnings: list[str] = []

    # 1. 筆記數量檢查
    if len(notes_meta) >= 5:
        checks.append({"name": "min_notes_count", "status": "PASS", "detail": f"共 {len(notes_meta)} 篇筆記"})
    else:
        msg = f"筆記數不足 5 篇（目前 {len(notes_meta)} 篇）"
        errors.append(msg)
        checks.append({"name": "min_notes_count", "status": "FAIL", "detail": msg})

    # 2. synthesis.md 存在性與引用檢查
    cited_counts = {name: 0 for name in valid_filenames}
    if not synthesis_path.exists():
        msg = f"找不到 {synthesis_path.as_posix()}"
        errors.append(msg)
        checks.append({"name": "synthesis_exists", "status": "FAIL", "detail": msg})
    else:
        synth_text = synthesis_path.read_text(encoding="utf-8")
        citations = re.findall(r"\[([^\[\]]+?\.md)\]", synth_text)

        invalid_citations = [c for c in citations if c not in valid_filenames]
        if invalid_citations:
            msg = f"發現不存在的引用檔名：{sorted(set(invalid_citations))}"
            errors.append(msg)
            checks.append({"name": "citation_validity", "status": "FAIL", "detail": msg})
        else:
            checks.append({"name": "citation_validity", "status": "PASS", "detail": f"共 {len(citations)} 處引用皆合法"})

        for c in citations:
            if c in cited_counts:
                cited_counts[c] += 1

        uncited = [name for name, cnt in cited_counts.items() if cnt == 0]
        if uncited:
            msg = f"以下筆記尚未在 synthesis.md 中被引用：{uncited}"
            errors.append(msg)
            checks.append({"name": "citation_coverage", "status": "FAIL", "detail": msg})
        else:
            checks.append({"name": "citation_coverage", "status": "PASS", "detail": "所有筆記皆已被引用"})

        required_sections = [
            "主線演進脈絡",
            "跨篇方法與目標差異",
            "新手教學講解順序",
            "侷限性與防過度宣稱提醒",
        ]
        missing_sections = [s for s in required_sections if s not in synth_text]
        if missing_sections:
            msg = f"synthesis.md 缺少章節：{missing_sections}"
            errors.append(msg)
            checks.append({"name": "required_sections", "status": "FAIL", "detail": msg})
        else:
            checks.append({"name": "required_sections", "status": "PASS", "detail": "四個核心章節皆存在"})

        placeholders = [kw for kw in ["TODO", "FIXME", "待補充"] if kw in synth_text]
        if placeholders:
            msg = f"synthesis.md 含未完成標記：{placeholders}"
            warnings.append(msg)
            checks.append({"name": "placeholders", "status": "WARN", "detail": msg})
        else:
            checks.append({"name": "placeholders", "status": "PASS", "detail": "無殘留未完成標記"})

        count_warns = check_count_phrases(synth_text, len(notes_meta))
        if count_warns:
            warnings.extend(count_warns)
            checks.append({"name": "count_consistency", "status": "WARN", "detail": " / ".join(count_warns)})
        else:
            checks.append({"name": "count_consistency", "status": "PASS", "detail": "數量詞檢查通過"})

    for m in notes_meta:
        m["synthesis_citation_count"] = cited_counts.get(m["filename"], 0)

    manifest_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "total_notes": len(notes_meta),
                "notes": notes_meta,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    overall_status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    report = {
        "step": "step1_wiki",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
        "artifacts": {
            "index_md": index_path.as_posix(),
            "manifest_json": manifest_path.as_posix(),
        },
    }

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    res = run_step1()
    print(f"[Step 1 Status] {res['overall_status']}")
    for c in res["checks"]:
        print(f"  - {c['name']}: {c['status']} ({c['detail']})")