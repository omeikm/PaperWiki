from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


def verify_html(
    html_path: Path = Path("build/slides.html"),
    content_path: Path = Path("build/slides_content.json"),
    notes_dir: Path = Path("notes"),
    log_path: Path = Path("logs/verify_html.json"),
) -> dict:
    checks: list[dict] = []
    errors: list[str] = []
    warnings: list[str] = []

    if not html_path.exists():
        errors.append(f"找不到 HTML：{html_path.as_posix()}")
    else:
        text = html_path.read_text(encoding="utf-8")
        if not content_path.exists():
            errors.append(f"找不到內容檔案：{content_path.as_posix()}")
            content_slides = []
        else:
            content_slides = json.loads(content_path.read_text(encoding="utf-8")).get("slides", [])

        section_count = len(re.findall(r'<section class="slide"', text))
        if section_count != len(content_slides):
            errors.append(
                f"HTML 投影片數 {section_count} 與 JSON 投影片數 {len(content_slides)} 不一致"
            )
        else:
            checks.append({
                "name": "slide_count",
                "status": "PASS",
                "detail": f"HTML 與 JSON 均為 {section_count} 頁",
            })

        placeholders = [token for token in ("TODO", "FIXME", "待補充") if token in text]
        if placeholders:
            errors.append(f"HTML 含未完成標記：{placeholders}")
        else:
            checks.append({"name": "placeholder_check", "status": "PASS", "detail": "無殘留未完成標記"})

        valid_notes = {p.name for p in notes_dir.glob("*.md")}
        refs = re.findall(r"\[([^\[\]]+\.md)\]", text)
        invalid_refs = sorted(set(refs) - valid_notes)
        if invalid_refs:
            errors.append(f"HTML 含不存在的來源：{invalid_refs}")
        else:
            checks.append({"name": "source_markers", "status": "PASS", "detail": "所有 HTML 來源標記皆合法"})

        nav_missing = [
            marker for marker in ('back-wiki', 'data-prev', 'data-next', 'data-counter')
            if marker not in text
        ]
        if nav_missing:
            errors.append(f"HTML 缺少導覽控制：{nav_missing}")
        else:
            checks.append({"name": "navigation", "status": "PASS", "detail": "前後頁與頁碼控制皆存在"})

    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    report = {
        "step": "verify_html",
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
    res = verify_html()
    print(f"[verify_html] {res['overall_status']}")
    for check in res["checks"]:
        print(f"  - {check['name']}: {check['status']} ({check['detail']})")
