from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def check_outline(
    outline_path: Path = Path("build/outline.json"),
    notes_dir: Path = Path("notes"),
    log_path: Path = Path("logs/check_outline.json"),
    min_slides: int = 6,
    max_slides: int = 12,
) -> dict:
    valid_notes = {p.name for p in notes_dir.glob("*.md")}
    checks: list[dict] = []
    errors: list[str] = []
    warnings: list[str] = []

    if not outline_path.exists():
        msg = f"找不到大綱檔案：{outline_path.as_posix()}"
        errors.append(msg)
        checks.append({"name": "outline_exists", "status": "FAIL", "detail": msg})
    else:
        data = json.loads(outline_path.read_text(encoding="utf-8"))
        slides = data.get("slides", [])

        # 1. 頁數範圍檢查
        if min_slides <= len(slides) <= max_slides:
            checks.append({
                "name": "slide_count_range",
                "status": "PASS",
                "detail": f"共 {len(slides)} 頁（允許區間 {min_slides}~{max_slides}）",
            })
        else:
            msg = f"頁數 {len(slides)} 超出允許區間 {min_slides}~{max_slides}"
            errors.append(msg)
            checks.append({"name": "slide_count_range", "status": "FAIL", "detail": msg})

        # 2. 每頁欄位與 source_files 合法性檢查
        covered_sources: set[str] = set()
        invalid_refs: list[str] = []
        missing_fields: list[str] = []

        for idx, slide in enumerate(slides, start=1):
            sid = slide.get("slide_id", idx)
            title = (slide.get("title") or "").strip()
            goal = (slide.get("goal") or "").strip()
            key_points = slide.get("key_points") or []
            sources = slide.get("source_files") or []

            if not title or not goal or not key_points or not sources:
                missing_fields.append(f"第 {sid} 頁缺少必要欄位（title/goal/key_points/source_files）")

            for src in sources:
                if src not in valid_notes:
                    invalid_refs.append(f"第 {sid} 頁引用不存在的來源：{src}")
                else:
                    covered_sources.add(src)

        if missing_fields:
            errors.extend(missing_fields)
            checks.append({"name": "slide_schema", "status": "FAIL", "detail": "；".join(missing_fields)})
        else:
            checks.append({"name": "slide_schema", "status": "PASS", "detail": "所有投影片必要欄位齊全"})

        if invalid_refs:
            errors.extend(invalid_refs)
            checks.append({"name": "source_validity", "status": "FAIL", "detail": "；".join(invalid_refs)})
        else:
            checks.append({"name": "source_validity", "status": "PASS", "detail": "所有 source_files 皆存在於 notes/"})

        # 3. 知識庫覆蓋率檢查
        uncovered = sorted(valid_notes - covered_sources)
        if uncovered:
            msg = f"大綱尚未涵蓋的 notes 檔案：{uncovered}"
            errors.append(msg)
            checks.append({"name": "source_coverage", "status": "FAIL", "detail": msg})
        else:
            checks.append({
                "name": "source_coverage",
                "status": "PASS",
                "detail": f"已涵蓋全部 {len(valid_notes)} 篇 notes",
            })

        # 4. 連續重複單一來源提醒
        consecutive_dups = 0
        for i in range(1, len(slides)):
            prev_s = slides[i - 1].get("source_files") or []
            curr_s = slides[i].get("source_files") or []
            if prev_s and prev_s == curr_s:
                consecutive_dups += 1
        if consecutive_dups >= 2:
            msg = f"連續 {consecutive_dups} 次相鄰投影片使用完全相同的 source_files"
            warnings.append(msg)
            checks.append({"name": "pacing_check", "status": "WARN", "detail": msg})
        else:
            checks.append({"name": "pacing_check", "status": "PASS", "detail": "投影片來源節奏正常"})

    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    report = {
        "step": "check_outline",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": status,
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    res = check_outline()
    print(f"[check_outline] {res['overall_status']}")
    for c in res["checks"]:
        print(f"  - {c['name']}: {c['status']} ({c['detail']})")