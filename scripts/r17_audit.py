"""R17 reporting checks only. Never imports a model or reads prediction/profile data.

Default CLI requires the actual pinned Git objects in an asset-independent checkout.
A successful mechanical audit is not a claim that all editorial evidence is verified.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from decimal import Decimal
from pathlib import Path

BASE = '35ab60046f3f4a7566d8eeee6b13172a6d0becc2'
ORIGINAL_BLOB = 'edf2eae2b30fb97b8934c4e86c81a09685e8704d'
ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tables(text: str) -> list[str]:
    return re.findall(r'(?m)^\|[^\n]*(?:\n\|[^\n]*)+', text)


def numeric_blocks(text: str) -> list[tuple[int, int, str]]:
    result = []
    for match in re.finditer(r'\S[^\n]*(?:\n(?!\n)[^\n]+)*', text):
        if re.search(r'\d', match.group()):
            result.append((text.count('\n', 0, match.start()) + 1,
                           text.count('\n', 0, match.end()) + 1, match.group()))
    return result


def documents(original: bytes, revised: bytes, supplement: bytes, ledger: dict) -> dict:
    """Check supplied documents, without implying that external sources were re-read."""
    require(ledger['base'] == BASE, 'wrong base in claim ledger')
    require(blob(original) == ORIGINAL_BLOB == ledger['original_blob'], 'original manuscript changed')
    require(sha(revised) == ledger['revised_sha256'], 'revised manuscript differs from reviewed patch')
    require(sha(supplement) == ledger['supplement_sha256'], 'supplement differs from reviewed patch')
    old, new, sup = (x.decode('utf-8') for x in (original, revised, supplement))
    blocks = numeric_blocks(old)
    claims = ledger['claims']
    require(len(blocks) == len(claims), 'missing or additional claim block')
    require(len({c['id'] for c in claims}) == len(claims), 'duplicate claim id')
    for (a, b, text), claim in zip(blocks, claims):
        require((a, b) == (claim['start_line'], claim['end_line']), 'claim location mismatch')
        require(sha(text.encode()) == claim['original_sha256'], 'claim text mismatch')
        require(bool(claim['status'] and claim['fix']), 'claim lacks a disposition')
    old_tables = tables(old)
    require(all(table in new + '\n' + sup for table in old_tables), 'an original table was changed or lost')
    lv1 = new.split('#### Registered negative result: LV1\n', 1)
    require(len(lv1) == 2, 'LV1 result missing')
    result_text = lv1[1].split('## 4. Discussion', 1)[0]
    for token in ('[-1.72, +0.13]', '[+0.008, +0.067]', '[+4.6, +25.1]',
                  '13.13%', '10.44%', '+14.2', '171,701', '51 pure-composition',
                  'failed the joint registered screen'):
        require(token in result_text, 'missing LV1 qualification: ' + token)
    discussion = new.split('## 4. Discussion', 1)[1].split('## 5. Limitations', 1)[0]
    require('LV1 made that declared change and failed' in discussion, 'discussion omits LV1 failure')
    require('closed for this project' in discussion, 'project closeout missing')
    require('No fitted factorial corner' in new, 'no-adoption statement missing')
    require(ledger['submission_ready'] is False and len(ledger['open_items']) > 0,
            'unverified editorial items silently marked complete')
    return dict(numeric_blocks_indexed=len(blocks), original_tables_preserved=len(old_tables),
                lv1_record_present=True, manuscript_blob_before=blob(original),
                manuscript_sha256_after=sha(revised), new_model_calls=0, new_QC_calls=0,
                submission_ready=False, open_items=ledger['open_items'],
                scope='Mechanical document checks. Claim dispositions are a human source audit, not a proof.')



def rounded_difference_compatible(left: str, right: str, difference: str, digits: int) -> bool:
    """Conservative compatibility of independently rounded public values; never a CI."""
    require(isinstance(digits, int) and 0 <= digits <= 12, 'invalid rounding precision')
    a, b, d = (Decimal(x) for x in (left, right, difference))
    require(all(x.is_finite() for x in (a, b, d)), 'nonfinite printed value')
    half = Decimal(5) * (Decimal(10) ** (-digits - 1))
    # left - right ranges over +/- 2 half-units; the printed difference over +/- half.
    return max(a - b - 2 * half, d - half) <= min(a - b + 2 * half, d + half)


def safe_relative(path: str) -> None:
    p = Path(path)
    require(not p.is_absolute() and '..' not in p.parts and path != '', 'unsafe source path')
    allowed = (path in ('PREREGISTRATION.md', 'PROGRESS.md', 'README.md', 'manuscript/draft.md') or
               path.startswith(('docs/astra/', 'results/scorecard_', 'results/error_map_',
                                'results/qc/', 'src/zcosmo/', 'scripts/', 'manuscript/figures/')))
    require(allowed and 'predictions' not in p.parts, 'source outside public audit allowlist')


def git_bytes(root: Path, path: str) -> bytes:
    safe_relative(path)
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=root,
                                   stderr=subprocess.PIPE)


def sources(root: Path, expected: dict[str, str], reviewed_changes: dict | None = None) -> dict:
    """Read only the hard-coded public sources and compare object and working bytes."""
    verified = {}
    for path, digest in expected.items():
        safe_relative(path)
        data = git_bytes(root, path)
        require(blob(data) == digest, 'pinned source object differs: ' + path)
        target = (root / path).resolve()
        require(target.is_relative_to(root.resolve()), 'source symlink leaves checkout: ' + path)
        current = target.read_bytes()
        if path in (reviewed_changes or {}):
            require(path == 'README.md' and current.startswith(data)
                    and sha(current) == reviewed_changes[path], 'reviewed README append differs')
        elif path == 'PREREGISTRATION.md' and current != data:
            proposed = (root / 'docs/astra/round17/REGISTRATION_PROPOSED.md').read_bytes()
            require(current.startswith(data) and proposed in current[len(data):]
                    and b'Round 17 adopted at ' in current[len(data):],
                    'historical registration changed or R17 append missing')
        else:
            require(current == data, 'working source differs: ' + path)
        verified[path] = dict(git_blob=digest, bytes=len(data), sha256=sha(data))
    return verified


def fresh_output(path: Path, root: Path) -> Path:
    path = path.expanduser().resolve()
    require(not path.is_relative_to(root.resolve()), 'output must be outside the checkout')
    require(not any((p / '.git').exists() for p in (path, *path.parents)), 'output is inside a Git checkout')
    path.mkdir(mode=0o700, parents=True, exist_ok=False)
    return path


def run(root: Path, output: Path) -> dict:
    root = root.resolve()
    ledger = json.loads((root / 'docs/astra/round17/CLAIMS.json').read_text())
    require(ledger['base'] == BASE, 'wrong audit base')
    subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'], cwd=root,
                   check=True, capture_output=True)
    result = documents(git_bytes(root, 'manuscript/draft.md'),
                       (root / 'manuscript/draft.md').read_bytes(),
                       (root / 'manuscript/supplement.md').read_bytes(), ledger)
    result['public_sources_verified'] = sources(root, ledger['sources'], ledger.get('edited_sources'))
    result['historical_private_statistics_recomputed'] = False
    result['figure_pixels_reviewed'] = False
    result['base_commit'] = BASE
    out = fresh_output(output, root)
    (out / 'audit.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.root, args.out)
    print(json.dumps(dict(mechanical_checks='passed',
                          source_objects=len(result['public_sources_verified']),
                          submission_ready=False, remaining_editorial_items=len(result['open_items']))))


if __name__ == '__main__':
    main()
