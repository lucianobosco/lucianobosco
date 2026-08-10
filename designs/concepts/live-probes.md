# Concept: tunnels-manager://prod — the README is his own app, wired to live probes

> **Not built.** This is the full design from the research run, kept so it can be built
> later without redoing the work. Score: see `designs/README.md`.

## The pitch

You land on the profile and there is no profile. There is a GTK4/libadwaita window: rounded dark chrome, headerbar reading `tunnels-manager · 11 probes · 6h cadence · Málaga UTC+02:00 · measured 06:13Z`, a blinking LIVE dot, and eleven boxed-list rows each with a switch — exactly the app in his flagship repo, except the tunnels are no longer his laptop's port-forwards. Row 1 is `tunnel.cloudproxy.app`, the actual endpoint his app dials. Row 2 is Google Cloud's open-incident feed, and if GKE or BigQuery is on fire right now, that switch is amber with the product name in the target column. Below them, real 7-day sparklines — 28 measured points each, built by his own cron, not a stock widget — then a second register of countdown bars: Kubernetes 1.36, Python 3.12, MySQL 8.4, PHP 8.3, Laravel 11, each draining toward its real end-of-support date, red bars first. At the bottom, a transition log: `2026-08-08 12:13Z  gcp-incidents  UP → DEGRADED  BigQuery, us-east1`. The stare happens twice: first because it's a running dashboard where a profile should be, then again when you notice the timestamp is four hours old, refresh, and the numbers have moved. It solves his real problem — 4 public repos, 5 followers, everything else private — by not showing repos at all. It shows the substrate he operates, and it proves the claim by measuring it live.

## Why it fits him and not a generic developer

Three things are true of him and of nothing else. (1) His one public artifact is a table of rows with a switch each that hands you a connection string — so the profile is not "a dashboard", it is *his UI*, scaled from one laptop to the whole public substrate. A visitor who then opens tunnels-manager recognises the window immediately; the README is the product demo. (2) The probe set is his actual job description, not a badge wall: the IAP tunnel endpoint, GKE/BigQuery/Cloud SQL incidents, kubectl stable, Temporal releases, GitHub Actions status. Nobody who doesn't run pipelines on GCP with Temporal picks that list. (3) The countdown bars are the senior move. A junior shows commits; a 14-year engineer shows the migration clocks he's already racing — Kubernetes' 14-month support window is the most honest anxiety in his profession, rendered as a red bar. And the whole thing is a data pipeline: probe → append JSONL → aggregate → render → commit, with git as the time-series store. He builds pipelines; the profile is one, and it's readable in 60 lines of Python.

## Techniques it relies on

- Generate-in-Actions, commit-the-artifact SVG dashboard (bot commits also keep the 60-day cron reaper away)
- Repo-relative <img src="./panel-dark.svg"> so camo is bypassed entirely (max-age=300, no 24h edge cache)
- <picture> + <source media="(prefers-color-scheme: dark)"> with two generated SVGs — the only theme swap that follows GitHub's toggle rather than the OS
- Plain SVG primitives only (rect/line/text/polyline), no foreignObject, all numeric columns text-anchor="end" so OS font-metric drift cannot break alignment
- Inline <style> @keyframes + SMIL animation inside the committed SVG (style-src 'unsafe-inline' is allowed), with prefers-reduced-motion escape and animations that start from the final visual state
- Whole image wrapped in one markdown <a> (per-region links are inert), plus a plain-text mirror in <details> for screen readers
- git-as-timeseries: append-only capped JSONL ring buffer read back for sparklines, p95, uptime % and transition log — no API paging, no rate limits
- xmllint gate in CI so a malformed render is never committed; probes fail into DOWN rows instead of failing the build

## Effort

Medium-high: ~8–12 h for v1 (render.py is the bulk — 300 lines of hand-emitted SVG), then near-zero. One weekend evening gets a 6-row board live; the sparklines only look good after the history file has ~2 days of samples, so ship it and let it fill in.

## Risks

