# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A small SmartMet data ingestion module distributed as a `noarch` RPM. It does not build any binaries — it only installs two shell scripts and cron entries onto a SmartMet server. The actual conversion work is done by external tools (`synop2qd`, `bufrtoqd`) that come from `smartmet-qdtools`.

There is no compilation, no test suite, and no `Makefile`. All "development" is editing shell scripts and the `.spec` file, then bumping the version and building an RPM.

## Layout

- `dosynop.sh` — converts text-format GTS WMO FM-12 SYNOP files (also extracts SHIP and BUOY subsets) via `synop2qd`. Driven by cron every 10 min.
- `dosynop-bufr.sh` — converts BUFR-format GTS SYNOP files via `bufrtoqd` (requires `BUFR_TABLES=/usr/share/libecbufr`). Driven by cron every 20 min. SHIP/BUOY branches are present but commented out.
- `smartmet-data-gts-synop.spec` — RPM packaging. Creates the `/smartmet/...` directory tree, writes the cron file (`cnf/cron/cron.d/synop-gts.cron`) and the hourly cleaner (`cnf/cron/cron.hourly/clean_data_gts_synop`), and installs the two scripts to `/smartmet/run/data/synop/bin/`.

## Runtime pipeline (what the scripts actually do)

Both scripts share the same shape:

1. `BASE=/smartmet` if present, else `$HOME` (so the scripts can be run by a developer locally without root).
2. Read raw GTS files from `$BASE/data/incoming/gts/synop` (text) or `…/synop-bufr` (BUFR). The message-switch server is expected to drop files there based on WMO heading (`SM/SI/SN///` → text, `IS///` → BUFR — see README).
3. Convert to SmartMet querydata (`.sqd`) in `$BASE/tmp/data/synop`, timestamped `YYYYMMDDHHMM_gts_world_*.sqd`.
4. If the output is non-empty: bzip2-copy it, move the `.sqd` to `$BASE/data/gts/{synop,ship,buoy,synop-bufr}/world/querydata/`, and move the `.bz2` to `$BASE/editor/in` (this is what feeds the editor).
5. Clear `$TMP/*.sqd*`.

When `$TERM = dumb` (i.e. invoked by cron) both scripts redirect all output to `$BASE/logs/data/synop-gts.log` or `…/synop-bufr-gts.log`.

The hourly cleaner installed by the spec keeps only the 2 most-recent `.sqd` files in each output dir and deletes incoming raw files older than 7 days.

## Editing rules specific to this repo

- **Version bump = touch `Version:` and add a `%changelog` entry.** Version format is `YY.MM.DD` (e.g. `25.10.13`). The spec must end with a `%changelog` entry whose date matches; otherwise `rpmbuild` complains.
- **Don't `git push` straight to master.** Recent commits are direct-to-master but the FMI convention is PR-based; ask before pushing.
- **Don't change the `$IN` / `$OUT` / `$EDITOR` paths casually.** They match the directory tree the `.spec` creates and the FMI message-switch configuration documented in the README. If you change a path in a script, mirror it in the spec's `mkdir -p` lines and the cleaner block.
- **The two scripts diverge intentionally.** `dosynop.sh` calls `synop2qd` (3 invocations: land/SHIP/BUOY), `dosynop-bufr.sh` calls `bufrtoqd` once for land only. Don't "unify" them without a reason — the BUFR SHIP/BUOY branches are commented out because the upstream tool path for those isn't wired up yet.

## Building the RPM (FMI infrastructure)

The spec assumes FMI's `smartbuildcfg` / `rpmbuild` topology: sources are expected under `%_topdir/SOURCES/smartmet-data-gts-synop/`. There is no `Makefile` target — packaging is done in FMI's CI. Locally you would run something like:

```sh
rpmbuild -ba smartmet-data-gts-synop.spec
```

after staging the scripts under `~/rpmbuild/SOURCES/smartmet-data-gts-synop/`. End users install via `yum install smartmet-data-gts-synop` from the FMI repo.

## macOS note

The parent workspace (`/Users/mrauhala/Code/smartmet/CLAUDE.md`) covers a macOS port of the broader SmartMet stack. **This package is not part of that port** — it is RHEL-only (RPM, `/smartmet` paths, FMI cron layout). Don't add `Makefile.mac` or `#ifdef __APPLE__` patches here; if the scripts need to run on macOS for ad-hoc testing they already fall back to `$HOME` automatically.
