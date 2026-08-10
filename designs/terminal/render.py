#!/usr/bin/env python3
"""session.dsl -> terminal.svg + transcript.txt   (stdlib only, deterministic)

Rules that make this survive:
  1. The resting state is ALWAYS a static declaration. Animations only borrow an
     element on the way in (fill-mode: backwards / none, never forwards) and the
     duration is never below .09s. Chrome silently drops sub-frame CSS animations
     inside SVG: elements whose delay lands mid-timeline stay at the animated
     value FOREVER. If the animation owns the resting state, they vanish.
  2. Every typed character carries its own absolute x. Nothing depends on the
     host font's advance width, so the caret can never drift off the text.
  3. Canvas width is derived from the longest line, so clipping is impossible.
"""
import html, re, sys

# ---------------------------------------------------------------- geometry
FS, LH = 13, 19.5
ADV = 0.62 * FS          # worst-case monospace advance (DejaVu .602, Menlo .600,
                         # SFMono .600, Consolas .550) -> grid is never too narrow
PAD, TOP = 22, 44
CPS = 0.015              # 15 ms per typed character
LEAD = 0.35              # dead air before the first keystroke
TAIL = 0.80              # dead air after the last line
PROMPT = "luciano@mlg ~ $ "

PAL = dict(bg="#0b0f14", chrome="#111820", rule="#1c242e", edge="#26313d",
           title="#8b98a5", stamp="#5d6d7b", ps="#3fb950", cmd="#8b96a1",
           out="#c0cbd6", say="#a8c7e8", dim="#4c5561", err="#f85149",
           kw="#bc8cff", on="#7ee787", off="#6b7c8c", caret="#3fb950")

SW = re.compile(r"\{sw:([^|}]*)\|([^}]*)\}")
KW = re.compile(r"\{k\}(.*?)\{/\}")


def esc(s):
    s = html.escape(s, quote=False)
    return "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in s)


def tokens(s):
    """'{k}SELECT{/} * FROM' -> [('SELECT', True), (' * FROM', False)]"""
    out, i = [], 0
    for m in KW.finditer(s):
        if m.start() > i:
            out.append((s[i:m.start()], False))
        out.append((m.group(1), True))
        i = m.end()
    if i < len(s):
        out.append((s[i:], False))
    return out


def plain(s):
    """visible text: keyword markers removed, switch marker collapsed to OFF"""
    s = SW.sub(lambda m: m.group(1), s)
    return "".join(t for t, _ in tokens(s))


def x_of(col):
    return PAD + col * ADV


def tl(s):
    """Nail a run of text to the ADV grid on every OS. Without this, a text node
    flows at the host font's own advance width (Consolas .550 vs our .620) and
    drifts left by ~1.3 chars by column 40 -- which is where the switch cell is."""
    return 'textLength="%.1f" lengthAdjust="spacing"' % (len(s) * ADV)


# ---------------------------------------------------------------- parse
def parse(path):
    rows, t, lineno = [], LEAD, 0
    for raw in open(path, encoding="utf-8"):
        lineno += 1
        raw = raw.rstrip("\n")
        if not raw or raw.lstrip().startswith("#"):
            continue
        try:
            kind, delay, text = raw.split("|", 2)
        except ValueError:
            sys.exit(f"{path}:{lineno}: expected KIND|delay|text")
        if kind not in ("cmd", "out", "err", "say", "dim", "tbl", "flip", "wait", "gap"):
            sys.exit(f"{path}:{lineno}: unknown kind {kind!r}")
        t += int(delay) / 1000.0
        if kind == "wait":
            continue
        rows.append(dict(kind=kind, text=text, t=t, src=lineno))
        t += len(plain(text)) * CPS + 0.22 if kind == "cmd" else 0.05
    return rows, t + TAIL


# ---------------------------------------------------------------- invariants
def check(rows, cols):
    for r in rows:
        if r["kind"] == "flip":
            m = SW.search(r["text"])
            if not m:
                sys.exit(f"line {r['src']}: flip row without a {{sw:OFF|ON}} marker")
            if len(m.group(1)) != len(m.group(2)):
                sys.exit(f"line {r['src']}: OFF/ON must be the same length")
    # contiguous table blocks must be column-aligned
    block = []
    for r in rows + [dict(kind="gap", text="", t=0, src=0)]:
        if r["kind"] in ("tbl", "flip"):
            block.append(r)
            continue
        if len(block) > 1:
            w = {len(plain(b["text"])) for b in block}
            if len(w) > 1:
                sys.exit("table block at lines %s is ragged: widths %s"
                         % ([b["src"] for b in block], sorted(w)))
        block = []
    if cols > 120:
        sys.exit(f"longest line is {cols} chars; keep it under 120")


