# SmartMet GTS SYNOP ingestion module

Reads incoming GTS WMO FM-12 (text) and BUFR SYNOP files and converts
them to SmartMet querydata (`.sqd`) for both the data server and the
editor.

## Install

```sh
yum install smartmet-data-gts-synop
```

The package installs two scripts under `/smartmet/run/data/synop/bin/` and
registers them in cron (FM-12 every 10 min, BUFR every 20 min). An hourly
cleaner keeps the two most recent outputs and prunes incoming files older
than 7 days.

## Configure the message switch

Route incoming GTS bulletins to the directories below based on WMO heading:

| Format             | WMO heading        | Drop files in                             |
|--------------------|--------------------|-------------------------------------------|
| GTS WMO FM-12 SYNOP | `SM///` `SI///` `SN///` | `/smartmet/data/incoming/gts/synop`      |
| GTS WMO BUFR SYNOP  | `IS///`            | `/smartmet/data/incoming/gts/synop-bufr` |

## Output

Converted querydata is written to `/smartmet/data/gts/<type>/world/querydata/`
(`synop`, `ship`, `buoy`, `synop-bufr`) and a bzip2 copy is delivered to
`/smartmet/editor/in/` for the editor. Run logs go to
`/smartmet/logs/data/synop-gts.log` and `synop-bufr-gts.log`.

## Requires

`smartmet-qdtools` (provides `synop2qd` and `bufrtoqd`), `bzip2`, `wget`.
