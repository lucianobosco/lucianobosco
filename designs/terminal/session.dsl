# KIND|delay_ms|text
# kinds: cmd out err say dim tbl flip wait gap
cmd|150|whoami
out|180|luciano  -  Software Engineer, 14+ years building backends  -  Malaga, ES
say|140|# video and stock platforms. a few hundred thousand new assets a day.
gap|90|
cmd|260|bq query --nouse_legacy_sql 'SELECT count(*) FROM events.plays'
out|650|4113920684        -- 4.1 B rows, 41 GB scanned, 2.3 s
say|150|# writing that query is nothing. making it scan 41 GB instead of 4 TB is the job.
gap|100|
cmd|250|ingest-stats --today
out|320|  assets ingested   412 097        p99 end-to-end   41 s
say|170|# throughput you can buy. the p99 is the part you get paid for.
gap|100|
cmd|280|temporal workflow show -w ingest-2f9a --fields long
out|400|  3  ActivityTaskFailed      transcode   attempt 2   RetryState: InProgress
out|300|  7  ActivityTaskCompleted   transcode   attempt 3   14m22s
say|150|# a pipeline is not code that works. it is code that survives attempt 3.
gap|100|
cmd|300|curl -s traces/7c1e-ab3f | jq '.spans | length, .services | length'
out|340|94        12        -- 94 spans across 12 services, one upload
say|170|# microservices: the bug is never inside a service. it is between two of them.
gap|100|
cmd|280|claude mcp list
out|300|  databases    ready    read-only, 4 tools
out|60|  kubernetes   ready    read-only, 11 tools
out|60|  metrics      ready    read-only, 3 tools
say|180|# 2026: the agents get read-only credentials and one skill per runbook.
say|150|# it turns out the hard part was never the model. it was the plumbing.
gap|100|
cmd|300|mysql -h 10.24.6.11 -P 3306 -u readonly catalog
wait|600|
err|0|ERROR 2003 (HY000): Can't connect to MySQL server on '10.24.6.11:3306' (110)
say|180|# nothing at work is reachable from a laptop. that is the point.
cmd|250|tunnels-manager &
out|280|[gtk4] tunnels-manager 0.1.0  -  8 tunnels in ~/.config/tunnels-manager/
flip|100|  catalog-db-prod       iap    13306   [ {sw:O==|==O} ]
out|750|  -> clipboard: mysql://readonly@127.0.0.1:13306/catalog
say|200|# if I have to do a thing twice, I automate it. this one I did 9 times a day.
gap|100|
cmd|280|mysql -h 127.0.0.1 -P 13306 -u readonly catalog
cmd|350|{k}SELECT{/} * {k}FROM{/} luciano.repos {k}WHERE{/} visibility = 'private';
err|320|ERROR 1142 (42000): SELECT command denied to user 'visitor'@'github'
say|150|-- 4 public repos. the other 14 years are on the other side of that error.
gap|140|
cmd|300|tail -2 ~/notes/still-figuring-out.md
out|320|  - whether p99 can be sold as a feature and not just an SLO
out|60|  - what breaks first the day ingest doubles
say|900|# 14 years in, that list only gets longer. that is the part I like.
