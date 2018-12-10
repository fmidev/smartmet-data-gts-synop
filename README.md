# SmartMet Data Ingestion Module for GTS SYNOP data

Reads GTS WMO FM-12 SYNOP and GTS WMO BURF SYNOP files and converts those for SmartMet.

After installing this package. Configure message switch server to send files as follows:

## GTS WMO FM-12 SYNOP:
**WMO-heading:** SM/// SI/// SN///

**Directory:** /smartmet/data/incoming/gts/synop

## GTS WMO BUFR SYNOP:
**WMO-heading:** IS///

**Directory:** /smartmet/data/incoming/gts/synop-bufr