# ---------------------------------------------------------------- render
def render(rows, total):
    cols = max((len(plain(r["text"])) for r in rows), default=0)
    check(rows, cols)
    W = int(2 * PAD + (len(PROMPT) + cols) * ADV) + 2
    W = max(W, 640)
    H = int(TOP + PAD + len(rows) * LH + PAD)

    body, stops = [], []
    for i, r in enumerate(rows):
        y = TOP + PAD + i * LH + FS
        k, txt = r["kind"], r["text"]

        if k == "gap":
            continue

        if k == "cmd":
            body.append(
                f'<text class="ps" x="{x_of(0):.1f}" y="{y:.1f}" xml:space="preserve"'
                f' {tl(PROMPT)}'
                f' style="animation-delay:{r["t"]:.2f}s">{esc(PROMPT)}</text>')
            spans, j = [], 0
            for run, kw in tokens(txt):
                for ch in run:
                    spans.append(
                        f'<tspan class="{"ch kw" if kw else "ch"}"'
                        f' x="{x_of(len(PROMPT)+j):.1f}"'
                        f' style="animation-delay:{r["t"]+j*CPS:.2f}s">{esc(ch)}</tspan>')
                    j += 1
            body.append(f'<text class="cmd" y="{y:.1f}" xml:space="preserve">'
                        + "".join(spans) + "</text>")
            # snap to the start of the line, then GLIDE across it as it types
            stops.append((r["t"], x_of(len(PROMPT)), y, True))
            stops.append((r["t"] + j * CPS, x_of(len(PROMPT) + j), y, False))
            continue

        if k in ("out", "err", "say", "dim", "tbl", "flip"):
            # a real terminal parks the caret right after whatever just printed
            stops.append((r["t"], x_of(len(plain(txt))), y, True))

        if k == "flip":
            m = SW.search(txt)
            off, on = m.group(1), m.group(2)
            col = len(txt[:m.start()])          # switch column (no {k} inside tbl rows)
            blank = txt[:m.start()] + " " * len(off) + txt[m.end():]
            hold = 0.75                          # OFF holds this long, then ON lands
            body.append(f'<text class="row tbl" x="{x_of(0):.1f}" y="{y:.1f}"'
                        f' xml:space="preserve" {tl(blank)}'
                        f' style="animation-delay:{r["t"]:.2f}s">{esc(blank)}</text>')
            body.append(f'<text class="fo" x="{x_of(col):.1f}" y="{y:.1f}"'
                        f' xml:space="preserve" {tl(off)}'
                        f' style="animation-delay:{r["t"]:.2f}s;'
                        f'animation-duration:{hold:.2f}s">{esc(off)}</text>')
            body.append(f'<text class="row on" x="{x_of(col):.1f}" y="{y:.1f}"'
                        f' xml:space="preserve" {tl(on)}'
                        f' style="animation-delay:{r["t"]+hold:.2f}s">{esc(on)}</text>')
            continue

        cls = {"out": "out", "err": "err", "say": "say", "dim": "dim", "tbl": "tbl"}[k]
        inner = KW.sub(r'<tspan class="kw">\1</tspan>', esc(txt))
        body.append(f'<text class="row {cls}" x="{x_of(0):.1f}" y="{y:.1f}"'
                    f' xml:space="preserve" {tl(plain(txt))}'
                    f' style="animation-delay:{r["t"]:.2f}s">{inner}</text>')

    # caret: one @keyframes, one stop per line-start / line-end, snapping between
    kf, prev, px, py = [], None, stops[0][1], stops[0][2]
    kf.append(f"0%{{transform:translate({px:.1f}px,{py:.1f}px)}}")
    for ts, cx, cy, snap in stops:
        p = 100.0 * ts / total
        # snap stops hold the previous position until the last instant, so the
        # caret jumps between lines. glide stops interpolate, so the caret walks
        # along the line at exactly typing speed.
        if snap and prev is not None and p - prev > 0.05:
            kf.append(f"{p-0.05:.3f}%{{transform:translate({px:.1f}px,{py:.1f}px)}}")
        kf.append(f"{p:.3f}%{{transform:translate({cx:.1f}px,{cy:.1f}px)}}")
        prev, px, py = p, cx, cy
    kf.append(f"100%{{transform:translate({px:.1f}px,{py:.1f}px)}}")

    P = PAL
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace" font-size="{FS}">
<title>Terminal session: a MySQL connection to a production host times out, tunnels-manager
opens a Google Cloud IAP tunnel on local port 13306, the same command then connects, and
selecting Luciano Bosco's private repositories returns permission denied.</title>
<style>
  /* Resting state is a STATIC declaration on every element. Animations only
     borrow an element on the way in: fill-mode backwards (or none), never
     forwards; duration never under .09s. Chrome drops sub-frame CSS animations
     inside SVG, so an animation that owns the resting state loses the element. */
  .row,.ch{{opacity:1;animation:app .10s linear backwards}}
  @keyframes app{{from{{opacity:0}}}}
  /* the OFF switch: invisible at rest, animation holds it visible for `hold` */
  .fo{{opacity:0;fill:{P['off']};animation-name:hold;
       animation-timing-function:linear;animation-fill-mode:none}}
  @keyframes hold{{0%,100%{{opacity:1}}}}
  .ps{{opacity:1;fill:{P['ps']};animation:app .10s linear backwards}}
  .cmd{{fill:{P['cmd']}}} .out{{fill:{P['out']}}} .say{{fill:{P['say']}}}
  .dim{{fill:{P['dim']}}} .tbl{{fill:{P['out']}}} .err{{fill:{P['err']}}}
  .kw{{fill:{P['kw']}}}  .on{{fill:{P['on']}}}
  #caret{{fill:{P['caret']};animation:walk {total:.2f}s linear backwards,
          blink 1.06s steps(1,end) infinite}}
  @keyframes walk{{{''.join(kf)}}}
  @keyframes blink{{0%,50%{{opacity:.95}}50.01%,100%{{opacity:.18}}}}
  @media (prefers-reduced-motion:reduce){{
    .row,.ch,.ps{{animation:none;opacity:1}}
    .fo{{animation:none;opacity:0}}          /* rest = switch already ON */
    #caret{{animation:none;opacity:.55}}
  }}
