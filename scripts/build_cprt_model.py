#!/usr/bin/env python3
"""Build model/CPRT_Model_v2.xlsx from the owner's skeleton (~/Downloads/CPRT_Model_v1.xlsx) plus repository data.
Steps are modules in scripts/cprt_model/; each adds tabs. The skeleton's DCF, Reverse DCF and PitchBook tabs are untouched."""
import sys, pathlib, importlib, openpyxl
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cprt_model.common import *
SRC = ROOT / 'model/CPRT_Model_v2.xlsx'; OUT = SRC   # 2 Oct: the build now takes the owner's current workbook as its base
BACKUP = ROOT / 'model/CPRT_Model_v2_prebuild.xlsx'
GENERATED = ['Cover', 'Key Drivers', 'Summary', 'E1 Fleet', 'E1a Fleet (roll)', 'E2 Claims & Totals', 'E3 Carriers', 'E4 Aftermarket', 'E5 Prices & Fees', 'E6 Other Branches', 'Scenarios', 'Street', 'Sources', 'Checks', 'D Reported', 'D Facts', 'D Barclays', 'D 10-K FY26', 'D Coverage', 'D CCC', 'D Fleet', 'D Fees', 'D Carriers', 'D Engine', 'RPM ENGINES ----->', 'DATA ----->', '3SM']
OWNER_EDITED = ['RPM', 'Reverse DCF', 'DCF']   # owner tabs the steps write specific cells into; never recreated
HIDE = ['Volume Build', 'RPU Build', 'PB IS (Annual)', 'PB BS (Annual)', 'PB CF (Annual)', 'PB IS (Qtr)', 'PB BS (Qtr)', 'PB CF (Qtr)']
STEPS = ['data_tabs', 'facts', 'e1_fleet', 'e2_claims', 'e3_carriers', 'e4_aftermarket', 'e5_fees', 'e6_branches', 'coverage', 'scenarios', 'rpm', 'street', 'key_drivers', 'd_barclays', 'd10k', 'wacc', 'sources', 'checks']
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
    import shutil
    shutil.copy(SRC, BACKUP)
    wb = openpyxl.load_workbook(SRC); ctx = {}
    before = list(wb.sheetnames); positions = {n: i for i, n in enumerate(before)}
    for n in GENERATED:
        if n in wb.sheetnames: wb.remove(wb[n])
    cover(wb)
    for s in STEPS: importlib.import_module(f'cprt_model.{s}').build(wb, ctx)
    if 'RPM ENGINES ----->' not in wb.sheetnames: divider(wb, 'RPM ENGINES ----->', '7030A0')
    if 'DATA ----->' not in wb.sheetnames: divider(wb, 'DATA ----->', 'BFBFBF')
    # order: owner's existing order for everything that existed; new generated tabs by default placement
    default_after = {'Summary': 'Key Drivers', '3SM': 'RPM', 'D Barclays': 'D Facts', 'D 10-K FY26': 'D Barclays'}
    order = [n for n in before if n in wb.sheetnames]
    for n in wb.sheetnames:
        if n in order: continue
        anchor = default_after.get(n); idx = order.index(anchor) + 1 if anchor in order else len(order); order.insert(idx, n)
    have = {ws.title: ws for ws in wb.worksheets}; wb._sheets = [have[n] for n in order]
    for n in HIDE:
        if n in have: have[n].sheet_state = 'hidden'
    wb.active = 0; wb.save(OUT); print('saved', OUT, 'sheets', len(wb.worksheets), '| order preserved from owner file; backup at', BACKUP.name)
if __name__ == '__main__': main()
