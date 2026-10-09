"""Portable R17 document and plotting tests. No model, private data or score execution."""
from __future__ import annotations
import copy
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import r17_audit as audit
import r17_figures as figures


def hb_fixture() -> tuple[bytes, bytes]:
    strings = io.StringIO()
    writer = csv.writer(strings, lineterminator='\n')
    writer.writerow(['label', 'cls', 'c_hb'])
    groups = io.StringIO()
    writer2 = csv.writer(groups, lineterminator='\n')
    writer2.writerow(['cls', 'mean', 'std', 'count'])
    for cls, count in zip(figures.CLASSES, (5, 7, 5)):
        for i in range(count):
            writer.writerow([f'{cls}-{i}', cls, 100.0 + i])
        writer2.writerow([cls, 123.0, 10.0, count])
    return strings.getvalue().encode(), groups.getvalue().encode()


def score_fixture() -> bytes:
    idac = {m: {'MAE_ln_gamma_inf': 0.2 + i / 100} for i, m in enumerate(figures.MODELS)}
    vle = {m: {'AAD_P_pct': 5.0 + i} for i, m in enumerate(figures.MODELS)}
    idac.update(n_points=708, n_systems=163)
    vle.update(n_points=9432)
    return json.dumps(dict(split='test', models=list(figures.MODELS), tables=dict(idac=idac, vle=vle))).encode()


class Documents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = audit.ROOT
        supplied = os.environ.get('R17_TEST_ORIGINAL')
        # Local reconstruction may supply an exact-blob original; normal checkout uses pinned Git.
        cls.original = Path(supplied).read_bytes() if supplied else audit.git_bytes(root, 'manuscript/draft.md')
        audit.require(audit.blob(cls.original) == audit.ORIGINAL_BLOB, 'test original is not exact reference')
        # The 2026-10-08 closeout edited the manuscript after R17; the R17 checks use the reviewed
        # R17 bytes (commit 7c1b899), and scripts/r17_closeout.py checks the later edits.
        show = lambda path: subprocess.check_output(['git', 'show', '7c1b899:' + path], cwd=root)
        cls.revised = show('manuscript/draft.md')
        cls.supp = show('manuscript/supplement.md')
        cls.ledger = json.loads(show('docs/astra/round17/CLAIMS.json'))

    def check(self, **kw):
        args = dict(original=self.original, revised=self.revised, supplement=self.supp, ledger=self.ledger)
        args.update(kw)
        return audit.documents(**args)

    def test_exact_reviewed_documents(self):
        out = self.check()
        self.assertEqual(out['numeric_blocks_indexed'], 68)
        self.assertEqual(out['original_tables_preserved'], 4)
        self.assertFalse(out['submission_ready'])

    def test_original_tamper(self):
        with self.assertRaises(ValueError): self.check(original=self.original + b'\n')

    def test_revised_tamper(self):
        with self.assertRaises(ValueError): self.check(revised=self.revised + b'\n')

    def test_supplement_tamper(self):
        with self.assertRaises(ValueError): self.check(supplement=self.supp + b'\n')

    def test_missing_claim(self):
        ledger = copy.deepcopy(self.ledger); ledger['claims'].pop()
        with self.assertRaises(ValueError): self.check(ledger=ledger)

    def test_claim_location(self):
        ledger = copy.deepcopy(self.ledger); ledger['claims'][1]['start_line'] += 1
        with self.assertRaises(ValueError): self.check(ledger=ledger)

    def test_duplicate_claim_id(self):
        ledger = copy.deepcopy(self.ledger); ledger['claims'][1]['id'] = ledger['claims'][0]['id']
        with self.assertRaises(ValueError): self.check(ledger=ledger)

    def test_fabricated_ready_flag(self):
        ledger = copy.deepcopy(self.ledger); ledger['submission_ready'] = True
        with self.assertRaises(ValueError): self.check(ledger=ledger)

    def test_no_unexplained_original_table_loss(self):
        old = audit.tables(self.original.decode())[0]
        revised = self.revised.replace(old.encode(), b'')
        ledger = copy.deepcopy(self.ledger); ledger['revised_sha256'] = audit.sha(revised)
        with self.assertRaises(ValueError): self.check(revised=revised, ledger=ledger)

    def test_lost_lv1_qualification(self):
        revised = self.revised.replace(b'failed the joint registered screen', b'passed this screen')
        ledger = copy.deepcopy(self.ledger); ledger['revised_sha256'] = audit.sha(revised)
        with self.assertRaises(ValueError): self.check(revised=revised, ledger=ledger)


