"""Run from melodyne-research: python3 -m unittest test_sampled_instrument.py"""
import json
import math
import struct
import tempfile
import unittest
import wave
from pathlib import Path
from sampled_instrument import load_instrument, render_sampled, write_sampled_wav

class SampledInstrumentTests(unittest.TestCase):
    def test_piano_sample_zone_and_render(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            sample = folder / "C4.wav"
            with wave.open(str(sample), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(16000)
                w.writeframes(b"".join(struct.pack("<h", int(10000 * math.sin(2 * math.pi * 261.6 * i / 16000))) for i in range(16000)))
            manifest = folder / "piano.json"
            manifest.write_text(json.dumps({"name": "Test piano", "samples": [
                {"file": "C4.wav", "root": 60, "low": 48, "high": 72, "velocity_low": 1, "velocity_high": 127}
            ]}))
            zones = load_instrument(manifest)
            notes = [(0.0, .2, 60, 100), (.3, .2, 64, 110)]
            original = list(notes)
            pcm = render_sampled(notes, zones, rate=16000)
            self.assertTrue(any(pcm))
            self.assertEqual(notes, original)
            destination = folder / "output.wav"
            write_sampled_wav(destination, notes, manifest, trifusion=True, rate=16000)
            with wave.open(str(destination)) as w:
                self.assertEqual(w.getframerate(), 16000)
                self.assertGreater(w.getnframes(), 0)
    def test_missing_zone(self):
        with self.assertRaises(ValueError):
            render_sampled([(0, .2, 60, 100)], [])
if __name__ == "__main__":
    unittest.main()
