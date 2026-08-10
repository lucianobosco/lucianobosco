#!/usr/bin/env python3
"""next-holiday.svg: what a "puente" is, drawn in the site's own colours.

A countdown would have been the obvious image, and it would have been a lie: an SVG cannot
know the date, so the numbers would be invented. This draws the rule instead -- a holiday on
Tuesday, one day asked for, four days off -- which is the idea the site sells and is true
whatever day you look at it.

Rules, the same as the other generated SVGs here:
  * the resting state is the finished diagram, and the animation only replays how it is
    built. Where no animation runs, the image is the whole explanation.
  * CSS only, infinite, no scripts: GitHub serves this through an <img>.
  * palette lifted from the site (src/styles/global.css in the next-holiday repo).

    python3 tools/render-holiday.py next-holiday.svg
"""

from __future__ import annotations

import sys

W, H = 1000, 226

# the site's own tokens
PAPER = "#f4e9d2"
CARD = "#fbf5e8"
LINE = "#e2d2b2"
INK = "#2c2017"
INK_SOFT = "#6b5b48"
TERRACOTTA = "#b03d1e"
TERRACOTTA_SOFT = "#e7c3b2"
OCHRE = "#c0851f"
OCHRE_SOFT = "#eed9a6"
OLIVE = "#6c7138"

DAYS = ["sáb", "dom", "lun", "mar", "mié", "jue", "vie"]
HOLIDAY = 3  # Tuesday, which is the classic case
ASKED = 2  # the Monday you ask for
OFF = (0, 3)  # the run of days that ends up free, inclusive

CELL_W, CELL_H, GAP = 108, 74, 12
LEFT, TOP = 26, 92
CYCLE = 6.0  # seconds for the whole explanation to replay


def cell_x(index: int) -> int:
    return LEFT + index * (CELL_W + GAP)


def svg() -> str:
    cells, labels = [], []
    for index, day in enumerate(DAYS):
        x = cell_x(index)
        weekend = index < 2
        fill = TERRACOTTA if index == HOLIDAY else (PAPER if weekend else CARD)
        stroke = TERRACOTTA if index == HOLIDAY else LINE
        cells.append(
            f'<rect x="{x}" y="{TOP}" width="{CELL_W}" height="{CELL_H}" rx="9" '
            f'fill="{fill}" stroke="{stroke}"/>'
        )
        colour = CARD if index == HOLIDAY else INK_SOFT
        labels.append(
            f'<text class="day" x="{x + CELL_W / 2:.0f}" y="{TOP - 12}" '
            f'text-anchor="middle" fill="{INK_SOFT}">{day}</text>'
        )
        if index == HOLIDAY:
            labels.append(
                f'<text class="in-cell" x="{x + CELL_W / 2:.0f}" y="{TOP + 44}" '
                f'text-anchor="middle" fill="{colour}">festivo</text>'
            )

    asked_x = cell_x(ASKED)
    bar_x0, bar_x1 = cell_x(OFF[0]), cell_x(OFF[1]) + CELL_W
    bar_y = TOP + CELL_H + 18

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" \
height="{H}" role="img">
<title>A week where the public holiday falls on Tuesday: asking for the Monday off turns the
weekend, the Monday and the holiday into four days off in a row -- a "puente".</title>
<style>
  .ui {{ font-family: ui-sans-serif, -apple-system, "Segoe UI", Cantarell, "Noto Sans", sans-serif }}
  .h    {{ font-size: 15px; font-weight: 700; fill: {INK} }}
  .sub  {{ font-size: 12.5px; fill: {INK_SOFT} }}
  .day  {{ font-size: 12px; letter-spacing: .04em }}
  .in-cell {{ font-size: 12.5px; font-weight: 700 }}
  .note {{ font-size: 12.5px; font-weight: 700 }}

  /* The resting state is the finished diagram: the day is asked for and the four days are
     counted. The animation only replays how it got there, so an image with no animation at
     all still explains the whole thing. */
  .asked, .bar, .bar-note {{ animation: {CYCLE}s linear infinite }}
  .asked      {{ animation-name: appear }}
  .bar        {{ animation-name: sweep }}
  .bar-note   {{ animation-name: appear-late }}

  @keyframes appear {{
    0%, 18% {{ opacity: 0 }}
    26%, 100% {{ opacity: 1 }}
  }}
  @keyframes sweep {{
    0%, 30% {{ transform: scaleX(0) }}
    52%, 100% {{ transform: scaleX(1) }}
  }}
  @keyframes appear-late {{
    0%, 52% {{ opacity: 0 }}
    60%, 100% {{ opacity: 1 }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .asked, .bar, .bar-note {{ animation: none }}
  }}
</style>
<rect width="{W}" height="{H}" rx="10" fill="{PAPER}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="9.5" fill="none" stroke="{LINE}"/>

<text class="ui h" x="{LEFT}" y="34">A <tspan font-style="italic">puente</tspan>, which is \
what the site is for</text>
<text class="ui sub" x="{LEFT}" y="55">The holiday falls on a Tuesday. Ask for the Monday, and \
the weekend joins in.</text>

{''.join(cells)}
{''.join(labels)}

<!-- the day you ask for -->
<g class="asked">
  <rect x="{asked_x}" y="{TOP}" width="{CELL_W}" height="{CELL_H}" rx="9" \
fill="{OCHRE_SOFT}" stroke="{OCHRE}" stroke-dasharray="4 3"/>
  <text class="ui in-cell" x="{asked_x + CELL_W / 2:.0f}" y="{TOP + 44}" \
text-anchor="middle" fill="#78500c">pides 1 día</text>
</g>

<!-- the run of days that ends up free -->
<g class="bar" style="transform-origin: {bar_x0}px {bar_y}px">
  <rect x="{bar_x0}" y="{bar_y}" width="{bar_x1 - bar_x0}" height="7" rx="3.5" \
fill="{OLIVE}"/>
</g>
<text class="ui note bar-note" x="{bar_x0}" y="{bar_y + 26}" fill="{OLIVE}">four days off, \
one of them yours</text>
<text class="ui sub bar-note" x="{W - LEFT}" y="{bar_y + 26}" text-anchor="end">\
elproximofestivo.es</text>
</svg>
"""


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "next-holiday.svg"
    body = svg()
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(body)
    print(f"{out}: {len(body) / 1024:.1f} KB  {W}x{H}")