class ArithmeticAndSafety(unittest.TestCase):
    def test_blob_known_empty(self):
        self.assertEqual(audit.blob(b''), 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391')

    def test_rounding_he_is_compatible(self):
        self.assertTrue(audit.rounded_difference_compatible('632.9', '618.6', '14.2', 1))

    def test_shapley_bias_is_not_singleton(self):
        self.assertFalse(audit.rounded_difference_compatible('-2.79', '1.44', '-4.47', 2))

    def test_rounding_nonfinite(self):
        with self.assertRaises(ValueError): audit.rounded_difference_compatible('NaN', '1', '0', 2)

    def test_rounding_invalid_precision(self):
        with self.assertRaises(ValueError): audit.rounded_difference_compatible('1', '1', '0', -1)

    def test_paths(self):
        for valid in ('manuscript/draft.md', 'results/scorecard_test_main7.json', 'PREREGISTRATION.md'):
            audit.safe_relative(valid)
        for invalid in ('../secrets', '/tmp/file', 'data/raw/nist/UD/x.sigma', 'results/predictions/x.csv'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError): audit.safe_relative(invalid)

    def test_fresh_path_is_resolved(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp).resolve(); root = parent / 'repo'; root.mkdir()
            out = audit.fresh_output(parent / 'report', root)
            self.assertEqual(out, (parent / 'report').resolve())
            with self.assertRaises(FileExistsError): audit.fresh_output(out, root)

    def test_inside_checkout_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve(); (root / '.git').mkdir()
            with self.assertRaises(ValueError): audit.fresh_output(root / 'bad', root)

    def test_other_checkout_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve(); repo = root / 'repo'; repo.mkdir()
            other = root / 'other'; other.mkdir(); (other / '.git').mkdir()
            with self.assertRaises(ValueError): audit.fresh_output(other / 'out', repo)

    def test_source_hash_mismatch_stops(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'changed'):
            with self.assertRaises(ValueError): audit.sources(Path(temp), {'README.md': '0' * 40})

    def test_working_source_mismatch_stops(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
            root = Path(temp); (root / 'README.md').write_bytes(b'changed')
            with self.assertRaises(ValueError): audit.sources(root, {'README.md': audit.blob(b'original')})

    def test_exact_source_passes(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
            root = Path(temp); (root / 'README.md').write_bytes(b'original')
            result = audit.sources(root, {'README.md': audit.blob(b'original')})
            self.assertEqual(result['README.md']['bytes'], 8)

    def test_reviewed_readme_append(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
            root = Path(temp); current = b'original\nreviewed append'; (root / 'README.md').write_bytes(current)
            audit.sources(root, {'README.md': audit.blob(b'original')}, {'README.md': audit.sha(current)})
            with self.assertRaises(ValueError):
                audit.sources(root, {'README.md': audit.blob(b'original')}, {'README.md': '0' * 64})

    def test_source_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
            parent = Path(temp).resolve(); root = parent / 'repo'; root.mkdir()
            external = parent / 'file'; external.write_bytes(b'original')
            (root / 'README.md').symlink_to(external)
            with self.assertRaises(ValueError): audit.sources(root, {'README.md': audit.blob(b'original')})

    def test_registration_append_preserves_history(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, 'git_bytes', return_value=b'original'):
            root = Path(temp); proposed = root / 'docs/astra/round17/REGISTRATION_PROPOSED.md'
            proposed.parent.mkdir(parents=True); proposed.write_bytes(b'R17 proposal')
            (root / 'PREREGISTRATION.md').write_bytes(b'original\nRound 17 adopted at DATE\nR17 proposal')
            audit.sources(root, {'PREREGISTRATION.md': audit.blob(b'original')})
            (root / 'PREREGISTRATION.md').write_bytes(b'revised history\nRound 17 adopted at DATE\nR17 proposal')
            with self.assertRaises(ValueError): audit.sources(root, {'PREREGISTRATION.md': audit.blob(b'original')})


class FigureData(unittest.TestCase):
    def test_hb_uses_stored_means(self):
        data = figures.figure2_data(*hb_fixture())
        self.assertEqual(data['means'], [123.0] * 3)
        self.assertEqual(data['count'], 17)

    def test_hb_missing_dimer(self):
        a, b = hb_fixture()
        a = b'\n'.join(a.splitlines()[:-1]) + b'\n'
        with self.assertRaises(ValueError): figures.figure2_data(a, b)

    def test_hb_nonfinite(self):
        a, b = hb_fixture(); a = a.replace(b'100.0', b'nan', 1)
        with self.assertRaises(ValueError): figures.figure2_data(a, b)

    def test_hb_duplicate_identity(self):
        a, b = hb_fixture(); a = a.replace(b'OH-OH-1,', b'OH-OH-0,', 1)
        with self.assertRaises(ValueError): figures.figure2_data(a, b)

    def test_main7_stored_values(self):
        d = figures.figure3_data(score_fixture())
        self.assertEqual(d['IDAC_rows'], 708)
        self.assertEqual(d['VLE_rows'], 9432)
        self.assertEqual(d['VLE'][0], 5.0)

    def test_main7_wrong_denominator(self):
        d = json.loads(score_fixture()); d['tables']['idac']['n_points'] = 762
        with self.assertRaises(ValueError): figures.figure3_data(json.dumps(d).encode())

    def test_main7_wrong_models(self):
        d = json.loads(score_fixture()); d['models'].append('hanna')
        with self.assertRaises(ValueError): figures.figure3_data(json.dumps(d).encode())

    def test_main7_nonfinite(self):
        d = json.loads(score_fixture()); d['tables']['vle']['Z0x']['AAD_P_pct'] = float('nan')
        with self.assertRaises(ValueError): figures.figure3_data(json.dumps(d).encode())

    def test_render_synthetic_fig2(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'fig2.png'
            figures.render2(figures.figure2_data(*hb_fixture()), path)
            self.assertEqual(path.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')

    def test_render_synthetic_fig3(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'fig3.png'
            figures.render3(figures.figure3_data(score_fixture()), path)
            self.assertEqual(path.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')

    def test_real_cli_wrong_input_hash_before_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'repo'; root.mkdir()
            for path in figures.INPUTS:
                p = root / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b'wrong')
            out = Path(temp) / 'out'
            with self.assertRaises(ValueError): figures.run(root, out)
            self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
