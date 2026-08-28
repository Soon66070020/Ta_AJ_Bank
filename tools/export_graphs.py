#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ดึงกราฟทั้งหมดจาก notebook ในโครงการ มารวมไว้ที่โฟลเดอร์ graphs/

Export every chart embedded in the repository's notebooks into `graphs/`,
one subfolder per project group.

ทำไมต้องมีสคริปต์นี้ (Why this exists)
--------------------------------------
Plotly renderer 'notebook' ฝังไลบรารี plotly.js (~4.85 MB) ลงใน cell output
ถ้าบันทึกกราฟตรง ๆ ไฟล์เดียวจะใหญ่ 4.85 MB และ 135 กราฟจะกินพื้นที่ ~650 MB
สคริปต์นี้จึงดึงเฉพาะ `<div class="plotly-graph-div">` + `Plotly.newPlot(...)`
แล้วประกอบเป็นหน้า HTML ใหม่ที่โหลด plotly.js จาก CDN แทน — เหลือไฟล์ละ ~10-200 KB

การใช้งาน (Usage)
-----------------
    .\venv\Scripts\python.exe tools\export_graphs.py

รันซ้ำได้ตลอด — จะล้างโฟลเดอร์ graphs/ แล้วสร้างใหม่จาก notebook ปัจจุบัน
"""

from __future__ import annotations

import base64
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "graphs"

PLOTLY_CDN = "https://cdn.plot.ly/plotly-3.7.0.min.js"

# โฟลเดอร์กลุ่มงาน → ชื่อที่แสดงในดัชนี
GROUPS: list[tuple[str, str]] = [
    ("กรมส่งเสริมการเกษตร", "🌾 กรมส่งเสริมการเกษตร (DOAE)"),
    ("เกษตรกรรม", "🐃 เกษตรกรรม / ปศุสัตว์ (DLD)"),
    ("ควบคุมโรค", "🦟 ควบคุมโรค (DDC)"),
    ("DGA_2", "🏢 DGA_2 — กรมสรรพากร & มาตรวิทยา"),
    ("DGA_3", "📈 DGA_3 — ดัชนีเศรษฐกิจ & สวัสดิการสังคม"),
]

SKIP_DIRS = {"venv", ".ipynb_checkpoints", "__pycache__", "graphs", ".git"}

# อักขระที่ใช้เป็นชื่อไฟล์บน Windows ไม่ได้
BAD_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def clean_title(text: str) -> str:
    """ตัด HTML tag และ <br> ออกจากชื่อกราฟ

    ต้องทำก่อน slugify เสมอ — ถ้าลบอักขระ < > ทิ้งก่อน tag จะเหลือเศษ
    เช่น '<b>ยอดขาย</b>' กลายเป็น 'bยอดขายb'
    """
    text = re.sub(r"<br\s*/?>", " ", text or "", flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def slugify(text: str, maxlen: int = 60) -> str:
    """ทำชื่อไฟล์ที่ปลอดภัย โดยยังคงตัวอักษรไทยไว้"""
    text = clean_title(text)
    text = BAD_CHARS.sub("", text)
    text = re.sub(r"\s+", "_", text.strip())
    text = text.strip("._-")
    if len(text) > maxlen:
        text = text[:maxlen].rstrip("._-")
    return text or "chart"


def iter_notebooks() -> list[Path]:
    out = []
    for p in sorted(REPO.rglob("*.ipynb")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return out


def group_of(nb: Path) -> tuple[str, str] | None:
    rel = nb.relative_to(REPO)
    if not rel.parts:
        return None
    top = rel.parts[0]
    for key, label in GROUPS:
        if top == key:
            return key, label
    return None


def is_figure_html(html: str) -> bool:
    return "plotly-graph-div" in html


def extract_title(html: str) -> str:
    """อ่านชื่อกราฟจาก layout ที่ส่งเข้า Plotly.newPlot()

    args ของ newPlot เป็น JSON ที่ถูกต้อง จึงใช้ raw_decode ไล่อ่านทีละก้อนได้
    ลำดับ: "div-id", [data], {layout}, {config}
    """
    i = html.find("Plotly.newPlot(")
    if i < 0:
        return ""
    dec = json.JSONDecoder()
    pos = i + len("Plotly.newPlot(")
    try:
        for _ in range(3):  # id, data, layout
            while pos < len(html) and html[pos] in " \t\r\n,":
                pos += 1
            obj, pos = dec.raw_decode(html, pos)
        layout = obj  # ก้อนที่สาม
    except Exception:
        return ""
    if not isinstance(layout, dict):
        return ""
    title = layout.get("title")
    if isinstance(title, dict):
        title = title.get("text", "")
    return clean_title(title) if isinstance(title, str) else ""


SELF_LOADS_PLOTLY = re.compile(r"cdn\.plot\.ly/plotly-[\d.]+\.min\.js")


def build_page(fragment: str, title: str, source: str) -> str:
    safe_title = (title or "Chart").replace("<", "&lt;").replace(">", "&gt;")

    # notebook ที่รันด้วย renderer 'notebook_connected' จะฝังโค้ดที่ inject
    # <script src="cdn.plot.ly/plotly-X.Y.Z.min.js"> เข้ามาเองตอนรันบนเบราว์เซอร์
    # ถ้าเราใส่ CDN ซ้ำอีก หน้าจะโหลด plotly.js สองรอบ (เปลืองไป ~4.85 MB)
    if SELF_LOADS_PLOTLY.search(fragment):
        cdn_tag = "<!-- กราฟนี้โหลด plotly.js จาก CDN ด้วยตัวเองอยู่แล้ว จึงไม่ใส่ซ้ำ -->"
    else:
        cdn_tag = (
            "<!-- โหลด plotly.js จาก CDN แทนการฝังไลบรารี 4.85 MB ลงในไฟล์ -->\n"
            f'<script src="{PLOTLY_CDN}" charset="utf-8"></script>'
        )

    return f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{safe_title}</title>
{cdn_tag}
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  body {{ margin:0; padding:16px 20px; font-family:'Prompt',system-ui,-apple-system,'Segoe UI',sans-serif;
         background:#fff; color:#1a1a1a; }}
  header {{ border-bottom:1px solid #e5e5e5; padding-bottom:10px; margin-bottom:16px; }}
  h1 {{ font-size:1.05rem; font-weight:600; margin:0 0 4px; }}
  .src {{ font-size:.78rem; color:#666; font-weight:300; }}
  .plotly-graph-div {{ max-width:100%; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background:#111; color:#eee; }}
    header {{ border-color:#333; }}
    .src {{ color:#999; }}
  }}
</style>
</head>
<body>
<header>
  <h1>{safe_title}</h1>
  <div class="src">ที่มา / source: <code>{source}</code></div>
</header>
{fragment}
</body>
</html>
"""


