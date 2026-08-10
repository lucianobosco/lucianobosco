#!/usr/bin/env python3
"""tunnels-manager.svg: one row of the app, open, with the light still moving.

The profile used to carry a screenshot of this. A screenshot cannot show the one thing the
row is for -- the pulse walking the path while a hop is being negotiated -- so the row is
drawn instead, from the same numbers the app lays it out with (see its ui/css.py).

Rules this file follows, learned from the terminal SVG next door:
  * The resting state is a static declaration, and nothing readable depends on the
    animation: with no animation at all the row is complete and the wires are simply
    quiet, which is what the app draws for an idle tunnel.
  * CSS transforms only, and infinite. GitHub loads this through an <img>, where scripts
    never run and Chrome drops animations whose delay lands mid-timeline.
  * No external font, no gradient object, nothing to fetch: one file, no dependencies.

    python3 tools/render-row.py tunnels-manager.svg
"""

from __future__ import annotations

import sys

W, H = 1000, 212
CARD_H = 58  # the header, before the row is opened

# palette: the app's own values (tunnels_manager/ui/css.py)
PAGE = "#16161a"
CARD = "#26262c"
EDGE = "#ffffff1f"
NODE = "#2b2b33"
NODE_EDGE = "#ffffff1a"
TITLE = "#eceaee"
DIM = "#94949f"
FAINT = "#7c7c88"
GREEN = "#2ec27e"
BLUE = "#62a0ea"
SWITCH = "#3584e4"
FIELD = "#16161a"

# the two hops, as x ranges: the pulse walks the first, then the second
WIRE_Y = 105
HOP1 = (200, 412)
HOP2 = (578, 786)
CYCLE = 2.4  # seconds for one pulse to walk the whole path


def wire(x0: int, x1: int) -> str:
    return (
        f'<line x1="{x0}" y1="{WIRE_Y}" x2="{x1}" y2="{WIRE_Y}" stroke="#ffffff24" '
        f'stroke-width="2" stroke-dasharray="3 5"/>'
    )


#: The pulse is as long as the app draws it: a third of the hop, give or take.
SPAN = 90


def pulse(x0: int, cls: str) -> str:
    """The light itself: a stretch of wire that brightens in the middle and fades out at
    both ends, which is what the app paints in Cairo. Two flat bars read as a smear on a
    dashed line; a gradient reads as light.

    Invisible at rest -- the animation is what brings it in -- so a still of this file is a
    quiet path rather than a stray blob.
    """
    return (
        f'<g class="pulse {cls}">'
        f'<rect x="{x0}" y="{WIRE_Y - 1.8}" width="{SPAN}" height="3.6" '
        f'fill="url(#glow)"/></g>'
    )


def node(x: int, w: int, title: str, detail: str, kind: str = "") -> str:
    """A box in the path: a name, a line of detail, and a LED when it carries a state."""
    stroke = {"up": "#2ec27e8c", "proxy": "#62a0ea73"}.get(kind, NODE_EDGE)
    fill = "#2ec27e12" if kind == "up" else NODE
    led = ""
    text_x = x + 14
    if kind == "up":
        led = f'<circle cx="{x + 14}" cy="{WIRE_Y - 11}" r="3.4" fill="{GREEN}"/>'
        text_x = x + 24
    elif kind == "proxy":
        # a padlock, drawn rather than an icon font: body plus shackle
        led = (
            f'<rect x="{x + 10}" y="{WIRE_Y - 13}" width="9" height="7" rx="1.6" '
            f'fill="{TITLE}"/>'
            f'<path d="M{x + 12} {WIRE_Y - 13}v-2.4a2.5 2.5 0 0 1 5 0v2.4" fill="none" '
            f'stroke="{TITLE}" stroke-width="1.4"/>'
        )
        text_x = x + 25
    return (
        f'<rect x="{x}" y="{WIRE_Y - 29}" width="{w}" height="58" rx="8" fill="{fill}" '
        f'stroke="{stroke}"/>{led}'
        f'<text class="ui b" x="{text_x}" y="{WIRE_Y - 6}" font-size="13" fill="{TITLE}">'
        f"{title}</text>"
        f'<text class="mono" x="{x + 14}" y="{WIRE_Y + 14}" font-size="11" fill="{FAINT}">'
        f"{detail}</text>"
    )


def svg() -> str:
    spark = "M0 22 L11 15 L22 19 L33 8 L44 14 L55 6 L66 11 L74 9"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" \
height="{H}" role="img">
<title>One row of tunnels-manager, open: a port-forward from this machine through a local
process to svc/my-dashboard, established, with the round trip measured through the tunnel
at under a millisecond.</title>
<style>
  .ui   {{ font-family: ui-sans-serif, -apple-system, "Segoe UI", Cantarell, "Noto Sans", sans-serif }}
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "DejaVu Sans Mono", monospace }}
  .b    {{ font-weight: 700 }}
  /* Decoration, and only decoration, moves: the pulse is invisible at rest and the
     animation is what makes it appear. Where an animation is not run -- reduced motion, a
     renderer that ignores CSS -- the wires are simply dashed and quiet, which is exactly
     what the app draws for a tunnel that is idle. Nothing readable depends on it. */
  .pulse {{ opacity: 0; transform: translate(0, 0); animation: walk1 {CYCLE}s linear infinite }}
  .hop2  {{ animation-name: walk2 }}
  /* Each pulse starts where its hop starts and ends where the hop ends, and the two take
     turns: the first half of the cycle walks hop one, the second half walks hop two, so
     the light arrives at the proxy before it leaves for the far end. */
  @keyframes walk1 {{
    0%   {{ transform: translate(0, 0); opacity: 0 }}
    4%   {{ opacity: 1 }}
    44%  {{ opacity: 1 }}
    48%  {{ transform: translate({HOP1[1] - HOP1[0] - SPAN}px, 0); opacity: 0 }}
    100% {{ transform: translate({HOP1[1] - HOP1[0] - SPAN}px, 0); opacity: 0 }}
  }}
  @keyframes walk2 {{
    0%, 48% {{ transform: translate(0, 0); opacity: 0 }}
    52%  {{ opacity: 1 }}
    94%  {{ opacity: 1 }}
    98%, 100% {{ transform: translate({HOP2[1] - HOP2[0] - SPAN}px, 0); opacity: 0 }}
  }}
  @media (prefers-reduced-motion: reduce) {{ .pulse {{ animation: none }} }}
