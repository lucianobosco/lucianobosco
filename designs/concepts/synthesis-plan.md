## 1. The concept, in three sentences

The profile is a single terminal session, rendered once as a hand-generated animated SVG: `mysql` to a production host **hangs and times out**, `ss -ltnp | grep 13306` shows nothing listening, and then **his own app** — `tunnels-manager` — draws its table, you watch one switch flip `[ O== ] → [ ==O ]`, the connection string lands on the clipboard, and the identical `mysql` command connects. From the working connection he selects his own private repos and gets `ERROR 1142 (42000): SELECT command denied to user 'visitor'@'github'`, which turns "4 public repos, 5 followers" from a hole in his career into the sharpest line on the page, stated in the syntax of the system he lives in. It runs **once, 16.0 s, no loop**, and its resting state is the complete, readable transcript — so the animation is a bonus and the document is the product; the image is wrapped in a link to `tunnels-manager`, and the selectable substance (bio, stack, three sanitized write-ups of the private systems the 1142 is hiding) lives in plain Markdown around it.

**All artifacts below are built and browser-verified**, not proposed. Working tree:
`<local scratch dir>`
→ `tools/render.py`, `session.dsl`, `terminal.svg`, `transcript.txt`, `harness.html` (img at 835 px + 390 px), `inline.html` (Web-Animations rig for frame-exact inspection).

Measured output: **835 × 614 px, 30,561 bytes, 356 elements** (35 `<text>`, 310 `<tspan>`), 54 caret keyframe stops, **16.0 s total**, `ERROR 2003` lands at **2.92 s**, 27 rows, longest line 82 chars. Chrome verification at `t = 5600 ms`: OFF cell `opacity 1`, ON cell `0`; at `t = 6500 ms`: OFF `0`, ON `1`; at rest: 0 of 14 output rows hidden.

### What was grafted from the runners-up
| Graft | From | Why |
|---|---|---|
| Scarcity-as-access-control **taken past the joke**: three public `docs/systems/*.md` write-ups, linked as plain Markdown | v14.2 panel | Its own vote's #1 kill: the good content was gated behind a public GitHub issue a hiring manager will never open. Ungated here. |
| All interactivity stays at the Markdown layer; zero workflows a stranger can trigger; committed artifact only | v14.2 panel | Removes the push-race, the spam surface, and the employer-disclosure hazard in one deletion. |
| "Animations only borrow an element on the way in" — extended to the switch cell, which was the one element still breaking the rule | v14.2 panel + winner's own risk note | The flip was the only frame that could degrade to garbage. Now it degrades to "switch already on". |
| Migration clocks as **static prose with no dates** ("what I'm racing") | live-probes panel | The senior signal without the calendar rot that vote proved fatal. |
| "Never let the artifact assert a fact that expires" | live-probes panel | Killed `UTC+2` (wrong 5 months/year) and the guessed `years` column. |

---

## 2. File layout — repo `lucianobosco/lucianobosco` (default branch `main`)

```
README.md                      # 3 selectable lines, the image, the write-up links, the transcript
session.dsl                    # THE TRANSCRIPT. the only file he normally edits.
terminal.svg                   # committed artifact: 835x614, 30.5 KB, 356 nodes, 16.0 s
transcript.txt                 # generated plain text; injected into README between markers
tools/render.py                # DSL -> SVG + transcript. ~215 lines, stdlib only, deterministic.
tools/inject.py                # transcript.txt -> README <details> block (so it cannot drift)
docs/systems/ingest-pipeline.md    # the three write-ups. NDA-sanitized. see §8.
docs/systems/catalog-mysql.md
docs/systems/video-delivery.md
.github/workflows/render.yml   # on: push only. NO cron -> nothing to auto-disable at 60 days.
```

Nothing else. No badges, no counters, no third-party image host, no token, no cron, no runtime dependency: `raw.githubusercontent.com` serving one committed file is the entire delivery path.

---

## 3. `session.dsl` — final, verified timings

Format `KIND|delay_ms|text`. Kinds: `cmd out err say dim tbl flip wait gap`.