def main() -> int:
    # ล้าง "เนื้อใน" ของ graphs/ แทนการลบตัวโฟลเดอร์เอง
    # บน Windows ถ้ามี process อื่นเปิดโฟลเดอร์นี้ค้างไว้ (เช่น เว็บเซิร์ฟเวอร์
    # หรือ terminal ที่ cd อยู่ข้างใน) การ rmtree ตัวโฟลเดอร์จะ PermissionError
    OUT.mkdir(parents=True, exist_ok=True)
    for child in OUT.iterdir():
        if child.is_dir():
            shutil.rmtree(child, ignore_errors=True)
        else:
            child.unlink(missing_ok=True)

    # group key -> list of (relative html/png path, title, source notebook)
    index: dict[str, list[tuple[str, str, str]]] = {k: [] for k, _ in GROUPS}
    broken: list[tuple[str, str]] = []
    total_html = total_png = 0

    for nb_path in iter_notebooks():
        g = group_of(nb_path)
        if g is None:
            continue
        gkey, _ = g
        rel_nb = nb_path.relative_to(REPO).as_posix()

        try:
            nb = json.loads(nb_path.read_text(encoding="utf-8"))
        except Exception as e:
            broken.append((rel_nb, f"{type(e).__name__}: {e}"))
            continue

        # โฟลเดอร์ปลายทาง: graphs/<group>/<path ย่อยเดิม>/<ชื่อ notebook>/
        sub = nb_path.relative_to(REPO / gkey).parent
        dest = OUT / gkey / sub / nb_path.stem
        n = 0

        for cell in nb.get("cells", []):
            for output in cell.get("outputs", []):
                data = output.get("data", {})

                png_b64 = data.get("image/png")
                if png_b64:
                    n += 1
                    dest.mkdir(parents=True, exist_ok=True)
                    name = f"{n:02d}_chart.png"
                    if isinstance(png_b64, list):
                        png_b64 = "".join(png_b64)
                    (dest / name).write_bytes(base64.b64decode(png_b64))
                    index[gkey].append(
                        ((dest / name).relative_to(OUT).as_posix(), f"chart {n}", rel_nb)
                    )
                    total_png += 1
                    continue

                html = data.get("text/html")
                if not html:
                    continue
                if isinstance(html, list):
                    html = "".join(html)
                # ข้าม output ที่เป็นแค่ตัวโหลดไลบรารี plotly.js (ไม่มีกราฟจริง)
                if not is_figure_html(html):
                    continue

                n += 1
                dest.mkdir(parents=True, exist_ok=True)
                title = extract_title(html) or f"{nb_path.stem} — chart {n}"
                name = f"{n:02d}_{slugify(title)}.html"
                (dest / name).write_text(
                    build_page(html, title, rel_nb), encoding="utf-8"
                )
                index[gkey].append(
                    ((dest / name).relative_to(OUT).as_posix(), title, rel_nb)
                )
                total_html += 1

    write_indexes(index, broken, total_html, total_png)

    print(f"\n  HTML charts : {total_html}")
    print(f"  PNG charts  : {total_png}")
    print(f"  total       : {total_html + total_png}")
    if broken:
        print(f"\n  ⚠️  notebook ที่อ่านไม่ได้ {len(broken)} ไฟล์:")
        for p, err in broken:
            print(f"      {p}  ({err})")
    size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"\n  graphs/ size: {size / 1024 / 1024:.1f} MB")
    return 0


