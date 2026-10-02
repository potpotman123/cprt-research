#!/usr/bin/env python3
"""Build model/CPRT_Model_v2.xlsx from the owner's skeleton (~/Downloads/CPRT_Model_v1.xlsx) plus repository data.
Steps are modules in scripts/cprt_model/; each adds tabs. The skeleton's DCF, Reverse DCF and PitchBook tabs are untouched."""
import sys, pathlib, importlib, openpyxl
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cprt_model.common import *
SRC = pathlib.Path('/Users/kwu/Downloads/CPRT_Model_v1.xlsx'); OUT = ROOT / 'model/CPRT_Model_v2.xlsx'
STEPS = ['data_tabs', 'facts', 'e1_fleet', 'e2_claims', 'e3_carriers', 'e4_aftermarket', 'e5_fees', 'e6_branches', 'coverage', 'scenarios', 'rpm', 'street', 'key_drivers', 'sources', 'checks']
def cover(wb):
    ws = wb.create_sheet('Cover', 0); tab_color(ws, NAVY); setup(ws, label_w=44, ncols=6, notes_col='H')
    title(ws, 'Copart, Inc. (NASDAQ: CPRT) — revenue architecture, DCF and reverse DCF', 'Fiscal year ends 31 July. $ millions unless stated. Built by scripts/build_cprt_model.py from the repository data; see docs/workbook_plan_2026-10-01.')
    section(ws, 4, 'Colour and label legend')
    for r, (k, t) in enumerate([('input', 'Blue: typed input (every one carries a label and a source in the Notes column)'), ('formula', 'Black: formula'), ('link', 'Green: link from another tab'), ('toggle', 'Red: toggle, probability or scenario selector'), ('engine', 'Purple: value pasted from the Python engine (file, date and hash on D Engine)'), ('note', 'Grey italic: notes and sources')], start=5):
        put(ws, f'B{r}', t, k)
    put(ws, 'B12', 'Evidence labels: VERIFIED (filing or page on disk) · MEASURED (computed from verified data by a committed script) · FITTED · CALIBRATED · ASSUMED · UNVERIFIED (recalled or second-hand) · ENGINE', 'note')
    section(ws, 14, 'Tab map')
    tabs = [('RPM', 'One page: revenue by channel, units, RPU, y/y, delta to Street, scenario selector'), ('DCF / Reverse DCF', "Owner's valuation (unchanged; reads RPM rows 6, 10, 12, 29)"),
            ('E1 Fleet / E1a', 'Vehicles on the road by age and body; claims-weighted mix checked against CCC 2020–2025'), ('E2 Claims & Totals', 'Claims × total-loss frequency by cell → total-loss pool by fiscal quarter'),
            ('E3 Carriers', 'Thesis A: carrier weights × Copart allocation paths; seller terms'), ('E4 Aftermarket', 'Thesis B: sourcing shift → repair saving → units; recycled displacement → bids → prices'),
            ('E5 Prices & Fees', 'ASP path, posted fee grid, buyer mix, seller fee, services → all-in RPU; historical ledger'), ('E6 Other Branches', 'Non-insurance, international, purchased vehicles, ACV gate'),
            ('Scenarios', 'Neither / A only / B only / Both / Bull offset, assembled live; engine 16-subset table for parity'), ('Street', 'Named-broker FY27 assumptions; not-disclosed preserved'), ('Checks', 'Ties to 8-Ks, identities, engine parity, no typed numbers outside Inputs blocks'),
            ('D …', 'Data tabs: values only, with source and date'), ('PB …', 'PitchBook statements (owner\'s original download)')]
    for r, (t, d) in enumerate(tabs, start=15): put(ws, f'B{r}', t, 'label', b=True); put(ws, f'D{r}', d, 'note')
    section(ws, 30, 'Dated benchmarks')
    for r, t in enumerate(['JPMorgan 11 Sep 2026: FY27 service revenue $4,061m (ex-ACV), purchased $721m, total $4,782m — VERIFIED, licensed report held locally', 'CapIQ 28 Sep 2026: FY27 total revenue $4,860.97m, acquisition perimeter unresolved — VERIFIED export', 'Engine reference (CCC family, 29 Sep): FY27 legacy service $4,093.08m; combined thesis case (1 Oct): $3,904.62m — ENGINE'], start=31): put(ws, f'B{r}', t, 'note')
def main():
    wb = openpyxl.load_workbook(SRC); ctx = {}
    cover(wb)
    for s in STEPS: importlib.import_module(f'cprt_model.{s}').build(wb, ctx)
    divider(wb, 'RPM ENGINES ----->', '7030A0'); divider(wb, 'DATA ----->', 'BFBFBF')
    order = ['Cover', 'RPM', 'DCF', 'Reverse DCF', 'RPM ENGINES ----->', 'E1 Fleet', 'E1a Fleet (roll)', 'E2 Claims & Totals', 'E3 Carriers', 'E4 Aftermarket', 'E5 Prices & Fees', 'E6 Other Branches', 'Key Drivers', 'Scenarios', 'Street', 'Sources', 'Checks', 'DATA ----->', 'D Reported', 'D Facts', 'D Barclays', 'D Coverage', 'D CCC', 'D Fleet', 'D Fees', 'D Carriers', 'D Engine', 'D Street']
    have = {ws.title: ws for ws in wb.worksheets}
    wb._sheets = [have[n] for n in order if n in have] + [ws for ws in wb.worksheets if ws.title not in order]
    for n in ('Volume Build', 'RPU Build'):
        if n in have: have[n].sheet_state = 'hidden'   # superseded by the engines; kept for reference until RPM is rewired
    for ws in wb.worksheets:
        if ws.title.startswith('PB '): ws.sheet_state = 'hidden'
    wb.active = 0; wb.save(OUT); print('saved', OUT, 'sheets', len(wb.worksheets))
if __name__ == '__main__': main()