```
# KIND|delay_ms|text
#   cmd  typed per character, preceded by the prompt
#   out  program output, bright        err  program output, red
#   say  his voice (comments); the brightest non-command text (7.9:1)
#   dim  chrome / low-priority        tbl  table row: contiguous tbl+flip rows must be equal length
#   flip exactly one {sw:OFF|ON} marker, len(OFF) == len(ON)
#   wait burns time without emitting a row      gap  an empty row
cmd|150|whoami
out|180|lbosco  -  software engineer, 14 years  -  Malaga, ES
gap|80|
cmd|220|mysql -h 10.24.6.11 -P 3306 -u readonly catalog
wait|600|
err|0|ERROR 2003 (HY000): Can't connect to MySQL server on '10.24.6.11:3306' (110)
cmd|300|ss -ltnp | grep 13306
say|180|# nothing at work is reachable from a laptop. that is the point.
gap|100|
cmd|250|tunnels-manager &
out|280|[gtk4] tunnels-manager 0.4  -  6 tunnels in ~/.config/tunnels.toml
flip|100|  catalog-db-prod       iap    13306   [ {sw:O==|==O} ]
tbl|60|  videos-db-replica     iap    13307   [ O== ]
out|850|  -> clipboard: mysql://readonly@127.0.0.1:13306/catalog
cmd|320|ss -ltnp | grep 13306
out|220|LISTEN 0 128 127.0.0.1:13306 0.0.0.0:* users:(("tunnels-manager",pid=41207,fd=11))
gap|100|
cmd|250|mysql -h 127.0.0.1 -P 13306 -u readonly catalog
cmd|350|{k}SELECT{/} * {k}FROM{/} luciano.repos {k}WHERE{/} visibility = 'private';
err|320|ERROR 1142 (42000): SELECT command denied to user 'visitor'@'github'
say|150|-- 4 public repos. the other 14 years ship under NDA. that is the tell.
gap|140|
cmd|250|kubectl -n platform get pods -l app=ingest --watch
out|350|ingest-worker-4b8qz   0/1   Pending   0     0s
out|800|ingest-worker-4b8qz   1/1   Running   0     6s
say|180|# the whole job is making that line boring. it has been for years.
gap|140|
cmd|350|open github.com/lucianobosco/tunnels-manager
```

Verified beat sheet (computed, not estimated): `whoami` 0.50 · error **2.92** · `ss` empty 3.26 · app launches 4.43 · switch flips **6.08** · clipboard 6.34 · `LISTEN` line 7.47 · reconnect 7.92 · `1142` **10.59** · pod Running 13.45 · final line 14.27 · ends 15.95.

Two acts were **cut** from the earlier draft on the judges' evidence: the `SELECT * FROM luciano.stack` results table (7 rows, generic skills list, and the only place the image asserted numbers he'd have to fact-check — moved to selectable Markdown) and the 1.6 s dead hang (600 ms still reads as a timeout and gets the error on screen before the 3 s scroll decision).

---

## 4. `tools/render.py` — complete

```python
#!/usr/bin/env python3
"""session.dsl -> terminal.svg + transcript.txt   (stdlib only, deterministic)

Rules that make this survive:
  1. The resting state is ALWAYS a static declaration. Animations only borrow an
     element on the way in (fill-mode: backwards / none, never forwards) and the
     duration is never below .09s. Chrome silently drops sub-frame CSS animations
     inside SVG: elements whose delay lands mid-timeline stay at the animated
     value FOREVER. If the animation owns the resting state, they vanish.
  2. Every typed character carries its own absolute x, and every other run of
     text is nailed to the same grid with textLength. Nothing depends on the host
     font's advance width, so the caret can never drift off the text.
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
           title="#8b98a5", stamp="#5d6d7b", ps="#3fb950", cmd="#e6edf3",
           out="#c0cbd6", say="#9aa8b5", dim="#6b7c8c", err="#f85149",
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

    # caret: one @keyframes, one stop per line-start / line-end / output-end
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
```

### Four fixes in there that are not obvious and are the difference between shipping and shipping broken

