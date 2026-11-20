from __future__ import annotations

import html
import json
from pathlib import Path


def escape(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    content_path = root / "build" / "slides_content.json"
    output_path = root / "build" / "slides.html"

    if not content_path.exists():
        raise FileNotFoundError(f"Missing content file: {content_path.as_posix()}")

    data = json.loads(content_path.read_text(encoding="utf-8"))
    slides = data.get("slides", [])
    if not slides:
        raise ValueError("No slides found in slides_content.json")

    slide_html = []
    for index, slide in enumerate(slides, start=1):
        bullets = "".join(
            f"<li>{escape(bullet)}</li>"
            for bullet in slide.get("bullets", [])
        )
        sources = " · ".join(
            f"[{escape(source)}]"
            for source in slide.get("source_files", [])
        )
        slide_html.append(
            f"""
<section class="slide" data-slide="{index}" aria-label="投影片 {index}">
  <div class="slide-accent"></div>
  <p class="kicker">PAPERWIKI · 教學簡報 {index:02d}/{len(slides):02d}</p>
  <h1>{escape(slide.get("title"))}</h1>
  <p class="analogy">{escape(slide.get("analogy"))}</p>
  <ul>{bullets}</ul>
  <aside class="limitation">
    <strong>邊界提醒</strong>
    <span>{escape(slide.get("limitation_note"))}</span>
  </aside>
  <footer>
    <div class="sources">{sources}</div>
  </footer>
</section>"""
        )

    document = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Representation Learning — 教學簡報</title>
  <style>
    :root {{
      --paper:#FAF8F5; --surface:#FFFFFF; --ink:#2D2A26; --muted:#6E6A63;
      --line:#E6E2D8; --accent:#D97757; --sage:#4A6B5D;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; overflow:hidden; background:var(--paper); color:var(--ink); font-family:Inter,"Noto Sans TC",sans-serif; }}
    .deck {{ height:100vh; }}
    .slide {{ display:none; position:relative; width:min(1120px,calc(100vw - 64px)); height:calc(100vh - 64px); margin:32px auto; padding:68px 82px 44px; border:1px solid var(--line); border-radius:18px; background:var(--surface); box-shadow:0 18px 46px rgba(58,45,32,.08); }}
    .slide.is-active {{ display:block; }}
    .slide-accent {{ position:absolute; left:82px; top:38px; width:54px; height:4px; border-radius:999px; background:var(--accent); }}
    .kicker {{ margin:0 0 18px; color:var(--accent); font-size:12px; font-weight:700; letter-spacing:.12em; }}
    h1 {{ max-width:900px; margin:0 0 22px; font-family:Merriweather,"Noto Serif TC",serif; font-size:clamp(38px,5vw,64px); line-height:1.18; letter-spacing:-.04em; }}
    .analogy {{ max-width:900px; margin:0 0 28px; color:var(--muted); font-size:20px; line-height:1.55; }}
    ul {{ margin:0; padding-left:26px; }}
    li {{ margin:12px 0; font-size:clamp(18px,2vw,26px); line-height:1.45; }}
    li::marker {{ color:var(--accent); }}
    .limitation {{ position:absolute; left:82px; right:82px; bottom:88px; display:flex; gap:14px; align-items:flex-start; padding:16px 18px; border:1px solid #E9E1BB; border-radius:12px; background:#FFF9DB; color:#5E5637; font-size:15px; line-height:1.5; }}
    .limitation strong {{ flex:none; color:var(--sage); }}
    footer {{ position:absolute; left:82px; right:82px; bottom:35px; display:flex; justify-content:flex-end; }}
    .sources {{ max-width:760px; color:var(--muted); font-size:11px; line-height:1.45; text-align:right; }}
    .nav {{ position:fixed; left:50%; bottom:12px; z-index:5; display:flex; gap:8px; transform:translateX(-50%); }}
    .nav button {{ min-width:42px; height:32px; border:1px solid var(--line); border-radius:999px; background:rgba(255,255,255,.92); color:var(--ink); cursor:pointer; }}
    .nav button:hover {{ border-color:var(--accent); color:var(--accent); }}
    .counter {{ display:grid; min-width:64px; place-items:center; color:var(--muted); font-size:12px; }}
    @media (max-width:760px) {{
      .slide {{ width:calc(100vw - 24px); height:calc(100vh - 56px); margin:20px 12px 36px; padding:48px 28px 36px; }}
      .slide-accent {{ left:28px; top:26px; }}
      h1 {{ font-size:34px; }}
      .analogy {{ font-size:16px; }}
      li {{ font-size:17px; }}
      .limitation {{ left:28px; right:28px; bottom:82px; font-size:13px; }}
      footer {{ left:28px; right:28px; bottom:38px; }}
      .sources {{ font-size:9px; }}
    }}
  </style>
</head>
<body>
  <main class="deck" aria-label="Representation Learning 教學簡報">
{''.join(slide_html)}
  </main>
  <nav class="nav" aria-label="投影片導覽">
    <button type="button" data-prev aria-label="上一頁">←</button>
    <span class="counter" data-counter>1 / {len(slides)}</span>
    <button type="button" data-next aria-label="下一頁">→</button>
  </nav>
  <script>
    const slides = [...document.querySelectorAll(".slide")];
    const counter = document.querySelector("[data-counter]");
    let current = 0;

    function show(index) {{
      current = (index + slides.length) % slides.length;
      slides.forEach((slide, i) => slide.classList.toggle("is-active", i === current));
      counter.textContent = `${{current + 1}} / ${{slides.length}}`;
      history.replaceState(null, "", `#${{current + 1}}`);
    }}

    document.querySelector("[data-prev]").addEventListener("click", () => show(current - 1));
    document.querySelector("[data-next]").addEventListener("click", () => show(current + 1));
    document.addEventListener("keydown", event => {{
      if (event.key === "ArrowLeft" || event.key === "PageUp") show(current - 1);
      if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") show(current + 1);
      if (event.key === "Home") show(0);
      if (event.key === "End") show(slides.length - 1);
    }});

    const hashIndex = Number(location.hash.replace("#", ""));
    show(Number.isInteger(hashIndex) && hashIndex >= 1 && hashIndex <= slides.length ? hashIndex - 1 : 0);
  </script>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
    print(f"[assemble_slides] Wrote {output_path.as_posix()} with {len(slides)} slides")


if __name__ == "__main__":
    main()