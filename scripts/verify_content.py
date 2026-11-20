from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def verify_content(
    content_path: Path = Path("build/slides_content.json"),
    notes_dir: Path = Path("notes"),
    log_path: Path = Path("logs/verify_content.json"),
    max_bullets: int = 4,
    max_bullet_chars: int = 60,
    max_slide_total_chars: int = 240,
) -> dict:
    valid_notes = {p.name for p in notes_dir.glob("*.md")}
    checks: list[dict] = []
    errors: list[str] = []
    warnings: list[str] = []

    if not content_path.exists():
        msg = f"找不到逐頁內容檔案：{content_path.as_posix()}"
        errors.append(msg)
        checks.append({"name": "content_exists", "status": "FAIL", "detail": msg})
    else:
        data = json.loads(content_path.read_text(encoding="utf-8"))
        slides = data.get("slides", [])

        source_violations: list[str] = []
        bullet_violations: list[str] = []
        char_violations: list[str] = []

        for idx, slide in enumerate(slides, start=1):
            sid = slide.get("slide_id", idx)
            title = (slide.get("title") or "").strip()
            analogy = (slide.get("analogy") or "").strip()
            limitation = (slide.get("limitation_note") or "").strip()
            bullets = slide.get("bullets") or []
            sources = slide.get("source_files") or []

            if not title:
                source_violations.append(f"第 {sid} 頁缺少 title")

            if not sources:
                source_violations.append(f"第 {sid} 頁缺少 source_files")
            else:
                for src in sources:
                    if src not in valid_notes:
                        source_violations.append(f"第 {sid} 頁引用不存在的來源：{src}")

            if len(bullets) > max_bullets:
                bullet_violations.append(f"第 {sid} 頁條列數 {len(bullets)} 超過上限 {max_bullets}")

            for b_idx, b in enumerate(bullets, start=1):
                b_str = (b or "").strip()
                if len(b_str) > max_bullet_chars:
                    char_violations.append(
                        f"第 {sid} 頁第 {b_idx} 點字數 {len(b_str)} 超過上限 {max_bullet_chars}"
                    )

            total_chars = (
                len(title)
                + len(analogy)
                + len(limitation)
                + sum(len((b or "").strip()) for b in bullets)
            )
            if total_chars > max_slide_total_chars:
                char_violations.append(
                    f"第 {sid} 頁總字數 {total_chars} 超過上限 {max_slide_total_chars}"
                )

        if source_violations:
            errors.extend(source_violations)
            checks.append({"name": "slide_sources_and_title", "status": "FAIL", "detail": "；".join(source_violations)})
        else:
            checks.append({"name": "slide_sources_and_title", "status": "PASS", "detail": "每頁標題與來源皆合法"})

        if bullet_violations:
            errors.extend(bullet_violations)
            checks.append({"name": "bullet_count", "status": "FAIL", "detail": "；".join(bullet_violations)})
        else:
            checks.append({"name": "bullet_count", "status": "PASS", "detail": f"每頁條列數皆在 {max_bullets} 點以內"})

        if char_violations:
            warnings.extend(char_violations)
            checks.append({"name": "text_length_guardrail", "status": "WARN", "detail": "；".join(char_violations)})
        else:
            checks.append({"name": "text_length_guardrail", "status": "PASS", "detail": "每頁字數皆在安全範圍內"})

    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    report = {
        "step": "verify_content",
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
    res = verify_content()
    print(f"[verify_content] {res['overall_status']}")
    for c in res["checks"]:
        print(f"  - {c['name']}: {c['status']} ({c['detail']})")