1. **`textLength` + `lengthAdjust="spacing"` on every non-typed run.** Without it a `<text>` node flows at the *host* font's advance (Consolas 0.550 vs our grid 0.620) and drifts ~1.3 characters left by column 40 — exactly where the switch cell sits. This was **observed in Chrome**: the ON overlay rendered as `[  ==O]` instead of `[ ==O ]`. With `textLength` it is pixel-exact on every OS, and total width no longer varies by platform.
2. **`.fo` never owns its resting state.** `opacity:0` static; a `hold` keyframe (`0%,100%{opacity:1}`) with `animation-fill-mode:none` lifts it to 1 for exactly 0.75 s. Written **longhand on purpose** — in the `animation` shorthand a bare `none` is ambiguous between `animation-name` and `animation-fill-mode`. Degradation: any renderer that drops CSS animation, and the reduced-motion path, both show *"switch already ON"* — never two rows of text on top of each other.
3. **Caret stops are typed `snap` vs `glide`.** The hold-previous-position keyframe is emitted **only before snap stops**. The first build emitted it before every stop, which pinned the caret at column 0 while the line typed out underneath it — visible in the browser, invisible in code review.
4. **Non-ASCII is emitted as numeric entities** (`M&#193;LAGA`), so encoding can never be the thing that blanks the image.

### Real generated output (verbatim, for byte-level comparison after re-implementation)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 835 614" width="835" height="614"
     font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace" font-size="13">
...
<rect width="835" height="614" rx="9" fill="#0b0f14"/>
<path d="M9 .5h817a8.5 8.5 0 0 1 8.5 8.5V44H.5V9A8.5 8.5 0 0 1 9 .5Z" fill="#111820"/>
<path d="M0 44.5H835" stroke="#1c242e"/>
<rect x=".5" y=".5" width="834" height="613" rx="9" fill="none" stroke="#26313d"/>
<text x="22" y="27" fill="#8b98a5" font-size="12">luciano@mlg: ~/work</text>
<text x="787" y="27" fill="#5d6d7b" font-size="12" text-anchor="end">M&#193;LAGA</text>
<g stroke="#8b98a5" stroke-width="1.3" stroke-linecap="round" opacity=".8">
  <path d="M804 17l9 9M813 17l-9 9"/></g>
<g id="caret" style="transform:translate(505.6px,586.0px)">
  <rect width="8.1" height="14" y="-10.5"/></g>

<!-- a typed line: prompt as one node, then one tspan per character with its own x -->
<text class="ps" x="22.0" y="79.0" xml:space="preserve" textLength="129.0" lengthAdjust="spacing"
      style="animation-delay:0.50s">luciano@mlg ~ $ </text>

<!-- the hinge: three nodes at y=274.0. the row's switch slot is BLANK; only the
     3-char cell cross-fades, so worst-case degradation is one muddy glyph. -->
<text class="row tbl" x="22.0" y="274.0" xml:space="preserve" textLength="370.8" lengthAdjust="spacing"
      style="animation-delay:5.33s">  catalog-db-prod       iap    13306   [     ]</text>
<text class="fo"      x="352.5" y="274.0" xml:space="preserve" textLength="24.2" lengthAdjust="spacing"
      style="animation-delay:5.33s;animation-duration:0.75s">O==</text>
<text class="row on"  x="352.5" y="274.0" xml:space="preserve" textLength="24.2" lengthAdjust="spacing"
      style="animation-delay:6.08s">==O</text>

<text class="row err" x="22.0" y="157.0" xml:space="preserve" textLength="612.6" lengthAdjust="spacing"
      style="animation-delay:2.92s">ERROR 2003 (HY000): Can't connect to MySQL server on '10.24.6.11:3306' (110)</text>
<text class="row say" x="22.0" y="449.5" xml:space="preserve" textLength="572.3" lengthAdjust="spacing"
      style="animation-delay:10.79s">-- 4 public repos. the other 14 years ship under NDA. that is the tell.</text>
