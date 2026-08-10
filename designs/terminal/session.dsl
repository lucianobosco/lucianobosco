# KIND|delay_ms|text
# kinds: cmd out err say dim tbl flip wait gap
#   cmd  typed per character, preceded by the prompt
#   out  program output, bright
#   err  program output, red
#   say  his voice (comments); brightest non-command text
#   dim  chrome / low-priority output
#   tbl  a row of a table: contiguous tbl+flip rows must all be the same length
#   flip contains exactly one {sw:OFF|ON} marker, len(OFF) == len(ON)
#   wait burns time without emitting a row
#   gap  an empty row
cmd|150|whoami
out|180|luciano  -  software engineer, 14 years  -  Malaga, ES
gap|80|
cmd|220|mysql -h 10.24.6.11 -P 3306 -u readonly catalog
wait|600|
err|0|ERROR 2003 (HY000): Can't connect to MySQL server on '10.24.6.11:3306' (110)
cmd|300|ss -ltnp | grep 13306
say|180|# nothing at work is reachable from a laptop. that is the point.
gap|100|
cmd|250|tunnels-manager &
out|280|[gtk4] tunnels-manager 0.1.0  -  8 tunnels in ~/.config/tunnels-manager/
flip|100|  catalog-db-prod       iap    13306   [ {sw:O==|==O} ]
tbl|60|  videos-db-replica     iap    13307   [ O== ]
out|850|  -> clipboard: mysql://readonly@127.0.0.1:13306/catalog
cmd|320|ss -ltnp | grep 13306
out|220|LISTEN 0 128 127.0.0.1:13306 0.0.0.0:* users:(("tunnels-manager",pid=41207,fd=11))
gap|100|
cmd|250|mysql -h 127.0.0.1 -P 13306 -u readonly catalog
cmd|350|{k}SELECT{/} * {k}FROM{/} luciano.repos {k}WHERE{/} visibility = 'private';
err|320|ERROR 1142 (42000): SELECT command denied to user 'visitor'@'github'
say|150|-- 4 public repos. the other 14 years ship under NDA. that is the tell.
gap|140|
cmd|250|kubectl -n platform get pods -l app=ingest --watch
out|350|ingest-worker-4b8qz   0/1   Pending   0     0s
out|800|ingest-worker-4b8qz   1/1   Running   0     6s
say|180|# the whole job is making that line boring. it has been for years.
gap|140|
cmd|350|open github.com/lucianobosco/tunnels-manager
