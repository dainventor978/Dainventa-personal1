"""Regression tests: python3 -m unittest melodyne-research/test_trifusion_matrix.py"""
import math
import struct
import unittest
from melody_beats_synth import trifusion_matrix, trifusion_process, render

MELODY = [(0.0, .3, 60, 110), (.4, .3, 64, 105), (.8, .4, 67, 100)]
class TriFusionMatrixTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(trifusion_matrix([])["drive"], 1.0)
    def test_bounds(self):
        for events in (MELODY, [(0, 0.01, 127, 127)] * 100, [(0, 8, 0, 1)]):
            m = trifusion_matrix(events)
            self.assertTrue(1 <= m["drive"] <= 2.5)
            self.assertTrue(.62 <= m["ceiling"] <= .85)
    def test_rejects_invalid_notes(self):
        with self.assertRaises(ValueError):
            trifusion_matrix([(0, 1, 200, 100)])
    def test_matrix_changes_with_melody(self):
        self.assertNotEqual(trifusion_matrix(MELODY), trifusion_matrix([(0, 2, 48, 60)]))
    def test_output_and_note_integrity(self):
        before = list(MELODY)
        dry = render(MELODY, "grand_piano", rate=8000)
        wet = trifusion_process(dry, trifusion_matrix(MELODY))
        self.assertEqual(len(dry), len(wet))
        self.assertNotEqual(dry, wet)
        self.assertEqual(before, MELODY)
        self.assertTrue(all(-32768 <= sample <= 32767 for (sample,) in struct.iter_unpack("<h", wet)))
    def test_rejects_bad_matrix(self):
        with self.assertRaises(ValueError):
            trifusion_process(b"\x00\x00", {"drive": 99, "ceiling": .8, "output": .9})
if __name__ == "__main__":
    unittest.main()
