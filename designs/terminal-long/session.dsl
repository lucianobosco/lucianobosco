cmd|300|whoami
out|300|luciano  -  software engineer, 14 years.  Malaga, ES.
dim|60|databases | data pipelines | the platforms behind video and stock content
gap|150|
cmd|350|mysql -h 10.24.6.11 -P 3306 -u readonly catalog
wait|1600|
err|0|ERROR 2003 (HY000): Can't connect to MySQL server on '10.24.6.11' (110 timed out)
cmd|450|ss -ltnp | grep 13306
dim|250|# nothing is listening. nothing at work is reachable from a laptop, ever.
gap|150|
cmd|350|tunnels-manager &
out|450|[gtk4] tunnels-manager 0.1.0  -  8 tunnels from ~/.config/tunnels-manager/tunnels.yaml
dim|100|  +--------------------------+----------+--------+-----------+
dim|40|  | TUNNEL                   | KIND     | LOCAL  |           |
dim|40|  +--------------------------+----------+--------+-----------+
flip|40|  | catalog-db-prod          | iap      | 13306  |  [ O== ]  |%%  | catalog-db-prod          | iap      | 13306  |  [ ==O ]  |
dim|40|  | videos-db-replica        | iap      | 13307  |  [ O== ]  |
dim|40|  +--------------------------+----------+--------+-----------+
out|900|  -> clipboard: mysql://readonly@127.0.0.1:13306/catalog
cmd|500|ss -ltnp | grep 13306
out|300|LISTEN 0 128 127.0.0.1:13306 0.0.0.0:* users:(("tunnels-manager",pid=41207))
gap|150|
cmd|350|mysql -h 127.0.0.1 -P 13306 -u readonly catalog
cmd|500|{k}SELECT{/} * {k}FROM{/} luciano.stack {k}ORDER BY{/} years {k}DESC{/};
dim|400|+------------+-----------------------------------------------+-------+
dim|40|| layer      | tools                                         | years |
dim|40|+------------+-----------------------------------------------+-------+
out|40|| databases  | MySQL, BigQuery, query plans at 03:00         |    14 |
out|40|| services   | Python, PHP/Laravel, some Vue                  |    12 |
out|40|| platform   | Google Cloud, Kubernetes, a little AWS        |     8 |
out|40|| pipelines  | Temporal, batch that has to survive a retry   |     6 |
out|40|| agents     | Claude Code, MCP servers, a skill per runbook  |     2 |
dim|40|+------------+-----------------------------------------------+-------+
dim|400|5 rows in set (0.01 sec)
cmd|600|{k}SELECT{/} * {k}FROM{/} luciano.repos {k}WHERE{/} visibility = 'private';
err|500|ERROR 1142 (42000): SELECT command denied to user 'visitor'@'github'
dim|150|-- 4 public repos. the other 14 years are on the other side of that error.
gap|200|
cmd|350|kubectl -n platform get pods -l app=ingest --watch
out|500|ingest-worker-4b8qz   0/1   Pending   0   0s
out|1200|ingest-worker-4b8qz   1/1   Running   0   6s
dim|250|# the whole job is making that line boring. it has been boring for years.
cmd|500|open github.com/lucianobosco/tunnels-manager
