# CPRT data collection

## Install the daily job (run these in Terminal on the Mac, not in Cowork)

    cp ~/Documents/cprt/com.kendall.cprt-snapshot.plist ~/Library/LaunchAgents/
    launchctl load ~/Library/LaunchAgents/com.kendall.cprt-snapshot.plist

Runs at 06:15 daily and once immediately on load. Check it worked:

    tail -40 ~/Documents/cprt/logs/snapshot.log
    head -3 ~/Documents/cprt/data/lots.csv

To stop:

    launchctl unload ~/Library/LaunchAgents/com.kendall.cprt-snapshot.plist

## Run once by hand

    cd ~/Documents/cprt && python3 copart_snapshot.py --profile

## Why launchd and not cron

cron inside the Cowork VM is not writable and the VM does not persist,
so a cron job there would silently stop running. launchd on macOS proper
survives reboots. The data folder is a real Mac folder either way.

## What it collects

- data/lots.csv   one row per lot per snapshot, from lot.xml pages 1-3
                  (SEO subset, ~1,800 lots, ~89% clean-title -- NOT full inventory)
- data/sales.csv  one row per scheduled auction, from sale-list-results.xml
                  (~1,144 entries: yard_id, state, city, sale_date)

The sales.csv series is the valuable one: sale events per yard per week
is an operational throughput proxy that requires no gated data.

Neither file can be backfilled. Every day it does not run is gone.

## Constraints

robots.txt disallows /public/data/, /downloadSalesData, /memberFees,
/lotSearchResults/. This script touches none of them -- only URLs Copart
publishes in its own sitemap index. Keep it that way.