def write_indexes(index, broken, total_html, total_png) -> None:
    """สร้าง README.md ดัชนีกราฟ ทั้งระดับรวมและระดับกลุ่ม"""
    lines = [
        "# 📊 คลังกราฟรวมทุกกลุ่ม (Graph Gallery)",
        "",
        "กราฟทั้งหมดที่ดึงออกมาจาก notebook ในโครงการนี้ รวบรวมไว้ที่เดียว",
        "แยกโฟลเดอร์ตามกลุ่มงาน เพื่อให้เปิดดูได้โดยไม่ต้องรัน notebook",
        "",
        f"| รวมทั้งหมด | {total_html + total_png} กราฟ |",
        "|---|---|",
        f"| Plotly (interactive `.html`) | {total_html} |",
        f"| ภาพนิ่ง (`.png`) | {total_png} |",
        "",
        "> ⚠️ ไฟล์ `.html` โหลด plotly.js จาก CDN — **ต้องต่ออินเทอร์เน็ตตอนเปิด**",
        "> และ GitHub ไม่เรนเดอร์ HTML ในหน้า preview ให้ดาวน์โหลดไปเปิดในเบราว์เซอร์",
        "> หรือดูผ่าน [htmlpreview.github.io](https://htmlpreview.github.io)",
        "",
        "สร้างใหม่ได้ด้วย:",
        "",
        "```powershell",
        ".\\venv\\Scripts\\python.exe tools\\export_graphs.py",
        "```",
        "",
        "---",
        "",
        "## กลุ่มงาน (Groups)",
        "",
        "| กลุ่ม | จำนวนกราฟ | ดัชนี |",
        "|---|---:|---|",
    ]
    for key, label in GROUPS:
        items = index.get(key, [])
        if not items:
            continue
        lines.append(f"| {label} | {len(items)} | [`{key}/`]({key}/README.md) |")
    lines.append("")

    if broken:
        lines += [
            "---",
            "",
            "## ⚠️ notebook ที่อ่านไม่ได้ (ข้ามไป)",
            "",
            "| ไฟล์ | ปัญหา |",
            "|---|---|",
        ]
        for p, err in broken:
            lines.append(f"| `{p}` | {err} |")
        lines.append("")

    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")

    for key, label in GROUPS:
        items = index.get(key, [])
        if not items:
            continue
        by_nb: dict[str, list[tuple[str, str]]] = {}
        for path, title, src in items:
            by_nb.setdefault(src, []).append((path, title))

        g = [
            f"# {label}",
            "",
            f"กราฟทั้งหมด **{len(items)}** ชิ้น จาก {len(by_nb)} notebook",
            "",
            "[⬅️ กลับไปดัชนีรวม](../README.md)",
            "",
        ]
        for src, charts in by_nb.items():
            g += [
                "---",
                "",
                f"### 📓 `{src}`",
                "",
                "| # | กราฟ |",
                "|---:|---|",
            ]
            for i, (path, title) in enumerate(charts, 1):
                # ลิงก์เทียบจากโฟลเดอร์กลุ่ม
                link = path[len(key) + 1 :] if path.startswith(key + "/") else path
                g.append(f"| {i} | [{title}]({link}) |")
            g.append("")
        (OUT / key / "README.md").write_text("\n".join(g), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
