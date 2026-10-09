"""R17 closeout check (2026-10-08). Document checks only: no model, prediction or profile is read.

The R17 audit (r17_audit.py) is byte-bound to the reviewed R17 manuscript at commit 7c1b899 and
requires submission_ready=false. This script re-runs that audit's document checks on the 7c1b899
bytes, so the R17 record stays verifiable, and then checks the closeout edits made after it:
the historical tables are still present, the withdrawn inferential claims are gone from the
manuscript, each R17 open item has a recorded resolution with existing source files, and the
public R17 sources are unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import r17_audit as audit

R17_COMMIT = '7c1b899'
ROOT = Path(__file__).resolve().parents[1]
LEDGER = 'docs/astra/round17/CLOSEOUT.json'
STATUSES = {'resolved', 'resolved_by_narrowing'}
# Strings that the closeout removed from the manuscript because their source output is lost.
WITHDRAWN = ('reports a significant LLE', 'should accompany that inferential claim',
             'Direct publisher verification remains', 'Provisional: the original publisher record',
             'publisher text and implications remain to be checked',
             'still needs an execution-artifact citation', '762 points in 177 systems')
REQUIRED_DRAFT = ('makes no inferential LLE claim', 'commit 6fe873c', '777 non-training observations',
                  'doi:10.1021/jacs.4c07099', '457-470', 'Software and data versions.',
                  'Hansen, A.; Neugebauer, H.')
REQUIRED_SUPP = ('is withdrawn because its source output could not be recovered',
                 'they are withdrawn', 'verified these statements')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(root: Path, rev: str, path: str) -> bytes:
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], cwd=root, stderr=subprocess.PIPE)


def check(root: Path) -> dict:
    root = root.resolve()
    ledger = json.loads((root / LEDGER).read_text())
    r17 = json.loads(git_show(root, R17_COMMIT, 'docs/astra/round17/CLAIMS.json'))
    original = git_show(root, audit.BASE, 'manuscript/draft.md')
    r17_draft = git_show(root, R17_COMMIT, 'manuscript/draft.md')
    r17_supp = git_show(root, R17_COMMIT, 'manuscript/supplement.md')
    record = audit.documents(original, r17_draft, r17_supp, r17)  # R17 record still passes
    draft = (root / 'manuscript/draft.md').read_bytes()
    supp = (root / 'manuscript/supplement.md').read_bytes()
    audit.require(sha(draft) == ledger['draft_sha256'], 'manuscript differs from the closeout ledger')
    audit.require(sha(supp) == ledger['supplement_sha256'], 'supplement differs from the closeout ledger')
    new, sup = draft.decode(), supp.decode()
    old_tables = audit.tables(original.decode())
    audit.require(all(t in new + '\n' + sup for t in old_tables), 'an original table was changed or lost')
    for token in WITHDRAWN:
        audit.require(token not in new, 'withdrawn wording still in manuscript: ' + token)
    for token in REQUIRED_DRAFT:
        audit.require(token in new, 'closeout wording missing from manuscript: ' + token)
    for token in REQUIRED_SUPP:
        audit.require(token in sup, 'closeout wording missing from supplement: ' + token)
    items = ledger['items']
    audit.require(len(items) == len(r17['open_items']) == 5, 'closeout must answer each R17 open item')
    for item, text in zip(items, r17['open_items']):
        audit.require(item['r17_text'] == text, 'closeout item does not match R17 open item')
        audit.require(item['status'] in STATUSES and item['resolution'], 'item lacks a resolution')
        for src in item['sources']:
            audit.require((root / src).is_file(), 'missing source file: ' + src)
    prov = root / 'docs/astra/round17/provenance'
    for line in (prov / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        audit.require(sha((prov / name.strip()).read_bytes()) == digest, 'provenance file changed: ' + name)
    sources = audit.sources(root, r17['sources'], r17.get('edited_sources'))
    for fig in ledger['figures']:
        data = (root / fig['path']).read_bytes()
        audit.require(sha(data) == fig['sha256'] and fig['pixels_inspected'], 'figure record mismatch')
    audit.require(ledger['new_model_calls'] == 0 and ledger['rescoring'] is False, 'closeout scope')
    ready = all(i['status'] in STATUSES for i in items)
    audit.require(ledger['submission_ready'] is ready, 'ready flag inconsistent with items')
    return dict(r17_record_passes=record['numeric_blocks_indexed'] == 68,
                original_tables_preserved=len(old_tables), items=len(items),
                public_sources_unchanged=len(sources), submission_ready=ready)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    print(json.dumps(check(parser.parse_args().root)))


if __name__ == '__main__':
    main()
