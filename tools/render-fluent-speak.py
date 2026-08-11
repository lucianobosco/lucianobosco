#!/usr/bin/env python3
"""fluent-speak.svg: the loop, its measured numbers, and the word it loses.

The obvious drawing would be three boxes with arrows, which says "STT, LLM, TTS" and
nothing else -- every voice project has those three boxes. What this project actually
found is in the numbers under them and in the last line: what travels between two
agents is what the other one *understood*, so a mishearing enters the conversation and
stays there. "Stripe" became "Constraip" for four turns and both agents went on
discussing the invented provider, with the WER barely moving, because it is one word
among many. That is the thing worth drawing.

Rules, the same as the other generated SVGs here:
  * the resting state is the finished diagram, numbers and all. The animation only
    replays the trip. Where no animation runs, the image is the whole explanation.
  * CSS only, infinite, no scripts: GitHub serves this through an <img>.
  * every number is real and comes from RESULTS.md in the repo, measured on an
    RTX A5000 over OpenSLR SLR61. The Spanish is the spoken material, which is the
    one thing in that repository that is deliberately not in English.

    python3 tools/render-fluent-speak.py fluent-speak.svg
"""

from __future__ import annotations

import sys

W, H = 1000, 258

# Its own palette: a dark console ground, warm off-white for what is spoken, steel for
# the signal path, ochre for anything measured, and rust for what was lost.
GROUND = "#111419"
CARD = "#191d24"
LINE = "#ffffff1f"
INK = "#e9e4d9"
INK_SOFT = "#8d8b85"
SIGNAL = "#7aa2c8"
MEASURED = "#d0a02c"
LOST = "#c2643f"

CYCLE = 7.0  # seconds for the whole trip to replay

# (x, label, model, metric). Left to right, in the order the audio travels.
STATIONS = [
    (208, "HEARS", "large-v3-turbo", "2.0% WER · 19× realtime"),
    (470, "THINKS", "llama3.1:8b", "0.75s to the first sentence"),
    (732, "SPEAKS", "edge · es-AR-Tomas", "1.4% round-trip WER"),
]
BOX_W, BOX_H = 224, 74
TOP = 92


def waveform(x: float, y: float, width: float, bars: int = 26) -> str:
    """A little level meter, so the thing on the wire reads as audio."""
    import math

    out = []
    step = width / bars
    for i in range(bars):
        # Deterministic, not random: the file has to be byte-identical between runs
        height = 4 + 10 * abs(math.sin(i * 1.7)) * (0.45 + 0.55 * abs(math.cos(i * 0.6)))
        out.append(
            f'<rect x="{x + i * step:.1f}" y="{y - height / 2:.1f}" width="{step * 0.5:.1f}" '
            f'height="{height:.1f}" rx="1" fill="{SIGNAL}" opacity=".55"/>'
        )
    return "".join(out)


