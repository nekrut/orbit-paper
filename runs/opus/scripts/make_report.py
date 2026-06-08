#!/usr/bin/env python
"""Render the final-report section of notebook.md to a standalone PDF
with embedded volcano figures."""
import re
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

ROOT = Path(__file__).resolve().parent.parent
NB = (ROOT / "notebook.md").read_text()

# Slice from the "## Final report" heading to end-of-file
m = re.search(r"^## Final report.*", NB, re.MULTILINE)
assert m, "Final report section not found"
body_md = NB[m.start():]

# Demote the top-level "## " of the report so the PDF's h1 is the report title
body_md = re.sub(r"^## Final report.*", "# Santana et al. 2023 — Reproduction Report", body_md, count=1, flags=re.MULTILINE)
body_md = re.sub(r"^### ", "## ", body_md, flags=re.MULTILINE)

# Convert the explicit figure reference lines into actual <img> tags so the
# PDF embeds the volcanoes
def embed_fig(match):
    fname = match.group(1)
    path = (ROOT / "figures" / fname).as_uri()
    cap = match.group(2).strip(" —-")
    return f'\n\n<figure><img src="{path}" alt="{cap}"/><figcaption>{cap}</figcaption></figure>\n\n'

# Pre-process figure bullets in raw markdown -> inline HTML <figure> blocks
# so the markdown engine never tries to nest them inside <li>.
fig_blocks = {}
def stash_fig(match):
    fname = match.group(1) + ".png"
    caption_md = match.group(2)
    # render caption snippet through markdown so backticks etc. become <code>
    cap_html = markdown.markdown(caption_md).replace("<p>", "").replace("</p>", "")
    src = (ROOT / "figures" / fname).as_uri()
    placeholder = f"@@FIG{len(fig_blocks)}@@"
    fig_blocks[placeholder] = f'<figure><img src="{src}"/><figcaption>{cap_html}</figcaption></figure>'
    return placeholder

body_md = re.sub(
    r"^- `figures/(volcano_[^`]+)\.pdf`\s*/\s*`\.png`\s*—\s*(.+)$",
    stash_fig,
    body_md,
    flags=re.MULTILINE,
)

html_body = markdown.markdown(body_md, extensions=["tables", "fenced_code"])
for ph, block in fig_blocks.items():
    # The placeholder ended up inside <li>...</li>; lift it out cleanly.
    html_body = re.sub(rf"<li>\s*{ph}\s*</li>", block, html_body)
    html_body = html_body.replace(ph, block)
# Tidy any resulting empty <ul></ul>
html_body = re.sub(r"<ul>\s*</ul>", "", html_body)

CSS_STR = """
@page { size: letter; margin: 1.6cm 1.8cm; @bottom-right { content: counter(page) " / " counter(pages); font-size: 9pt; color: #666; } }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #222; }
h1 { font-size: 20pt; border-bottom: 2px solid #333; padding-bottom: 0.2em; margin-bottom: 0.4em; }
h2 { font-size: 13pt; color: #1a3b6e; margin-top: 1.2em; border-bottom: 1px solid #cfd8e3; padding-bottom: 0.1em; }
h3 { font-size: 11.5pt; color: #333; }
p, li { font-size: 10.5pt; }
code { background: #f3f3f3; padding: 1px 4px; border-radius: 3px; font-size: 9.5pt; }
table { border-collapse: collapse; margin: 0.5em 0 1em 0; width: 100%; font-size: 9.5pt; page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 4px 7px; text-align: left; vertical-align: top; }
th { background: #eef2f7; font-weight: 600; }
figure { margin: 1em 0; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; height: auto; border: 1px solid #ddd; }
figcaption { font-size: 9pt; color: #555; margin-top: 0.3em; font-style: italic; }
hr { border: none; border-top: 1px solid #ccc; margin: 1em 0; }
em { color: #444; }
"""

html_doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Santana et al. 2023 — Reproduction Report</title></head>
<body>
<p style="color:#666;font-size:9.5pt;margin-top:0;">Reproduction of <em>Santana DJ et al., Science 381:1461 (2023)</em> &middot; RNA-seq DE analysis &middot; <em>C. auris</em> B8441 v3 / Galaxy</p>
{html_body}
</body></html>"""

(ROOT / "figures" / "final_report.html").write_text(html_doc)
HTML(string=html_doc, base_url=str(ROOT)).write_pdf(
    ROOT / "figures" / "final_report.pdf",
    stylesheets=[CSS(string=CSS_STR)],
)
print("wrote", ROOT / "figures" / "final_report.pdf")
