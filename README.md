<!-- design: terminal -->

### Luciano Bosco — software engineer, 14+ years, Málaga

Databases, data pipelines and the platforms behind video and stock content — and lately,
agents with MCP servers pointed at all of it. I also build small tools that remove daily
friction, which is what the session below is about.

<a href="https://github.com/lucianobosco/tunnels-manager">
  <img src="terminal.svg" width="787" alt="A terminal session: a production database connection times out, tunnels-manager opens the tunnel, and the same command connects.">
</a>

**[tunnels-manager](https://github.com/lucianobosco/tunnels-manager)** — the app in that
session. Google Cloud IAP tunnels and port-forwards with a switch per tunnel and the
connection string one click away. GTK4, Python, 100% branch coverage of the logic.

<details>
<summary>The session as text</summary>

```console
luciano@mlg ~ $ whoami
luciano  -  software engineer, 14+ years  -  Malaga, ES
# backends. the last years on the platforms behind video and stock content.

luciano@mlg ~ $ bq query --nouse_legacy_sql 'SELECT count(*) FROM events.plays'
4113920684        -- 4.1 B rows, 41 GB scanned, 2.3 s
# most of the job is making a number like that cheap to ask for.

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
-- 4 public repos. the other 14 years ship under NDA. that is the tell.

luciano@mlg ~ $ open github.com/lucianobosco/tunnels-manager
```

The hostname and the table rows are invented; the constraint is not.

</details>

`Python` · `PHP / Laravel` · `JavaScript` · `MySQL` · `BigQuery` · `Google Cloud` ·
`Kubernetes` · `Temporal` · `AWS` · `Claude Code` · `MCP servers` · `agent skills`

[LinkedIn](https://www.linkedin.com/in/luciano-bosco/) · the image above is generated from
a 40-line text file, see [`designs/`](designs/)