```

Row geometry: `y = 44 + 22 + i·19.5 + 13` for row *i* (0-indexed over all rows including `gap`), `x = 22 + col·8.06`. Prompt is 16 chars → command text starts at `x = 151.0`.

Contrast, computed on `#0b0f14`: `say #9aa8b5` = **7.97:1**; `out #c0cbd6` = 11.4:1; `dim #6b7c8c` = 4.47:1 — which is why **`dim` is reserved for chrome and every line of actual writing is `say`**. The earlier draft had the punchlines at 4.47:1, tied with table borders.

---

## 5. `tools/inject.py` — keeps the accessible transcript from drifting

```python
#!/usr/bin/env python3
"""transcript.txt -> README.md, between the markers. Run after render.py."""
import re, sys
readme, txt = sys.argv[1], sys.argv[2]
body = open(txt, encoding="utf-8").read().rstrip("\n")
src = open(readme, encoding="utf-8").read()
new, n = re.subn(r"(?s)(<!--TRANSCRIPT:BEGIN-->\n).*?(\n<!--TRANSCRIPT:END-->)",
                 lambda m: m.group(1) + "\n```console\n" + body + "\n```\n" + m.group(2),
                 src)
if n != 1:
    sys.exit("README.md must contain exactly one TRANSCRIPT:BEGIN/END pair")
open(readme, "w", encoding="utf-8").write(new)
```

---

## 6. `README.md` — complete

```html
**Luciano Bosco** — software engineer, 14 years, Málaga (ES).
Databases, data pipelines, and the platforms behind video and stock content.
`Python` `Go` `PHP/Laravel` `Vue` · `MySQL` `BigQuery` · `Google Cloud` `Kubernetes` `Temporal`

<!-- The last line of the session is `open github.com/lucianobosco/tunnels-manager`.
     Wrapping the img in my own <a> makes that command the click target, instead of
     letting GitHub hijack the click to the blob page. -->
<a href="https://github.com/lucianobosco/tunnels-manager">
  <img src="terminal.svg" width="835"
       alt="Terminal session. `mysql -h 10.24.6.11 -P 3306 -u readonly catalog` times out with
ERROR 2003. `ss -ltnp | grep 13306` returns nothing: nothing at work is reachable from a laptop.
tunnels-manager, a GTK4 app, lists six tunnels; the switch on catalog-db-prod flips on, opening a
Google Cloud IAP tunnel on local port 13306, and puts mysql://readonly@127.0.0.1:13306/catalog on
the clipboard. `ss -ltnp` now shows a LISTEN socket owned by tunnels-manager. The same mysql
command connects. Selecting the private repositories returns ERROR 1142 (42000): SELECT command
denied to user 'visitor'@'github' — four public repos, the other fourteen years ship under NDA.
It closes on kubectl watching an ingest pod go Pending then Running in six seconds.">
</a>

### tunnels-manager

GTK4 desktop app. Every Google Cloud IAP tunnel and `kubectl port-forward` you need,
a table with one switch each, and the connection string handed to you on the clipboard.
Local ports are the real default plus ten thousand, because 3306 is already bound on my laptop.

[repo](https://github.com/lucianobosco/tunnels-manager) ·
[screenshot](https://raw.githubusercontent.com/lucianobosco/tunnels-manager/main/docs/screenshot.png)

### What the 1142 is hiding

Three systems I own that you cannot clone. Written up instead — architecture, the
tradeoff taken, and the number that moved. No employer internals, no hostnames.

- [**ingest-pipeline**](docs/systems/ingest-pipeline.md) — Temporal workflows over a
  batch that has to survive a retry. Why durable execution and not cron, and what it
  cost to make partial failure boring.
- [**catalog-mysql**](docs/systems/catalog-mysql.md) — the query plan work. One
  filesort on a large catalogue table, before and after, and why the index that looks
  right is the wrong one.
- [**video-delivery**](docs/systems/video-delivery.md) — encode and deliver on
  Kubernetes: queue shape, backpressure, and the failure mode that only shows up at
  the edge.

Currently racing: Kubernetes minor upgrades, PHP 8.3 → 8.4, MySQL 8.0 → 8.4.
Fourteen years in, that list is the actual job.

<details open>
<summary>The session above as text — selectable, searchable, no motion</summary>

<!--TRANSCRIPT:BEGIN-->
<!--TRANSCRIPT:END-->
</details>
```