</style>
<rect width="{W}" height="{H}" rx="9" fill="{P['bg']}"/>
<path d="M9 .5h{W-18}a8.5 8.5 0 0 1 8.5 8.5V{TOP}H.5V9A8.5 8.5 0 0 1 9 .5Z" fill="{P['chrome']}"/>
<path d="M0 {TOP}.5H{W}" stroke="{P['rule']}"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="9" fill="none" stroke="{P['edge']}"/>
<text x="{PAD}" y="27" fill="{P['title']}" font-size="12">luciano@mlg: ~/work</text>
<text x="{W-PAD-26}" y="27" fill="{P['stamp']}" font-size="12" text-anchor="end">M&#193;LAGA</text>
<g stroke="{P['title']}" stroke-width="1.3" stroke-linecap="round" opacity=".8">
  <path d="M{W-PAD-9} 17l9 9M{W-PAD} 17l-9 9"/>
</g>
<g id="caret" style="transform:translate({px:.1f}px,{py:.1f}px)">
  <rect width="{ADV:.1f}" height="{FS+1}" y="{-FS+2.5:.1f}"/></g>
{chr(10).join(body)}
</svg>
'''
    return svg, W, H, cols


def transcript(rows):
    out = []
    for r in rows:
        if r["kind"] == "gap":
            out.append("")
        elif r["kind"] == "cmd":
            out.append(PROMPT + plain(r["text"]))
        elif r["kind"] == "flip":
            out.append(SW.sub(lambda m: m.group(2), r["text"]))
        else:
            out.append(plain(r["text"]))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    dsl, svg_path, txt_path = sys.argv[1], sys.argv[2], sys.argv[3]
    rows, total = parse(dsl)
    svg, W, H, cols = render(rows, total)
    open(svg_path, "w", encoding="utf-8").write(svg)
    open(txt_path, "w", encoding="utf-8").write(transcript(rows))
    print(f"{svg_path}: {len(svg)/1024:.1f} KB  {W}x{H}  {len(rows)} rows  "
          f"{cols} cols  {total:.1f}s")
