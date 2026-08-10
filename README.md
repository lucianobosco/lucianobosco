<!-- design: terminal -->

## Luciano Bosco — Software Engineer · 14+ years building backends · Málaga

Databases, data pipelines and the platforms behind video and stock content — and lately,
agents with MCP servers pointed at all of it. If I have to do something twice, I automate
it, so a good part of what I build is the tooling around the work rather than the work.

The long version of those years — the roles, the products, the things that cannot go in a
public repo — is on **[LinkedIn](https://www.linkedin.com/in/luciano-bosco/)**, which is also
the fastest way to reach me.

<picture>
  <img src="terminal.svg" width="100%" alt="A terminal session about the work: the scale of the data, a query that reads 41 GB instead of 4 TB, a pipeline that recovers on its own, one upload crossing twelve services, agents with read-only access to production, the tool that opens a tunnel to a database no laptop can reach, and the stack it all runs on. The full transcript is in the text block below.">
</picture>

<details>
<summary>Terminal session transcript (text)</summary>

```console
luciano@bosco $ whoami
luciano  -  software engineer  -  14+ years building backends
# I work on video and stock platforms: a few hundred thousand new files a day.

luciano@bosco $ count published_resources
  287,410,933 rows        41 GB read        2.3 s
# writing that query takes a minute. making it read 41 GB instead of 4 TB is the job.

luciano@bosco $ stats today
  files ingested   412,097        slowest 1%   41 s
# 400,000 files is the easy half. the slowest 1% is the half people notice.

luciano@bosco $ workflow ingest-2f9a
  transcode   attempt 1   failed
  transcode   attempt 3   done in 14m
# a pipeline is not code that works. it is code that recovers at 4am without me.

luciano@bosco $ trace upload-7c1e
  12 services        94 steps        1 uploaded file
# each of those twelve works on its own. the hard bugs live in between them.

luciano@bosco $ mcp list
  databases     read-only
  kubernetes    read-only
  metrics       read-only
# these are the doors an agent of mine can open. read-only: it can look, never touch.

luciano@bosco $ tunnels-manager &
  catalog-prod   iap tunnel   localhost:13306   [ ==O ]
# if I have to repeat something several times a day, I automate it.

luciano@bosco $ stack
  languages   python  php  laravel  vue  vuex  wordpress
  data        mysql  bigquery
  platform    microservices  dapr  kubernetes  google cloud  aws  temporal
  agents      claude code  mcp servers  skills per runbook
# 14 years in, and the questions got better, not fewer.
```

Those are pseudo-commands — the short version of the real ones — and every number is
invented. The constraints they describe are not.

</details>

### The one thing that is public

The app in the session is **[tunnels-manager](https://github.com/lucianobosco/tunnels-manager)**:
Google Cloud IAP tunnels and port-forwards, one switch per tunnel, the connection string a
click away. GTK4 and Python, 100% branch coverage of the logic, and it is pinned below.

Everything else I work on lives behind that tunnel.

---

<sub>The terminal above is not a recording. It is a 37-line text file rendered into an
animated SVG by 259 lines of standard-library Python — no service, no dependency, nothing
to rate limit. Three more designs, and the research behind them, live in
<a href="designs/"><code>designs/</code></a>.</sub>
