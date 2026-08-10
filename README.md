<!-- design: terminal -->

## Luciano Bosco — Software Engineer, 14+ years, Málaga

Databases, data pipelines and the platforms behind video and stock content — and lately,
agents with MCP servers pointed at all of it. I also build small tools that remove daily
friction, which is what the session below is about.

<picture>
  <img src="terminal.svg" width="100%" alt="A terminal session: 4.1 billion rows queried in BigQuery, a Temporal workflow surviving its third attempt, three read-only MCP servers, then a production database a laptop cannot reach and the tunnel that fixes it.">
</picture>

<details>
<summary>The session as text</summary>

```console
luciano@mlg ~ $ whoami
luciano  -  Software Engineer, 14+ years  -  Malaga, ES
# backends. video and stock platforms: a few hundred thousand new assets a day.

luciano@mlg ~ $ bq query --nouse_legacy_sql 'SELECT count(*) FROM events.plays'
4113920684        -- 4.1 B rows, 41 GB scanned, 2.3 s
# writing that query is nothing. making it scan 41 GB instead of 4 TB is the job.

luciano@mlg ~ $ ingest-stats --today
  assets ingested   412 097        p99 end-to-end   41 s
# throughput you can buy. the p99 is the part you get paid for.

luciano@mlg ~ $ temporal workflow show -w ingest-2f9a --fields long
  3  ActivityTaskFailed      transcode   attempt 2   RetryState: InProgress
  7  ActivityTaskCompleted   transcode   attempt 3   14m22s
# a pipeline is not code that works. it is code that survives attempt 3.

luciano@mlg ~ $ claude mcp list
  databases    ready    read-only, 4 tools
  kubernetes   ready    read-only, 11 tools
  metrics      ready    read-only, 3 tools
# 2026: the agents get read-only credentials and one skill per runbook.
# it turns out the hard part was never the model. it was the plumbing.

luciano@mlg ~ $ mysql -h 10.24.6.11 -P 3306 -u readonly catalog
ERROR 2003 (HY000): Can't connect to MySQL server on '10.24.6.11:3306' (110)
# nothing at work is reachable from a laptop. that is the point.
luciano@mlg ~ $ tunnels-manager &
[gtk4] tunnels-manager 0.1.0  -  8 tunnels in ~/.config/tunnels-manager/
  catalog-db-prod       iap    13306   [ ==O ]
  videos-db-replica     iap    13307   [ O== ]
  -> clipboard: mysql://readonly@127.0.0.1:13306/catalog
# a weekend tool, because doing that by hand 9 times a day was absurd.

luciano@mlg ~ $ mysql -h 127.0.0.1 -P 13306 -u readonly catalog
luciano@mlg ~ $ SELECT * FROM luciano.repos WHERE visibility = 'private';
ERROR 1142 (42000): SELECT command denied to user 'visitor'@'github'
-- 4 public repos. the other 14 years are on the other side of that error.

luciano@mlg ~ $
```

The hostname and the table rows are invented; the constraint is not.

</details>

### What I work with

**Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![Laravel](https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**Data**

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=googlebigquery&logoColor=white)

**Platform**

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white) ![Temporal](https://img.shields.io/badge/Temporal-000000?style=for-the-badge&logo=temporal&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge)

**Agents**

![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white) ![MCP servers](https://img.shields.io/badge/MCP_servers-1F2937?style=for-the-badge&logo=modelcontextprotocol&logoColor=white) ![agent skills](https://img.shields.io/badge/agent_skills-1F2937?style=for-the-badge)

### Where to find me

The long version of those 14 years — the roles, the products, the things I cannot put in a
public repo — is on LinkedIn. That is also the fastest way to reach me.

<a href="https://www.linkedin.com/in/luciano-bosco/">
  <img src="https://img.shields.io/badge/Luciano_Bosco_on_LinkedIn-0A66C2?style=for-the-badge" height="34" alt="Luciano Bosco on LinkedIn">
</a>

### The one thing that is public

The app in the session above is **[tunnels-manager](https://github.com/lucianobosco/tunnels-manager)**:
Google Cloud IAP tunnels and port-forwards, one switch per tunnel, the connection string a
click away. GTK4 and Python, 100% branch coverage of the logic, and it is pinned below.

Everything else I work on is on the other side of that `ERROR 1142`.

---

<sub>The terminal above is not a recording. It is a 40-line text file rendered into an
animated SVG by 200 lines of standard-library Python — no service, no dependency, nothing
to rate limit. Three more designs, and the research behind them, live in
<a href="designs/"><code>designs/</code></a>.</sub>