def svg() -> str:
    boxes, labels = [], []
    for x, label, model, metric in STATIONS:
        boxes.append(
            f'<rect x="{x}" y="{TOP}" width="{BOX_W}" height="{BOX_H}" rx="9" '
            f'fill="{CARD}" stroke="{LINE}"/>'
        )
        labels.append(
            f'<text class="ui tag" x="{x + 16}" y="{TOP + 21}" fill="{INK_SOFT}">{label}</text>'
            f'<text class="ui model" x="{x + 16}" y="{TOP + 42}" fill="{INK}">{model}</text>'
            f'<text class="ui num" x="{x + 16}" y="{TOP + 62}" fill="{MEASURED}">{metric}</text>'
        )

    # The wire runs behind the boxes, from the waveform to the last one
    wire_y = TOP + BOX_H / 2
    arrows = []
    for i in range(len(STATIONS) - 1):
        x0 = STATIONS[i][0] + BOX_W
        x1 = STATIONS[i + 1][0]
        arrows.append(
            f'<path d="M{x0} {wire_y} H{x1 - 7}" stroke="{LINE}" stroke-width="1.5" fill="none"/>'
            f'<path d="M{x1 - 9} {wire_y - 4} l5 4 -5 4" stroke="{INK_SOFT}" '
            f'stroke-width="1.5" fill="none"/>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" \
height="{H}" role="img">
<title>A voice assistant measured module by module: a phrase is heard by
large-v3-turbo at 2.0% word error, answered by llama3.1:8b in 0.75 seconds, spoken back
by a Rioplatense edge-tts voice at 1.4% round-trip error — and what the next agent
receives is what it understood, one word already wrong.</title>
<style>
  .ui {{ font-family: ui-sans-serif, -apple-system, "Segoe UI", Cantarell, "Noto Sans", sans-serif }}
  .mono {{ font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace }}
  .h     {{ font-size: 14.5px; font-weight: 700; fill: {INK} }}
  .sub   {{ font-size: 12.5px; fill: {INK_SOFT} }}
  .tag   {{ font-size: 10px; font-weight: 700; letter-spacing: .1em }}
  .model {{ font-size: 14px; font-weight: 600 }}
  .num   {{ font-size: 11.5px; font-weight: 600 }}
  .said  {{ font-size: 13px }}
  .note  {{ font-size: 11.5px }}

  /* The resting state is the finished diagram: every box, every number and the line
     at the bottom are painted with no animation at all. What replays is only the trip
     — a pulse of light along the wire — so an image where animation never runs still
     explains the whole thing. */
  .pulse {{ animation: {CYCLE}s linear infinite travel; opacity: 0 }}
  .meter {{ animation: {CYCLE}s ease-in-out infinite listen }}

  @keyframes travel {{
    0%, 4%    {{ transform: translateX(0); opacity: 0 }}
    10%       {{ opacity: .95 }}
    64%       {{ transform: translateX({STATIONS[-1][0] + BOX_W - 188}px); opacity: .95 }}
    72%, 100% {{ transform: translateX({STATIONS[-1][0] + BOX_W - 188}px); opacity: 0 }}
  }}
  /* The meter only leans while the phrase is being taken in */
  @keyframes listen {{
    0%, 6%   {{ opacity: .35 }}
    14%, 26% {{ opacity: 1 }}
    40%, 100% {{ opacity: .35 }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .pulse, .meter {{ animation: none }}
    .pulse {{ opacity: 0 }}
    .meter {{ opacity: 1 }}
  }}
</style>
<rect width="{W}" height="{H}" rx="10" fill="{GROUND}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="9.5" fill="none" stroke="{LINE}"/>

<text class="ui h" x="26" y="34">Every model in the loop was chosen by measuring, not by \
ear</text>
<text class="ui sub" x="26" y="55">Twelve transcription combinations, thirteen voices, \
seventeen reasoning models. RTX A5000.</text>

<!-- the audio going in -->
<g class="meter">{waveform(30, TOP + BOX_H / 2, 150)}</g>

{"".join(arrows)}

<!-- The pulse walks the wire behind the cards, so it only shows in the gaps between
     stations: over a card it would smudge across the model name. Parked and invisible
     at rest, so it never owns the resting state. -->
<g class="pulse">
  <circle cx="188" cy="{TOP + BOX_H / 2}" r="4.5" fill="{SIGNAL}"/>
  <circle cx="188" cy="{TOP + BOX_H / 2}" r="9" fill="{SIGNAL}" opacity=".25"/>
</g>

{"".join(boxes)}
{"".join(labels)}

<!-- and the part no metric catches -->
<text class="mono said" x="26" y="212" fill="{INK_SOFT}">said</text>
<text class="mono said" x="72" y="212" fill="{INK}">tocá el bucket de \
<tspan fill="{INK}">Stripe</tspan></text>
<text class="mono said" x="26" y="234" fill="{INK_SOFT}">heard</text>
<text class="mono said" x="72" y="234" fill="{INK}">tocá el bucket de \
<tspan fill="{LOST}" text-decoration="underline">Constraip</tspan></text>
<text class="ui note" x="{W - 26}" y="212" text-anchor="end" fill="{INK_SOFT}">\
What the next agent receives is what it understood, not what was said.</text>
<text class="ui note" x="{W - 26}" y="234" text-anchor="end" fill="{INK_SOFT}">\
So one wrong word travels — and the error rate barely moves. That is the point.</text>
</svg>
"""


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "fluent-speak.svg"
    body = svg()
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(body)
    print(f"{out}: {len(body) / 1024:.1f} KB  {W}x{H}")