</style>
<defs>
  <linearGradient id="glow" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>
    <stop offset=".3" stop-color="{BLUE}" stop-opacity=".7"/>
    <stop offset=".5" stop-color="#cfe6ff" stop-opacity="1"/>
    <stop offset=".7" stop-color="{BLUE}" stop-opacity=".7"/>
    <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="10" fill="{PAGE}"/>
<rect x="3" y="1" width="{W - 4}" height="{H - 2}" rx="9" fill="{CARD}" stroke="{EDGE}"/>
<rect x="0" y="1" width="3" height="{H - 2}" fill="{GREEN}"/>

<!-- the header, as the closed row shows it -->
<circle cx="22" cy="29" r="8" fill="{GREEN}" opacity=".22"/>
<circle cx="22" cy="29" r="3.5" fill="{GREEN}"/>
<text class="mono b" x="41" y="27" font-size="14" fill="{TITLE}">Internal dashboard</text>
<text class="ui" x="41" y="44" font-size="12" fill="{DIM}">kubernetes</text>
<rect x="322" y="19" width="78" height="20" rx="5" fill="#ffffff17"/>
<text class="mono b" x="331" y="33" font-size="10.5" fill="#b0aeb5">PORT-FWD</text>
<text class="mono" x="492" y="33" font-size="13" fill="{TITLE}" text-anchor="end">:8096</text>
<text class="mono" x="516" y="33" font-size="13" fill="{DIM}">svc/my-dashboard:80</text>
<text class="mono b" x="752" y="26" font-size="12" fill="{GREEN}">ESTABLISHED</text>
<text class="mono" x="752" y="41" font-size="10.5" fill="{DIM}">24s</text>
<g fill="{DIM}"><circle cx="872" cy="22" r="1.7"/><circle cx="872" cy="29" r="1.7"/>\
<circle cx="872" cy="36" r="1.7"/></g>
<rect x="890" y="17" width="46" height="24" rx="12" fill="{SWITCH}"/>
<circle cx="924" cy="29" r="9" fill="#ffffff"/>
<path d="M950 26l6 6 6-6" fill="none" stroke="{FAINT}" stroke-width="1.6" \
stroke-linecap="round" stroke-linejoin="round"/>

<!-- the path the row opens onto -->
{node(36, 156, "localhost", "127.0.0.1 · :8096")}
<text class="ui" x="{(HOP1[0] + HOP1[1]) // 2}" y="{WIRE_Y - 16}" font-size="10.5" \
fill="{FAINT}" text-anchor="middle">port-forward</text>
{wire(*HOP1)}
{pulse(HOP1[0], "hop1")}
<text class="mono" x="{(HOP1[0] + HOP1[1]) // 2}" y="{WIRE_Y + 22}" font-size="10.5" \
fill="{FAINT}" text-anchor="middle">python3</text>
{node(420, 158, "local process", "established · &lt;1 ms", "proxy")}
{wire(*HOP2)}
{pulse(HOP2[0], "hop2")}
<text class="mono" x="{(HOP2[0] + HOP2[1]) // 2}" y="{WIRE_Y + 22}" font-size="10.5" \
fill="{FAINT}" text-anchor="middle">svc/my-dashboard:80</text>
{node(794, 170, "svc/my-dashboard:80", "kubernetes", "up")}

<!-- what you paste, and the round trip -->
<rect x="36" y="150" width="784" height="38" rx="8" fill="{FIELD}" stroke="{EDGE}"/>
<text class="mono" x="52" y="174" font-size="13" fill="#c9c9d1">127.0.0.1:8096</text>
<text class="mono" x="804" y="174" font-size="11.5" fill="{GREEN}" text-anchor="end">\
✓ established</text>
<rect x="830" y="152" width="56" height="34" rx="8" fill="{SWITCH}"/>
<text class="ui b" x="858" y="174" font-size="12.5" fill="#ffffff" text-anchor="middle">\
Copy</text>
<g transform="translate(900,150)"><path d="{spark}" fill="none" stroke="{GREEN}" \
stroke-width="1.4"/><circle cx="74" cy="9" r="2.1" fill="{GREEN}"/></g>
<text class="mono" x="974" y="192" font-size="10.5" fill="{FAINT}" text-anchor="end">\
rtt &lt;1 ms</text>
</svg>
"""


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "tunnels-manager.svg"
    body = svg()
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(body)
    print(f"{out}: {len(body) / 1024:.1f} KB  {W}x{H}")
