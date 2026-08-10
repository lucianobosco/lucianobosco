# Designs

Three concepts came out of a research run: 26 agents swept the web for profile READMEs
that do something unusual, a skeptic pass checked every promising technique against what
GitHub's sanitiser and image proxy actually allow, and three judges — a hiring manager, a
designer, and the person who would have to maintain it — scored the results.

| Design | Score | State | What it is |
| --- | --- | --- | --- |
| [`terminal`](terminal/) | **7.3** | **built, live** | A terminal session: a production database connection times out, his own app opens the tunnel, and his bio comes back as a MySQL result set |
| [`terminal-long`](terminal-long/) | 7.3 | built | The same session, longer: adds a `SELECT * FROM luciano.stack` table and a `kubectl --watch` act. 920×877, 26.6 s |
| [`concepts/app-panel`](concepts/app-panel.md) | 6.7 | concept only | The README *is* the app's window, and the private work is a `403` you can request access to |
| [`concepts/live-probes`](concepts/live-probes.md) | 6.3 | concept only | The README is the app wired to live probes, regenerated on a schedule |

Switch which one the profile shows:

```bash
./switch.sh                 # list them, marking the live one
./switch.sh terminal-long   # then commit terminal.svg and README.md
```

## How the built ones work

A plain-text DSL describes the session line by line; `render.py` (stdlib only, no
dependencies) turns it into a self-contained animated SVG. The SVG is committed and
referenced from the README with a relative path, so it is served from
`raw.githubusercontent.com` as `image/svg+xml` — no third-party service, nothing to rate
limit, nothing that can go down.

```bash
cd designs/terminal
python3 render.py session.dsl terminal.svg transcript.txt
```

Edit `session.dsl` and re-render. That file is the only one worth touching.

## The rule that makes it work

GitHub loads the SVG through an `<img>`, and **Chrome silently drops sub-frame CSS
animations inside an SVG loaded that way**. The first build lost twenty lines to it: they
sat at `opacity: 0` forever while `getAnimations()` cheerfully reported `finished`.

The fix is a rule worth keeping: **never let an animation own the resting state.** The
resting value is a static declaration, and the animation only borrows the element on the
way in:

```css
.l, .ch { opacity: 1; animation: appear .09s linear backwards }
@keyframes appear { from { opacity: 0 } }
```

`backwards` applies the first keyframe *during the delay* and hands the element back
afterwards. That also makes the fallbacks free: with no animation support, with
`prefers-reduced-motion`, or for anyone arriving after it finished, the image is the
complete transcript.

## What the research rejected

Every technique that survived verification is listed in the plan
([`concepts/synthesis-plan.md`](concepts/synthesis-plan.md)). What was deliberately left
out is just as useful:

- **Visitor counters, trophy cases, streak cards** — every profile has them; they say
  nothing about the person.
- **The snake eating the contribution graph** — beautiful once, now furniture.
- **Generic typing-SVG one-liners** ("Full Stack Developer | Coffee Lover") — the
  technique is fine, the content is the problem.
- **Anything on a cron that shows a date or a count that can rot** — a profile that says
  "last updated 8 months ago" is worse than one that says nothing.
- **Games driven by public issues** — genuinely impressive, but the wow depends on
  strangers playing along, and it opens an inbox.
