#!/usr/bin/env python3
"""session.dsl -> terminal.svg   (stdlib only)"""
import html, sys, re

W, PAD = 920, 26
FS, LH = 13, 19.0
ADV = 0.62 * FS
TOP = 46
CPS = 0.023
PROMPT = "luciano@mlg ~ $ "

def esc(s): return html.escape(s, quote=False)
def tokens(s):
    "split '{k}SELECT{/} * FROM' into [(text, is_keyword), ...]"
    out, i = [], 0
    for m in re.finditer(r"\{k\}(.*?)\{/\}", s):
        if m.start() > i: out.append((s[i:m.start()], False))
        out.append((m.group(1), True)); i = m.end()
    if i < len(s): out.append((s[i:], False))
    return out
def plain(s): return sum(len(t) for t, _ in tokens(s))

lines, t = [], 0.6
for raw in open(sys.argv[1], encoding="utf-8"):
    raw = raw.rstrip("\n")
    if not raw or raw.startswith("#"):
        continue
    kind, delay, text = raw.split("|", 2)
    t += int(delay) / 1000.0
    if kind == "wait":
        continue
    lines.append({"kind": kind, "text": text, "t": t})
    t += plain(text) * CPS + 0.25 if kind == "cmd" else 0.05

H = TOP + PAD + int(len(lines) * LH) + PAD
TOTAL = t + 1.0

def x_of(col): return PAD + col * ADV
def y_of(i):   return TOP + PAD + i * LH + FS

body, caret_stops, chid = [], [], 0
for i, ln in enumerate(lines):
    y = y_of(i)
    if ln["kind"] == "gap":
        continue
    if ln["kind"] == "cmd":
        body.append(f'<text class="l ps" x="{x_of(0):.1f}" y="{y:.1f}" '
                    f'style="animation-delay:{ln["t"]:.2f}s">{esc(PROMPT)}</text>')
        spans, j = [], 0
        for run, kw in tokens(ln["text"]):
            for ch in run:
                chid += 1
                cl = "ch kw" if kw else "ch"
                spans.append(f'<tspan class="{cl}" style="animation-delay:{ln["t"]+j*CPS:.2f}s">{esc(ch)}</tspan>')
                j += 1
        body.append(f'<text class="cmd" x="{x_of(len(PROMPT)):.1f}" y="{y:.1f}" '
                    f'xml:space="preserve">{"".join(spans)}</text>')
        caret_stops.append((ln["t"], x_of(len(PROMPT)), y))
        caret_stops.append((ln["t"] + plain(ln["text"]) * CPS,
                            x_of(len(PROMPT) + plain(ln["text"])), y))
    elif ln["kind"] == "flip":
        off, on = ln["text"].split("%%")
        hold = 1.1                                    # switch flips 1.1s after the row lands
        body.append(f'<text class="fo" x="{x_of(0):.1f}" y="{y:.1f}" xml:space="preserve" '
                    f'style="animation-delay:{ln["t"]:.2f}s,{ln["t"]+hold:.2f}s">{esc(off)}</text>')
        body.append(f'<text class="l on" x="{x_of(0):.1f}" y="{y:.1f}" xml:space="preserve" '
                    f'style="animation-delay:{ln["t"]+hold:.2f}s">{esc(on)}</text>')
    else:
        cls = {"out": "out", "err": "err", "dim": "dim"}[ln["kind"]]
        txt = esc(ln["text"])
        txt = re.sub(r"\{k\}(.*?)\{/\}", r'<tspan class="kw">\1</tspan>', txt)
        body.append(f'<text class="l {cls}" x="{x_of(0):.1f}" y="{y:.1f}" xml:space="preserve" '
                    f'style="animation-delay:{ln["t"]:.2f}s">{txt}</text>')

kf, prev, prevx, prevy = [], None, 0, 0
kf.append(f"0%{{transform:translate({caret_stops[0][1]:.1f}px,{caret_stops[0][2]:.1f}px)}}")
for (ts, cx, cy) in caret_stops:
    p = 100.0 * ts / TOTAL
    if prev is not None and p - prev > 0.05:
        kf.append(f"{p-0.05:.3f}%{{transform:translate({prevx:.1f}px,{prevy:.1f}px)}}")
    kf.append(f"{p:.3f}%{{transform:translate({cx:.1f}px,{cy:.1f}px)}}")
    prev, prevx, prevy = p, cx, cy
kf.append(f"100%{{transform:translate({prevx:.1f}px,{prevy:.1f}px)}}")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace" font-size="{FS}">
<title>Terminal session: a database connection that times out, tunnels-manager opening a Google Cloud IAP tunnel, and Luciano Bosco's profile read back out of a MySQL result set.</title>
<style>
  /* resting state is ALWAYS a static declaration; animations only borrow the
     element on the way in. fill-mode:backwards, never forwards. */
  .l,.ch{{opacity:1;animation:app .09s linear backwards}}
  @keyframes app{{from{{opacity:0}}}}
  .fo{{opacity:1;fill:#6b7c8c;animation:app .09s linear backwards,dis .16s linear forwards}}
  @keyframes dis{{to{{opacity:0}}}}
  .on{{fill:#7ee787}}
  .ps{{fill:#3fb950}} .cmd{{fill:#e6edf3}} .out{{fill:#c0cbd6}}
  .dim{{fill:#6b7c8c}} .err{{fill:#f85149}} .kw{{fill:#bc8cff}}
  #caret{{fill:#3fb950;animation:walk {TOTAL:.2f}s linear backwards,blink 1s steps(1,end) infinite}}
  @keyframes walk{{{"".join(kf)}}}
  @keyframes blink{{0%,50%{{opacity:.95}}50.01%,100%{{opacity:.15}}}}
  @media (prefers-reduced-motion:reduce){{
    .l,.ch{{animation:none;opacity:1}} #caret{{animation:none;opacity:.6}}
  }}
</style>
<rect width="{W}" height="{H}" rx="10" fill="#0b0f14"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="#26313d"/>
<path d="M0 {TOP}H{W}" stroke="#1c242e"/>
<g fill="#3d4a58"><circle cx="20" cy="23" r="5"/><circle cx="38" cy="23" r="5"/><circle cx="56" cy="23" r="5"/></g>
<text x="80" y="27" fill="#8b98a5" font-size="12">luciano@mlg: ~/work &#8212; 1: mysql &#183; 2: kubectl</text>
<text x="{W-PAD}" y="27" fill="#4a5a68" font-size="12" text-anchor="end">M&#193;LAGA &#183; UTC+2</text>
<g id="caret" style="transform:translate({prevx:.1f}px,{prevy:.1f}px)"><rect width="{ADV:.1f}" height="{FS}" y="{-FS+2.5}"/></g>
{chr(10).join(body)}
</svg>
'''
open(sys.argv[2], "w", encoding="utf-8").write(svg)
print(f"{sys.argv[2]}: {len(svg)/1024:.1f} KB, {len(lines)} lines, {chid} typed chars, {TOTAL:.1f}s")