Four real ones. (1) Repo growth: two ~25 KB SVGs + a JSONL line, 4×/day ≈ 70 MB of git history per year in a repo nobody garbage-collects — mitigate by rounding latencies into 5 ms buckets (many runs then produce no diff and no commit) and truncating history once a year. (2) Third-party schema drift: endoflife.date and status.cloud.google.com are public but not contracts; the renderer must mark a row DOWN with the parse error rather than crash or, worse, invent a number. (3) XML escaping is the classic killer — one `&` in a GCP incident title voids the entire image with no error anywhere; every interpolated string goes through esc() and xmllint gates the commit. (4) Cron is best-effort: observed drift of 1–4 h is normal, and public-repo schedules are auto-disabled after 60 days of inactivity — the bot's own commits *probably* reset that clock but it's undocumented, so keep workflow_dispatch and stamp the real measurement time on the board instead of implying real-time. Minor: an SVG's text is not selectable or searchable, hence the panel.txt mirror; and treating "any HTTP status = reachable" on the IAP endpoint must be stated in the row note, or it reads as a fudge to anyone who curls it.

## Sketch

## File layout — `lucianobosco/lucianobosco` (default branch `main`)

```
README.md
panel-dark.svg          generated, committed  (~25 KB)
panel-light.svg         generated, committed
panel.txt               generated plain-text mirror (a11y + curl)
data/probes.yml         declarative probe list  (hand-edited)
data/history.jsonl      append-only ring buffer, last 730 runs (~180 days @ 4/day)
tools/probe.py          fetch + measure + append one JSONL line
tools/render.py         history -> two SVGs + panel.txt
.github/workflows/panel.yml
```

## README.md (whole thing)

```markdown
<a href="https://github.com/lucianobosco/tunnels-manager">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./panel-dark.svg">
    <img src="./panel-light.svg" width="900"
         alt="tunnels-manager control panel. 11 live probes measured 2026-08-10 06:13 UTC:
              IAP tunnel endpoint 214 ms, Google Cloud incidents 0 open, kubectl stable v1.36.3,
              GitHub Actions operational, Temporal v1.29.4, tunnels-manager 41 stars.
              End-of-support countdowns: Kubernetes 1.36 322 days, Python 3.12 511 days,
              MySQL 8.4 1204 days, PHP 8.3 143 days, Laravel 11 89 days.">
  </picture>
</a>

**Luciano Bosco** · Málaga · 14 years on databases, data pipelines, and the platforms
under video and stock content. Python · Go · PHP/Laravel · MySQL · BigQuery · GCP ·
Kubernetes · Temporal

That panel is not a mockup and not a badge. [`tools/probe.py`](tools/probe.py) dials every
target on a cron, appends the latencies to [`data/history.jsonl`](data/history.jsonl), and
[`tools/render.py`](tools/render.py) draws the SVG you are looking at. Six rows are the
substrate my work actually sits on. Five are the end-of-support clocks I plan migrations
around. Git is the time-series database; there is no server.
→ [last run](https://github.com/lucianobosco/lucianobosco/actions/workflows/panel.yml)
· [why it looks like that](https://github.com/lucianobosco/tunnels-manager)

<details><summary>Plain-text panel — screen readers, terminals, <code>curl</code></summary>

<!-- render.py rewrites the fence below in place, between the markers -->
<!--PANEL:BEGIN-->
```
tunnel.cloudproxy.app   UP    214 ms   p95 289   100.0%
gcp-incidents           UP      0 open p95   1   99.6%
...
```
<!--PANEL:END-->
</details>

<details><summary>The app the panel is dressed as</summary>

![tunnels-manager: a table of tunnels, a switch each, and the connection string](https://raw.githubusercontent.com/lucianobosco/tunnels-manager/main/docs/screenshot.png)
</details>
```

## data/probes.yml

