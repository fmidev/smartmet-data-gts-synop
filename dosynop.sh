#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2017)
#
# SmartMet Data Ingestion Module for GTS SYNOP Observations
#

if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME
fi

IN=$BASE/data/incoming/gts/synop
OUT=$BASE/data/gts
EDITOR=$BASE/editor/in
TMP=$BASE/tmp/data/synop
TIMESTAMP=`date +%Y%m%d%H%M`
LOGFILE=$BASE/logs/data/synop-gts.log

SYNOPFILE=$TMP/${TIMESTAMP}_gts_world_synop.sqd
SHIPFILE=$TMP/${TIMESTAMP}_gts_world_ship.sqd
BUOYFILE=$TMP/${TIMESTAMP}_gts_world_buoy.sqd

mkdir -p $TMP
mkdir -p $OUT/{synop,ship,buoy}/world/querydata

# Use log file if not run interactively
if [ $TERM = "dumb" ]; then
    exec &> $LOGFILE
fi

echo "URL: $URL"
echo "IN:  $IN" 
echo "OUT: $OUT" 
echo "TMP: $TMP" 
echo "SYNOP File: $SYNOPFILE"
echo "SHIP  File: $SHIPFILE"
echo "BUOY  File: $BUOYFILE"

# Do SYNOP stations
synop2qd "$IN/*" > $SYNOPFILE

# Do SHIP SYNOP stations
synop2qd -S -p 1002,SHIP "$IN/*" > $SHIPFILE

# Do SHIP SYNOP stations
synop2qd -B -p 1017,BUOY "$IN/*" > $BUOYFILE


if [ -s $SYNOPFILE ]; then
    bzip2 -k $SYNOPFILE
    mv -f $SYNOPFILE $OUT/synop/world/querydata/
    mv -f ${SYNOPFILE}.bz2 $EDITOR
fi

if [ -s $SHIPFILE ]; then
    bzip2 -k $SHIPFILE
    mv -f $SHIPFILE $OUT/ship/world/querydata/
    mv -f ${SHIPFILE}.bz2 $EDITOR
fi

if [ -s $BUOYFILE ]; then
    bzip2 -k $BUOYFILE
    mv -f $BUOYFILE $OUT/buoy/world/querydata/
    mv -f ${BUOYFILE}.bz2 $EDITOR
fi

rm -f $TMP/*.sqd*