`<details open>` is deliberate: SVG text is neither selectable nor visible to screen readers, and it is illegible on a phone (835 px scaled to 390 px is ~6 px type — **confirmed in the browser**). The transcript is the mobile and a11y experience, so it must not be a click away.

---

## 7. `.github/workflows/render.yml` — complete

```yaml
name: render
on:
  push:
    paths: [session.dsl, tools/render.py, tools/inject.py, .github/workflows/render.yml]
  workflow_dispatch:
permissions:
  contents: write            # new repos give GITHUB_TOKEN read-only; the push fails without this
concurrency: {group: render, cancel-in-progress: false}
jobs:
  svg:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: render                       # render.py exits non-zero on a ragged table block,
        run: |                             # a bad {sw:} marker, or a line over 120 chars
          python3 tools/render.py session.dsl terminal.svg transcript.txt
          python3 tools/inject.py README.md transcript.txt
      - name: gate
        run: |
          python3 -c "import xml.dom.minidom as m; m.parse('terminal.svg')"
          test "$(stat -c%s terminal.svg)" -lt 204800
          grep -q 'prefers-reduced-motion' terminal.svg
          # THE RULE, enforced: no animation may own a resting state.
          ! grep -q 'forwards' terminal.svg
          # the transcript in the README must match the render
          python3 - <<'PY'
          import re
          r=open('README.md').read(); t=open('transcript.txt').read().rstrip('\n')
          m=re.search(r'(?s)TRANSCRIPT:BEGIN-->\n\n```console\n(.*?)\n```',r)
          assert m and m.group(1)==t, 'README transcript drifted from transcript.txt'
          PY
      - name: commit
        run: |
          git config user.name  'github-actions[bot]'
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git add terminal.svg transcript.txt README.md
          git diff --quiet --cached && exit 0
          git commit -m 'render terminal.svg from session.dsl'
          git pull --rebase --autostash origin "${GITHUB_REF_NAME}"
          git push
```

Push-triggered only: there is no cron, so there is nothing for GitHub's 60-day scheduled-workflow reaper to disable. If the workflow rots entirely the profile is untouched, because **the committed SVG is the artifact** — CI only regenerates it.

---

## 8. `docs/systems/*.md` — the shape each must take

Three files, ~400–600 words each, structured identically. This is the graft that converts the whole page from decoration into evidence, and it is the part a hiring manager actually reads:

1. **What it does** (2 sentences) · 2. **Shape of the data** — orders of magnitude only (rows, GB/day, events/s) · 3. **The architecture**, one `flowchart TD` Mermaid diagram, ≤8 nodes · 4. **The tradeoff taken** and the option rejected, with the reason · 5. **The number that moved** — before → after, and how it was measured · 6. **What broke** and what changed afterwards.

Hard constraint, non-negotiable: **no employer name, no internal hostnames, no service names, no port numbers, no dashboard screenshots, no schema DDL.** Describe patterns and magnitudes, never topology. One of the runner-up concepts was downgraded specifically because its equivalent content would have become a conversation with a security team; write these as if a competitor's engineer will read them, because one will.

---

## 9. Build order