```yaml
# kind: reach  -> any HTTP status counts as reachable; only DNS/TLS/timeout is DOWN
- {id: iap-tunnel,      kind: reach,  url: "https://tunnel.cloudproxy.app/",
   target: "tunnel.cloudproxy.app  (what the app dials)"}
- {id: gcp-incidents,   kind: gcp,    url: "https://status.cloud.google.com/incidents.json",
   watch: ["Google Kubernetes Engine","BigQuery","Cloud SQL","Cloud Storage",
           "Identity-Aware Proxy","Cloud Composer"]}
- {id: kubectl-stable,  kind: text,   url: "https://dl.k8s.io/release/stable.txt"}
- {id: gh-actions,      kind: json,   url: "https://www.githubstatus.com/api/v2/status.json",
   pick: "status.indicator", up_when: "none"}
- {id: temporal,        kind: release, repo: temporalio/temporal}
- {id: tunnels-manager, kind: repo,    repo: lucianobosco/tunnels-manager}
# kind: ttl -> endoflife.date, bar = fraction of the support window still left
- {id: k8s 1.36,     kind: ttl, product: kubernetes, cycle: "1.36"}
- {id: python 3.12,  kind: ttl, product: python,     cycle: "3.12"}
- {id: mysql 8.4,    kind: ttl, product: mysql,      cycle: "8.4"}
- {id: php 8.3,      kind: ttl, product: php,        cycle: "8.3"}
- {id: laravel 11,   kind: ttl, product: laravel,    cycle: "11"}
```

All five sources verified live and unauthenticated today:
`endoflife.date/api/kubernetes.json` → `{"cycle":"1.36","releaseDate":"2026-04-22","eol":"2027-06-28","latest":"1.36.3","support":"2027-04-28"}`;
`dl.k8s.io/release/stable.txt` → `v1.36.3`;
`githubstatus.com/api/v2/status.json` → `status.indicator: "none"`;
`status.cloud.google.com/incidents.json` → array with `id, begin, end, external_desc, status_impact, affected_products[].title, currently_affected_locations[]`.
GitHub API calls use `GITHUB_TOKEN` (5 000/h, not the anonymous 60/h).

## data/history.jsonl — one line per run, ring-buffered to 730 lines

```json
{"t":"2026-08-10T06:13:41Z","p":{
  "iap-tunnel":{"s":"up","ms":214},
  "gcp-incidents":{"s":"up","ms":180,"v":"0 open"},
  "kubectl-stable":{"s":"up","ms":95,"v":"v1.36.3"},
  "gh-actions":{"s":"up","ms":140,"v":"operational"},
  "temporal":{"s":"up","ms":210,"v":"v1.29.4","sub":"released 12 d ago"},
  "tunnels-manager":{"s":"up","ms":205,"v":"41 ★","sub":"main 9f2c1ab · 6 d ago"},
  "k8s 1.36":{"s":"up","d":322,"frac":0.74,"v":"2027-06-28"},
  "php 8.3":{"s":"warn","d":143,"frac":0.11,"v":"2026-12-31"}}}
```
`render.py` reads the last 28 lines for sparklines (7 days @ 4/day), the whole file for
p95 + uptime %, and diffs consecutive `s` values for the transition log.

