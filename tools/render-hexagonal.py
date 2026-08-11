#!/usr/bin/env python3
"""ddd-hexagonal-php.svg: the boundary, and the day it earned its keep.

The obvious drawing is a hexagon with "domain" in the middle, and it says nothing that
the words "hexagonal architecture" have not already said. What actually happened to this
project is worth a picture: the API it was built on was deprecated, and the fix was to
write a second adapter behind the interface that was already there. Nothing above that
line moved — not the use case, not the domain, not one test.

So the drawing is the dependency arrow on top, the port as a line, and two adapters
hanging off it: the one that died and the one that took over.

Rules, the same as the other generated SVGs here:
  * the resting state is the finished diagram — the REST adapter already struck out, the
    fixture one already live. The animation only replays the handover, so an image where
    animation never runs still explains the whole thing.
  * CSS only, infinite, no scripts: GitHub serves this through an <img>.
  * a light technical-drawing palette, to sit apart from the two dark ones above it.

    python3 tools/render-hexagonal.py ddd-hexagonal-php.svg
"""

from __future__ import annotations

import sys

W, H = 1000, 302

# A blueprint, rather than a fourth dark card: pale ground, indigo rules, ink text.
GROUND = "#eef1f6"
CARD = "#ffffff"
RULE = "#c3ccdd"
INK = "#212a3e"
INK_SOFT = "#6b7793"
PORT = "#4a5c94"
LIVE = "#2f7d5a"
DEAD = "#a8583f"

CYCLE = 8.0  # seconds for the handover to replay

# (x, layer, what lives there). Left to right, and the dependency arrow runs with them.
LAYERS = [
    (26, "INFRASTRUCTURE", "CountryController"),
    (338, "APPLICATION", "CountryChecker"),
    (650, "DOMAIN", "Criteria · the port"),
]
BOX_W, BOX_H = 288, 62
TOP = 74

PORT_Y = 172
# Under the Infrastructure column, because that is where an adapter lives. Nothing
# hangs off the Domain end of the port, which is the point of the port.
ADAPTERS = [
    (26, "RestCountriesRepository", "v3.1 deprecated", DEAD),
    (338, "FixtureCountryRepository", "default, no network", LIVE),
]


def svg() -> str:
    boxes = []
    for x, layer, what in LAYERS:
        boxes.append(
            f'<rect x="{x}" y="{TOP}" width="{BOX_W}" height="{BOX_H}" rx="7" '
            f'fill="{CARD}" stroke="{RULE}"/>'
            f'<text class="ui tag" x="{x + 14}" y="{TOP + 21}" fill="{INK_SOFT}">{layer}</text>'
            f'<text class="mono what" x="{x + 14}" y="{TOP + 45}" fill="{INK}">{what}</text>'
        )

    arrows = []
    for i in range(len(LAYERS) - 1):
        x0 = LAYERS[i][0] + BOX_W
        x1 = LAYERS[i + 1][0]
        mid = TOP + BOX_H / 2
        arrows.append(
            f'<path d="M{x0 + 4} {mid} H{x1 - 9}" stroke="{PORT}" stroke-width="1.5"/>'
            f'<path d="M{x1 - 11} {mid - 4} l5 4 -5 4" stroke="{PORT}" stroke-width="1.5" fill="none"/>'
        )

    adapters = []
    for x, name, note, colour in ADAPTERS:
        dead = colour == DEAD
        cls = "dead" if dead else "live"
        adapters.append(
            f'<g class="{cls}">'
            f'<path d="M{x + 90} {PORT_Y} V{PORT_Y + 26}" stroke="{colour}" stroke-width="1.5"/>'
            f'<rect x="{x}" y="{PORT_Y + 26}" width="{BOX_W}" height="{BOX_H - 4}" rx="7" '
            f'fill="{CARD}" stroke="{colour}"/>'
            f'<text class="mono what" x="{x + 14}" y="{PORT_Y + 49}" fill="{INK}">{name}</text>'
            f'<text class="ui note" x="{x + 14}" y="{PORT_Y + 70}" fill="{colour}">{note}</text>'
            # The strike lives with the adapter it crosses out, so it cannot drift
            + (
                f'<path class="strike" d="M{x + 12} {PORT_Y + 44} H{x + 12 + 196}" '
                f'stroke="{DEAD}" stroke-width="2"/>'
                if dead
                else ""
            )
            + "</g>"
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" \
height="{H}" role="img">
<title>The dependency arrow runs from infrastructure to application to domain, and the
port sits at the bottom with two adapters on it: the REST one, struck out because the API
version it was written against was deprecated, and the fixture one that replaced it. The
layers above the port did not change.</title>
<style>
  .ui {{ font-family: ui-sans-serif, -apple-system, "Segoe UI", Cantarell, "Noto Sans", sans-serif }}
  .mono {{ font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace }}
  .h    {{ font-size: 14.5px; font-weight: 700; fill: {INK} }}
  .sub  {{ font-size: 12.5px; fill: {INK_SOFT} }}
  .tag  {{ font-size: 9.5px; font-weight: 700; letter-spacing: .11em }}
  .what {{ font-size: 13px }}
  .note {{ font-size: 11px; font-weight: 600 }}
  .port {{ font-size: 10.5px; font-weight: 700; letter-spacing: .08em }}
  .foot {{ font-size: 11.5px; fill: {INK_SOFT} }}

  /* The resting state is the finished diagram: the REST adapter is already struck out
     and the fixture one is already the live path. What replays is the handover — the
     strike drawing itself, the survivor coming up — so a still frame is the whole
     story rather than half of it. */
  .strike {{
    stroke-dasharray: 200; animation: {CYCLE}s ease-in-out infinite strike;
  }}
  .dead {{ animation: {CYCLE}s ease-in-out infinite fade }}
  .live {{ animation: {CYCLE}s ease-in-out infinite arrive }}

  @keyframes strike {{
    0%, 18%   {{ stroke-dashoffset: 200 }}
    34%, 100% {{ stroke-dashoffset: 0 }}
  }}
  @keyframes fade {{
    0%, 18%   {{ opacity: 1 }}
    40%, 100% {{ opacity: .45 }}
  }}
  @keyframes arrive {{
    0%, 40%   {{ opacity: .45 }}
    56%, 100% {{ opacity: 1 }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .strike, .dead, .live {{ animation: none }}
    .strike {{ stroke-dashoffset: 0 }}
    .dead {{ opacity: .45 }}
  }}
</style>
<rect width="{W}" height="{H}" rx="10" fill="{GROUND}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="9.5" fill="none" stroke="{RULE}"/>

<text class="ui h" x="26" y="32">The port stopped being a diagram the day the API went \
away</text>
<text class="ui sub" x="26" y="52">A 2023 hiring exercise. The arrow only ever points one \
way, which is what made the swap below a new file.</text>

{"".join(arrows)}
{"".join(boxes)}

<!-- the port itself, as the line everything below hangs from -->
<path d="M26 {PORT_Y} H{W - 26}" stroke="{PORT}" stroke-width="1.5" stroke-dasharray="5 4"/>
<text class="ui port" x="26" y="{PORT_Y - 9}" fill="{PORT}">CountryRepository \
— THE PORT</text>

{"".join(adapters)}

<text class="ui foot" x="26" y="{H - 16}">Two implementations, one interface. Replacing \
the dead one changed no use case, no domain object and no test.</text>
</svg>
"""


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "ddd-hexagonal-php.svg"
    body = svg()
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(body)
    print(f"{out}: {len(body) / 1024:.1f} KB  {W}x{H}")
