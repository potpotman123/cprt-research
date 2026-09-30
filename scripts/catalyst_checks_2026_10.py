#!/usr/bin/env python3
"""Offline checks for the 30 September expectations/catalyst review.

No fetching, model fitting or source changes. Public filings remain in raw/;
only derived facts, source fingerprints and limited analytical inputs are saved.
Run from any directory: python3 scripts/catalyst_checks_2026_10.py
"""
from pathlib import Path
from html.parser import HTMLParser
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/catalyst_evidence_2026-10"


class Plain(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def plain(path):
    h = Plain()
    h.feed(path.read_text())
    return re.sub(r"\s+", " ", " ".join(h.parts))


def main():
    OUT.mkdir(exist_ok=True, parents=True)
    inventory = ROOT / "data/csv/duopoly_daily.csv"
    rows = [r for r in csv.DictReader(inventory.open()) if r["usable"] == "1"]
    values = []
    for r in rows:
        share = 100 * int(r["copart_us_lots"]) / (int(r["copart_us_lots"]) + int(r["iaa_vehicles"]))
        assert abs(share - float(r["copart_share_pct"])) <= 0.0051
        values.append({"day": r["day"], "copart_share_pct_recomputed": share,
                       "copart_snapshot": r["copart_snapshot"]})
    shares = [r["copart_share_pct_recomputed"] for r in values]

    cp25 = ROOT / "raw/sec/10k/cprt_2025-07-31.htm"
    cp26 = ROOT / "raw/sec/10k/cprt_2026-07-31.htm"
    rba = ROOT / "raw/sec/rba/10k_2025-12-31.htm"
    rbaq = ROOT / "raw/sec/rba/8k_2026-08-04_ex99_1.htm"
    t25, t26, trba, tq = map(plain, (cp25, cp26, rba, rbaq))
    assert "non-exclusive" not in t25 and "non-exclusive" in t26
    assert "79%, 81%, and 81%" in t26
    assert "286 total operating facilities" in t26
    assert "281 total operating facilities" in t25
    def competition(t):
        a = t.index("We face significant competition from other remarketers")
        b = t.index("privately-held independent remarketers.", a)
        return t[a:b + len("privately-held independent remarketers.")]
    assert competition(t25) == competition(t26)
    assert "Automotive 2,447.7 2,297.2" in trba
    assert "Automotive 658.8 595.9" in tq
    assert "Total 333 6,143 8,660" in trba

    carrier_path = ROOT / "docs/carrier_test_2026-09-28/forward_comparison.csv"
    carrier = list(csv.DictReader(carrier_path.open()))
    by_key = {(r["quarter"], r["case"]): r for r in carrier}
    runoff_delta = {}
    for q in ("FY27Q1", "FY27Q2", "FY27Q3", "FY27Q4"):
        a = float(by_key[q, "PGR runoff only; fixed carrier mix"]["insurance_revenue_musd"])
        b = float(by_key[q, "Freeze all at FY26Q4"]["insurance_revenue_musd"])
        runoff_delta[q] = a - b

    # Analyst inputs below are transcribed from Stephens 20-Aug PDF pp9-10,
    # checked against the native PDF page; unit/RPU labels are all US fee units.
    us_service = [863.9, 852.6, 931.6, 845.4]
    intl_service = [154.4, 151.7, 178.8, 172.1]
    service = [1018.4, 1004.3, 1110.4, 1017.5]
    total = [1184.5, 1177.0, 1294.7, 1190.5]
    purchased = [166.1, 172.7, 184.3, 173.0]
    assert abs(sum(service) - 4150.6) < 1e-6
    for i in range(4):
        assert abs(service[i] - us_service[i] - intl_service[i]) <= 0.11
        assert abs(total[i] - service[i] - purchased[i]) <= 0.11
    # Hypothetical miss of a named driver, not a forecast: Q2 US fee units
    # flat rather than +2%, retaining the analyst's RPU and all other branches.
    q2_delta = us_service[1] * (1 / 1.02 - 1)
    out = {
        "as_of": "2026-09-30", "status": "MEASURED arithmetic; forecast shocks remain ASSUMED",
        "inventory": {"observations": values, "n": len(values),
                      "mean_pct": sum(shares) / len(shares), "min_pct": min(shares),
                      "max_pct": max(shares), "denominator": "listed US inventory of two platforms; stock, not flow"},
        "rba_owned_acreage_pct": 100 * 6143 / (6143 + 8660),
        "rba_us_owned_acreage_pct": 100 * 4431 / (4431 + 7769),
        "rba_2025_automotive_lots_thousands": 2447.7,
        "rba_2025_quarter_sum_thousands": 625.6 + 595.9 + 601.7 + 624.5,
        "stephens_iaa_lots_difference_thousands": 2516 - 2447.7,
        "rba_q2_2026_automotive_lot_growth_pct": 100 * (658.8 / 595.9 - 1),
        "carrier_runoff_minus_flat_musd": runoff_delta,
        "carrier_runoff_minus_flat_H1_musd": runoff_delta["FY27Q1"] + runoff_delta["FY27Q2"],
        "carrier_runoff_minus_flat_FY_musd": sum(runoff_delta.values()),
        "stephens_Q2_flat_units_hypothetical": {
            "us_service_delta_musd": q2_delta,
            "global_service_after_musd": service[1] + q2_delta,
            "annual_service_if_other_quarters_unchanged_musd": 4150.6 + q2_delta,
            "annual_gap_to_JPM_4061_musd": 4150.6 + q2_delta - 4061,
            "limit": "One-quarter driver sensitivity to dated Stephens forecast; no evidence-supported shock or JPM quarterly comparison"},
        "stephens_minus_jpm_service_musd": 4150.6 - 4061,
        "jpm_service_growth_vs_reported_fy26_pct": 100 * (4061 / 3969.520 - 1),
        "stephens_sums": {"service": sum(service), "purchased": sum(purchased), "total": sum(total)},
        "checks": {"inventory_rounding": True, "new_contract_sentence": True,
                   "competition_body_identical": True, "facilities_and_insurer_mix": True,
                   "rba_source_values": True, "stephens_quarter_sums": True}
    }
    (OUT / "checks.json").write_text(json.dumps(out, indent=2) + "\n")
    paths = [inventory, cp25, cp26, rba, rbaq, carrier_path,
             ROOT / "raw/sec/rba/10q_2026-06-30.htm",
             ROOT / "raw/transcripts/call_2026-09-10.txt"]
    paths += sorted((ROOT / "raw/sec/rba").glob("8k_2026*.htm"))
    source_dir = Path("/Users/kwu/Documents/ChatGPT/HFAC x Citadel/research/cprt_discovery_plan_2026-09-26/sources")
    for tag in ("124345098", "123970131", "124339246", "124041014"):
        paths += list(source_dir.glob("*" + tag + ".txt"))
        paths += list(source_dir.glob("*" + tag + ".pdf"))
    paths += list((ROOT / "raw/catalyst_2026_10").glob("*.html"))
    manifest = []
    for p in dict.fromkeys(paths):
        manifest.append({"path": str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),
                         "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size})
    (OUT / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for source, target in (("query_manifest.json", "search_results.json"), ("page_manifest.json", "page_access.json")):
        p = ROOT / "raw/catalyst_2026_10" / source
        rows = json.loads(p.read_text())
        if source == "query_manifest.json":
            for r in rows:
                # Preserve search metadata and URLs, not third-party snippet prose.
                r["result_urls"] = [x["url"] for x in r.pop("results") if x["type"] == "result__a"]
                if not (ROOT / r["path"]).exists():
                    r["path"] = None
        (OUT / target).write_text(json.dumps(rows, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
