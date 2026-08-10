# KIND|delay_ms|text
# kinds: cmd out err say dim tbl flip wait gap
cmd|150|whoami
out|180|luciano  -  software engineer, 14+ years  -  Malaga, ES
say|140|# backends. the last years on the platforms behind video and stock content.
gap|90|
cmd|260|bq query --nouse_legacy_sql 'SELECT count(*) FROM events.plays'
out|650|4113920684        -- 4.1 B rows, 41 GB scanned, 2.3 s
say|150|# most of the job is making a number like that cheap to ask for.
gap|100|
cmd|280|temporal workflow show -w ingest-2f9a --fields long
out|400|  3  ActivityTaskFailed      transcode   attempt 2   RetryState: InProgress
out|300|  7  ActivityTaskCompleted   transcode   attempt 3   14m22s
say|150|# a pipeline is not code that works. it is code that survives attempt 3.
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
tbl|60|  videos-db-replica     iap    13307   [ O== ]
out|750|  -> clipboard: mysql://readonly@127.0.0.1:13306/catalog
say|200|# a weekend tool, because doing that by hand 9 times a day was absurd.
gap|100|
cmd|280|mysql -h 127.0.0.1 -P 13306 -u readonly catalog
cmd|350|{k}SELECT{/} * {k}FROM{/} luciano.repos {k}WHERE{/} visibility = 'private';
err|320|ERROR 1142 (42000): SELECT command denied to user 'visitor'@'github'
say|150|-- 4 public repos. the other 14 years are on the other side of that error.
gap|140|
cmd|350|open github.com/lucianobosco/tunnels-manager
