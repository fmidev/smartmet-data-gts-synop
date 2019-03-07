#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2018-)
#
# SmartMet Data Ingestion Module for GTS SYNOP Observations
#
export BUFR_TABLES=/usr/share/libecbufr
if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME
fi

IN=$BASE/data/incoming/gts/synop-bufr
OUT=$BASE/data/gts
EDITOR=$BASE/editor/in
TMP=$BASE/tmp/data/synop
TIMESTAMP=`date +%Y%m%d%H%M`
LOGFILE=$BASE/logs/data/synop-bufr-gts.log

SYNOPFILE=$TMP/${TIMESTAMP}_gts_world_synop_bufr.sqd
SHIPFILE=$TMP/${TIMESTAMP}_gts_world_ship_bufr.sqd
BUOYFILE=$TMP/${TIMESTAMP}_gts_world_buoy_bufr.sqd

mkdir -p $TMP
mkdir -p $OUT/{synop-bufr,ship-bufr,buoy-bufr}/world/querydata

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
bufrtoqd -a -C land $IN/ $SYNOPFILE

# Do SHIP SYNOP stations
#synop2qd -S -t -p 1002,SHIP "$IN/*" > $SHIPFILE

# Do SHIP SYNOP stations
#synop2qd -B -t -p 1017,BUOY "$IN/*" > $BUOYFILE


if [ -s $SYNOPFILE ]; then
    bzip2 -k $SYNOPFILE
    mv -f $SYNOPFILE $OUT/synop-bufr/world/querydata/
    mv -f ${SYNOPFILE}.bz2 $EDITOR
fi

if [ -s $SHIPFILE ]; then
    bzip2 -k $SHIPFILE
    mv -f $SHIPFILE $OUT/ship-bufr/world/querydata/
    mv -f ${SHIPFILE}.bz2 $EDITOR
fi

if [ -s $BUOYFILE ]; then
    bzip2 -k $BUOYFILE
    mv -f $BUOYFILE $OUT/buoy-bufr/world/querydata/
    mv -f ${BUOYFILE}.bz2 $EDITOR
fi

rm -f $TMP/*.sqd*
