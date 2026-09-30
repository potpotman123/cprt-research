"""Inventory publication payload and explicitly excluded local research files."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREFIX = str(HERE.relative_to(ROOT)) + '/'

def git_names(*args):
    return [n for n in subprocess.check_output(['git', 'ls-files', '-z', *args], cwd=ROOT).decode().split('\0') if n]

def write_csv(name, rows, fields):
    with (HERE / name).open('w') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

files = []
counts = collections.Counter()
credential_flags = []
pattern = re.compile(rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}')
for name in git_names('--cached'):
    if name.startswith(PREFIX):
        continue
    path = ROOT / name
    data = path.read_bytes()
    category = path.relative_to(ROOT).parts[0] if '/' in name else 'root'
    counts[category] += 1
    assert len(data) < 100 * 1024 * 1024, name
    if pattern.search(data):
        credential_flags.append(name)
    # Match the bytes to be committed, not merely the working-tree filenames.
    staged = subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT)
    assert staged == data, 'Working tree differs from staged snapshot: ' + name
    files.append(dict(path=name, category=category, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
assert not credential_flags, 'Credential-pattern flags: ' + repr(credential_flags)

ignored = []
omitted = collections.Counter()
for name in git_names('--others', '--ignored', '--exclude-standard'):
    p = ROOT / name
    if name.startswith('.venv/') or '__pycache__/' in name or p.suffix in ('.pyc', '.bak') or p.name == '.DS_Store':
        omitted['environment_bytecode_editor'] += 1
        continue
    if name.startswith('logs/'):
        omitted['logs'] += 1
        continue
    if 'barclays_figure1.png' in name or '/transcripts/' in name or '/sellside/' in name:
        reason = 'Licensed source material; local only'
    elif name.startswith(('raw/ccc_direct_', 'raw/reference/')):
        reason = 'Original private/source workbook; extracted model inputs published separately'
    elif name.startswith('raw/'):
        reason = 'Raw source/cache excluded by existing blanket raw/ rule'
    elif name.startswith('data/'):
        reason = 'Bulk collection/database or regenerable export excluded by existing rules'
    else:
        reason = 'Existing ignored artifact; retained locally'
    ignored.append(dict(path=name, bytes=p.stat().st_size, reason=reason))

write_csv('files.csv', files, ['path', 'category', 'bytes', 'sha256'])
write_csv('local_only.csv', ignored, ['path', 'bytes', 'reason'])
summary = dict(publication_date='2026-09-30', base_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
               payload_files=len(files), payload_bytes=sum(x['bytes'] for x in files), categories=dict(sorted(counts.items())),
               payload_extensions=dict(sorted(collections.Counter(Path(x['path']).suffix or '[none]' for x in files).items())),
               ignored_research_files=len(ignored), ignored_research_bytes=sum(x['bytes'] for x in ignored),
               ignored_runtime_files_omitted=dict(omitted), staged_bytes_match=True, common_credential_scan='no matches',
               inventory_directory_excluded_from_self_hashes=PREFIX,
               scope='Repository publication payload only; local exclusions listed separately; no claim of full raw-source or external-file backup')
(HERE / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