| # | Step | Verify |
|---|---|---|
| 1 | Create repo `lucianobosco/lucianobosco` (public, README, `main`). | The profile page shows the README. |
| 2 | Drop in `tools/render.py`, `tools/inject.py`, `session.dsl` from the working tree. Run `python3 tools/render.py session.dsl terminal.svg transcript.txt`. | Prints `835x614  27 rows  82 cols  16.0s`. Re-run: byte-identical output. |
| 3 | **Editorial pass on `session.dsl` only** — resolve the decisions in §10. Re-render. | `render.py` fails loudly on a ragged table; width auto-adjusts to the longest line. |
| 4 | Open `harness.html` (image at 835 px **and** 390 px, on a white page). Watch it once end to end. | Error at ~2.9 s; switch flips at ~6.1 s; caret walks *with* the text; at rest all 27 rows readable. |
| 5 | Open `inline.html`, run `at(5600)` then `at(6500)` in the console. | `{off:"1", on:"0"}` then `{off:"0", on:"1"}`. This is the only frame that can fail into garbage — check it every time the DSL changes. |
| 6 | Write `README.md`, run `inject.py`, commit `README.md terminal.svg transcript.txt session.dsl tools/`. | — |
| 7 | `curl -sSI https://raw.githubusercontent.com/lucianobosco/lucianobosco/main/terminal.svg \| grep -i content-type` | Must be `image/svg+xml`. `text/plain` means the path is wrong. |
| 8 | Hard-reload the profile (raw caches 300 s; append `?v=2` to `src` if impatient). Check with GitHub in light **and** dark theme, and once on a real phone. | Panel is dark in both (intentional, framed as a floating window); the open transcript carries the phone. |
| 9 | Add `.github/workflows/render.yml` last, and push a one-character `session.dsl` change to prove it round-trips. | Green run; a commit from `github-actions[bot]` touching only generated files. |
| 10 | Write the three `docs/systems/*.md`. | Ship the profile without them if needed — but the page is only half-delivered until they exist. |

---

## 10. Needs the owner's decision

**Blocking — these are facts about him or his employer that the image asserts:**

1. **Every hostname, IP, port and tunnel name in the transcript.** `10.24.6.11`, `catalog-db-prod`, `videos-db-replica`, `catalog`, `luciano.repos`, ports `13306/13307`, `~/.config/tunnels.toml`, `-n platform`, `-l app=ingest`, `ingest-worker-4b8qz`. If any of these resemble something real, change them. The design goal is that it reads as real, which is precisely why nothing in it may *be* real.
2. **The exact `mysql` error string for the client he actually runs.** Different clients/versions print the host with or without the port and with or without a decoded errno. Run it against a black-holed IP and paste the literal output into `session.dsl`. Same for `ss -ltnp` — paste real output; the `fd=11` and the untruncated 15-char `comm` are the details a reader will check.
3. **`tunnels-manager 0.4` and "6 tunnels".** Must match the real repo's current version and a plausible config.
4. **"14 years".** The only self-quantifying claim left (the guessed years-per-layer column was cut). It needs a one-character edit each year — or replace with "since 2012", which never rots.
5. **The three write-up topics and their contents** (§8), including the NDA read-through. This is the one place a mistake has consequences beyond a profile page.

**Design choices, defaults stated:**

6. **Height.** 614 px. If that is still too much of a viewport, cutting the `kubectl` act removes 4 rows (−78 px, −2.6 s) and costs the best line on the page (*"the whole job is making that line boring"*). Default: keep it.
7. **Mobile.** Default: accept that the image is desktop-only and let `<details open>` + the three Markdown lines carry phones. Alternative, ~1 hour: a `session-narrow.dsl` (≤48 columns, same generator, different content) served via `<picture><source media="(max-width:600px)">` — costs a second transcript to keep in editorial sync, and GitHub's native mobile apps may ignore `<picture>` entirely.
8. **Light-theme variant.** Default: one dark panel on both themes, framed with a `#26313d` border so it reads as an intentional floating window. `<picture>` + a second palette is available but doubles the artifact to keep in sync — one runner-up was marked down specifically for that maintenance cost.
9. **Typing speed.** 15 ms/char. Faster stops reading as typing; slower pushes past 16 s.

**Known and accepted, not fixable:**

10. The text inside the SVG is unselectable, unsearchable, and invisible to screen readers. The `<details open>` transcript is not a nicety — it is the entire accessibility and mobile story, and CI fails if it drifts from the render.
11. On Windows the font stack resolves to Consolas (0.550 advance) and `lengthAdjust="spacing"` adds ~0.9 px of tracking per character. Alignment stays exact; the type looks slightly loose. That is the correct trade against a caret nine characters off the text.