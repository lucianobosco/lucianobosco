#!/usr/bin/env python3
"""Stack strip: brand-coloured monospace labels, optional logos. Terminal aesthetic."""
import html, json, pathlib

FS, LH, PAD = 13, 24.0, 18
ADV = 0.62 * FS
BG, BORDER, DIM, TITLE = "#0d1117", "#26313d", "#6b7c8c", "#8b98a5"
LOGOS = json.loads((pathlib.Path(__file__).parent / "logos.json").read_text())

# brand colours, nudged for contrast on a #0d1117 panel
ROWS = [
    ("languages", [("python", "#6ba5d9", "Python"), ("php", "#9b93d3", "PHP"),
                   ("laravel", "#ff5a4d", "Laravel"), ("wordpress", "#4a9cc4", None),
                   ("vue", "#4fc08d", None), ("vuex", "#3f9c74", None)]),
    ("data", [("mysql", "#4fb3d0", "MySQL"), ("bigquery", "#7fb2ff", "BigQuery")]),
    ("platform", [("microservices", "#d2a8ff", None), ("kubernetes", "#7f9dff", "Kubernetes"),
                  ("google cloud", "#6ba0ff", "Google_Cloud"), ("aws", "#ff9900", None),
                  ("temporal", "#b6c2cf", "Temporal")]),
    ("agents", [("claude code", "#e0876a", "Claude_Code"), ("mcp servers", "#79c0ff", "MCP"),
                ("skills per runbook", "#8b949e", None)]),
]

def esc(s): return html.escape(s, quote=False)

def build(with_logos: bool, width=880, label_w=11):
    top = PAD + 20
    height = int(top + len(ROWS) * LH + PAD)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" '
             f'font-size="{FS}">',
             f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="9" fill="{BG}" stroke="{BORDER}"/>',
             f'<text x="{PAD}" y="{PAD+11}" fill="{TITLE}" font-size="11" letter-spacing="1.4">'
             f'WHAT I WORK WITH</text>']
    for i, (group, items) in enumerate(ROWS):
        y = top + LH * (i + 0.7)
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{DIM}">{esc(group.ljust(label_w))}</text>')
        x = PAD + label_w * ADV
        for index, (name, colour, logo_key) in enumerate(items):
            if index:
                parts.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="#39424d">·</text>')
                x += 2 * ADV
            if with_logos and logo_key and logo_key in LOGOS:
                parts.append(f'<image x="{x:.1f}" y="{y-11:.1f}" width="13" height="13" '
                             f'href="{LOGOS[logo_key]}"/>')
                x += 18
            parts.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{colour}">{esc(name)}</text>')
            x += (len(name) + 1) * ADV
    parts.append('</svg>')
    return "\n".join(parts)

root = pathlib.Path(__file__).parent.parent
root.joinpath("stack.svg").write_text(build(False))

print("stack.svg", root.joinpath("stack.svg").stat().st_size, "bytes")