## panel-dark.svg — real structure and coordinates (900 × 560)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560" width="900" height="560"
     role="img" aria-labelledby="t d">
  <title id="t">tunnels-manager control panel</title>
  <desc id="d">11 live probes, measured 2026-08-10 06:13 UTC. …same text as alt…</desc>
  <style>
    text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"DejaVu Sans Mono",monospace;
         fill:#e6edf3}
    .dim{fill:#8b949e} .lbl{font-size:9px;letter-spacing:.11em;fill:#6e7681}
    .name{font-size:12.5px} .tgt{font-size:10.5px;fill:#8b949e}
    .num{font-size:11.5px;text-anchor:end}          /* every number right-anchored:
                                                       immune to per-OS advance widths */
    .spark{fill:none;stroke:#62a0ea;stroke-width:1.4;stroke-linejoin:round;
           stroke-dasharray:520;stroke-dashoffset:0}   /* final state IS the default:
                                                          a non-animating renderer shows
                                                          the complete line */
    .knob{animation:knob .45s cubic-bezier(.2,.8,.2,1) both}
    @keyframes knob{from{transform:translateX(-17px)}to{transform:translateX(0)}}
    @keyframes draw{from{stroke-dashoffset:520}to{stroke-dashoffset:0}}
    .spark{animation:draw 1.1s ease-out}
    @keyframes live{0%,100%{opacity:1}45%{opacity:.12}}
    #live{animation:live 2.6s steps(1,end) infinite}
    @media (prefers-reduced-motion:reduce){*{animation:none!important}}
  </style>

  <!-- libadwaita window -->
  <rect x=".5" y=".5" width="899" height="559" rx="12" fill="#1e1e1e" stroke="#3d3d3d"/>
  <path d="M0 52h900" stroke="#3d3d3d"/>
  <rect x=".5" y=".5" width="899" height="51" rx="12" fill="#303030"/>
  <circle cx="20" cy="26" r="6" fill="#57e389"/>   <!-- overall: green/amber/red -->
  <circle cx="38" cy="26" r="6" fill="#4f4f4f"/><circle cx="56" cy="26" r="6" fill="#4f4f4f"/>
  <text x="450" y="23" text-anchor="middle" font-size="13" font-weight="600">tunnels-manager</text>
  <text x="450" y="38" text-anchor="middle" font-size="10" class="dim">11 probes · 6 h cadence · Málaga UTC+02:00 · measured 06:13 UTC</text>
  <circle id="live" cx="866" cy="26" r="4" fill="#ed333b"/>

  <!-- column labels -->
  <text x="76"  y="67" class="lbl">TUNNEL</text>
  <text x="248" y="67" class="lbl">TARGET</text>
  <text x="530" y="67" class="lbl" text-anchor="middle">7 DAYS</text>
  <text x="700" y="67" class="lbl" text-anchor="end">LAST</text>
  <text x="772" y="67" class="lbl" text-anchor="end">P95</text>
  <text x="858" y="67" class="lbl" text-anchor="end">UP</text>

  <!-- ROW i: top = 74 + 34*i  (probe row, ON) ------------------------------ -->
  <g transform="translate(0,74)">
    <rect x="8" y="1" width="884" height="32" rx="6" fill="#232323"/>       <!-- zebra -->
    <rect x="20" y="11" width="32" height="14" rx="7" fill="#26a269"/>
    <circle class="knob" style="animation-delay:.05s" cx="45" cy="18" r="6" fill="#fff"/>
    <text x="76"  y="22" class="name">iap-tunnel</text>
    <text x="248" y="22" class="tgt">tunnel.cloudproxy.app  (what the app dials)</text>
    <path d="M460 26h140" stroke="#333"/>
    <polyline class="spark" style="animation-delay:.05s"
      points="460,20 465,17 470,19 475,12 480,15 485,14 490,9 495,13 500,11 505,16
              510,10 515,12 520,8 525,11 530,9 535,14 540,10 545,7 550,12 555,9
              560,11 565,8 570,13 575,10 580,9 585,12 590,8 600,10"/>
    <text x="700" y="22" class="num">214 ms</text>
    <text x="772" y="22" class="num dim">289</text>
    <text x="858" y="22" class="num" fill="#57e389">100.0%</text>
  </g>

  <!-- TTL row (countdown bar instead of sparkline) --------------------------- -->
  <g transform="translate(0,346)">
    <rect x="20" y="11" width="32" height="14" rx="7" fill="#c64600"/>       <!-- warn -->
    <circle class="knob" cx="45" cy="18" r="6" fill="#fff"/>
    <text x="76"  y="22" class="name">php 8.3</text>
    <text x="248" y="22" class="tgt">security support ends 2026-12-31</text>
    <rect x="460" y="14" width="140" height="8" rx="4" fill="#3a3a3a"/>
    <rect x="460" y="14" width="15"  height="8" rx="4" fill="#ed333b"/>      <!-- frac .11 -->
    <text x="700" y="22" class="num">143 d</text>
    <text x="772" y="22" class="num dim">—</text>
    <text x="858" y="22" class="num dim">EOL</text>
  </g>

  <!-- transition log, y 448..552 -->
  <path d="M8 452h884" stroke="#3d3d3d"/>
  <text x="20" y="470" class="lbl">TRANSITIONS · LAST 5</text>
  <text x="20" y="490" font-size="10.5" class="dim">2026-08-08 12:13Z  gcp-incidents   UP → DEGRADED   BigQuery, us-east1</text>
  <text x="20" y="506" font-size="10.5" class="dim">2026-08-08 18:13Z  gcp-incidents   DEGRADED → UP   resolved in 5 h 12 m</text>
  <text x="20" y="522" font-size="10.5" class="dim">2026-08-05 00:13Z  kubectl-stable  v1.36.2 → v1.36.3</text>
  <text x="20" y="538" font-size="10.5" class="dim">2026-07-31 06:13Z  php 8.3         UP → WARN        180 d to EOL</text>
</svg>
```

`panel-light.svg` is the same emitter with one palette dict swapped
(`bg #ffffff`, `chrome #f6f8fa`, `border #d0d7de`, `text #1f2328`, `dim #656d76`,
`on #2da44e`, `spark #0969da`, `zebra #f6f8fa`).

## .github/workflows/panel.yml

```yaml
name: panel
on:
  schedule: [{cron: "13 3,9,15,21 * * *"}]   # off the hour on purpose; expect 1–4 h drift
  workflow_dispatch:
permissions: {contents: write}
concurrency: {group: panel, cancel-in-progress: false}
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install --no-cache-dir httpx pyyaml
      - name: probe                       # a DOWN target is data, not a failure;
        env:                              # only config/IO errors exit non-zero
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python tools/probe.py --config data/probes.yml
                                  --out data/history.jsonl --keep 730 --timeout 6
      - name: render
        run: python tools/render.py --history data/history.jsonl
                                   --dark panel-dark.svg --light panel-light.svg
                                   --text panel.txt --readme README.md
      - name: gate                        # a malformed SVG must never reach the profile
        run: |
          sudo apt-get -qq install -y libxml2-utils
          xmllint --noout panel-dark.svg panel-light.svg
          test "$(stat -c%s panel-dark.svg)" -gt 4000
      - name: commit
        run: |
          git config user.name  panel-bot
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git add panel-*.svg panel.txt data/history.jsonl README.md
          git diff --cached --quiet || git commit -m "panel: $(date -u +%FT%TZ) [skip ci]"
          git push
```

## render.py — the three rules that decide whether this survives

```python
_ESC = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;"}
def esc(s):                      # a single "&" in a GCP incident title voids the
    return "".join(_ESC.get(c, c) for c in str(s)  # WHOLE image, silently
                   if c == "\n" or 0x20 <= ord(c) < 0xFFFE)

def trunc(s, n):                 # never measure text; hard-cut, right-anchor numbers
    return s if len(s) <= n else s[: n - 1] + "…"

def spark(vals, x=460, y=8, w=140, h=18):
    lo, hi = min(vals), max(vals); span = (hi - lo) or 1
    step = w / max(len(vals) - 1, 1)
    return " ".join(f"{x + i * step:.0f},{y + h - (v - lo) / span * h:.0f}"
                    for i, v in enumerate(vals))
```
Plus: a probe whose fetch or parse raised renders as a grey OFF switch with the exception
class in the target column (`httpx.ConnectTimeout`) — never as a plausible number.
`--readme` rewrites only the block between `<!--PANEL:BEGIN-->` / `<!--PANEL:END-->`.

## Verify after the first push

```sh
curl -sSI https://raw.githubusercontent.com/lucianobosco/lucianobosco/main/panel-dark.svg \
  | grep -i content-type          # must be image/svg+xml, not text/plain
curl -sS https://github.com/lucianobosco | grep -c 'themed-picture'   # sanitiser kept it
```
Then check it with the OS in light mode and GitHub in dark (that mismatch is exactly why
this uses `<picture>` and not a media query inside the SVG), and on a phone at 390 px wide.
