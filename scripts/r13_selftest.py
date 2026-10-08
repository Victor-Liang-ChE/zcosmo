"""Portable R13 software tests. Fixtures contain public aggregate numbers only."""
from decimal import Decimal as D
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import r13_closeout as r

FIXTURE = '''| solvent | rows | MAE O | MAE C | MAE U | removed O→C | signed recovery | rows improved / worsened |
|---|---:|---:|---:|---:|---:|---:|---|
| ethylene glycol | 10 | 2.541 | 0.559 | 0.498 | 1.982 | 0.97 | 10 / 0 |
| diethylene glycol | 108 | 1.740 | 0.648 | 0.371 | 1.092 | 0.80 | 105 / 3 |
| triethylene glycol | 17 | 2.088 | 0.934 | 0.556 | 1.153 | 0.75 | 17 / 0 |
| tetraethylene glycol | 7 | 1.242 | 1.175 | 0.731 | 0.067 | 0.13 | 7 / 0 |
| **pooled** | **142** | **1.813** | **0.702** | **0.419** | **1.111** | **0.80** | **139 / 3** |
'''


class CloseoutTests(unittest.TestCase):
    def test_P46a_counts(self):
        self.assertEqual(r.table(FIXTURE)['ethylene glycol']['rows'], 10)
        self.assertEqual(r.table(FIXTURE)['pooled']['rows'], 142)

    def test_wrong_old_count_rejected(self):
        with self.assertRaises(ValueError): r.table(FIXTURE.replace('glycol | 10 |', 'glycol | 9 |'))

    def test_missing_solvent_rejected(self):
        with self.assertRaises(ValueError): r.table('\n'.join(FIXTURE.splitlines()[:-2]))

    def test_duplicate_row_rejected(self):
        with self.assertRaises(ValueError): r.table(FIXTURE + FIXTURE.splitlines()[2] + '\n')

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): r.table(FIXTURE.replace('2.541', 'NaN'))

    def test_wrong_outcomes_rejected(self):
        with self.assertRaises(ValueError): r.table(FIXTURE.replace('105 / 3', '105 / 2'))

    def test_rounding_is_not_false_exactness(self):
        rows = r.table(FIXTURE)
        z = rows['triethylene glycol']
        self.assertNotEqual(z['O'] - z['C'], z['removed'])
        self.assertTrue(r.overlaps(r.difference_interval(z['O'], z['C']), r.rounding_interval(z['removed'])))

    def test_false_recovery_rejected(self):
        with self.assertRaises(ValueError): r.table(FIXTURE.replace('0.97', '0.85'))

    def test_recovery_denominator(self):
        q = r.arithmetic(r.table(FIXTURE))
        self.assertAlmostEqual(q['comparator_gap_recovery'], .7969870875, places=9)
        self.assertAlmostEqual(q['original_absolute_error_fraction_removed'], .6127964699, places=9)
        self.assertGreater(q['comparator_gap_recovery'], q['original_absolute_error_fraction_removed'])

    def test_zero_denominator_rejected(self):
        with self.assertRaises(ValueError): r.recovery_interval(D('1'), D('.5'), D('1'))

    def test_cost_units(self):
        q = r.sizing()['cases'][1]
        self.assertEqual(q['TZVP_single_points'], 5040)
        self.assertEqual(q['SVP_energy_gradient_evaluations'], 40320)
        self.assertEqual(q['four_core_SVP_hours_at_assumed_seconds']['60'], 672)
        self.assertAlmostEqual(q['Mac_SP_hours_if_R11_small_panel_mean_transferred'], 34.65)

    def test_invalid_portfolio(self):
        for n in (0, -1, 2.5, True):
            with self.assertRaises(ValueError): r.sizing(n)

    def test_blob_verification_and_source_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); path = root / r.SOURCE; path.parent.mkdir(parents=True)
            path.write_text(FIXTURE)
            raw = path.read_bytes()
            with self.assertRaises(ValueError): r.audit(root)
            with patch.object(r, 'SOURCE_BLOB', r.blob(raw)):
                q = r.audit(root)
            self.assertFalse(q['adoption_authorized'])
            self.assertFalse(q['new_scientific_gate_passed'])
            self.assertEqual(q['SCF_calls'], 0)
            self.assertEqual(path.read_bytes(), raw)

    def test_fresh_output_only(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / 'existing.json'; out.write_text('keep')
            with patch('sys.argv', ['r13', '--out', str(out)]), patch.object(r, 'audit', return_value={}):
                with self.assertRaises(FileExistsError): r.main()
            self.assertEqual(out.read_text(), 'keep')

    def test_no_chemistry_imports(self):
        import ast
        tree = ast.parse(Path(r.__file__).read_text())
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import): imports.update(x.name.split('.')[0] for x in node.names)
            if isinstance(node, ast.ImportFrom): imports.add((node.module or '').split('.')[0])
        self.assertFalse(imports & {'pyscf', 'rdkit', 'zcosmo', 'r12_review', 'numpy', 'pandas'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
