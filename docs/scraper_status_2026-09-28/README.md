# Existing auction scraper status — 2026-09-28

Read-only audit; no scraper execution, network collection, schedule edits or changes to live data.

## Finding
Scheduled job com.cprt.job1 is loaded (launchctl: no active PID, last exit 0); configuration runs daily at 18:45 local. Latest log records successful Copart and IAA script exits September28. Exit success does not establish complete/fresh data.

SQLite read-only lot_snapshots aggregation: 2,882,058 repeated snapshot rows across20 dates, September8–28 (September9 missing). This is not2.88m unique vehicles and not a month of completed sales. Latest snapshot has147,608 rows,147,581 distinct lot IDs; paired daily file reports143,452 US listings. These are listed sitemap inventory, not sold units.

Schema contains snapshot time, lot ID, title label, year, make_model slug, state, yard, lastmod, URL. No current bid, accepted bid, final price, ACV, damage severity or seller fields. All SQLite table schemas searched for bid/price; no price-bearing table found. Original archive BUILD_SPEC listed desired current_bid/buy_it_now fields, but implemented scripts/job1_snapshot.py does not collect them. sale_events_live is yard-level scheduled auction events, not vehicle-level completed transactions. No price trajectory can be calculated from this collection.

Quality: latest log flags Copart stale fetch, median entry ages4/4/7 days and no page rebuilt in>3days. September28 IAA third vehicle sitemap challenged;89,999 rows partial, comparison share NULL. duopoly_daily has4/16 rows flagged usable under existing gates, which still do not establish sold-unit or market share comparability. September28 Copart overlap0.02% does not cure stale pages. Arrivals/departures may reflect publication changes, not sold/newly assigned vehicles.

Storage: SQLite replaces same-day snapshots subject to quality checks while CSV appends runs; SQLite is preferable for retained snapshot analysis. Neither fixes semantic absence of bids.

## Next price-data gate
Do not extend sitemap analysis into an ASP proxy. First confirm a small set of accessible lot records contains accepted/final sale results rather than live high bid, reserve or buy-now asking price, together with timestamps/outcome status. Historical month comparison needs corresponding historical records; starting a new collection cannot backfill them. Prior auction_recovery_pilot and repair_salvage_execution EVIDENCE document failed final-price/provider schema leads; check these before any further collection. Obtain approval before substantial collection. Any usable future price comparison needs stable geography, age/model, damage/title/running condition and auction outcome coverage; never treat listing disappearance as sale confirmation.

Reproduction: inspect scripts/job1_snapshot.py schema/CSV loop, scripts/com.cprt.job1.plist, logs/job1_cron.log tail; read-only data/cprt.db SQL: SELECT substr(snapshot_utc,1,10),count(*),count(DISTINCT lot_id) FROM lot_snapshots GROUP BY1 ORDER BY1 (use spaces GROUP BY 1 ORDER BY 1). Paired flags from data/csv/duopoly_daily.csv. Live files may change after this audit.
