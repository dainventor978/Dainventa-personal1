#!/usr/bin/env python3
"""Melody Beats licensed multisample playback prototype (offline, stdlib only).

Manifest format: {"name":"...", "samples":[{"file":"C4.wav","root":60,
"low":48,"high":71,"velocity_low":1,"velocity_high":127}, ...]}.
WAV paths must be relative to manifest directory. Only mono 16-bit PCM WAV.
Samples are NOT bundled: provide recordings with verified redistribution rights.
"""
import json
import math
import struct
import wave
from pathlib import Path

def load_instrument(manifest_path):
    path = Path(manifest_path).resolve()
    spec = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(spec.get("samples"), list) or not spec["samples"]:
        raise ValueError("Manifest requires at least one sample")
    zones = []
    for entry in spec["samples"]:
        filename = entry["file"]
        sample_path = (path.parent / filename).resolve()
        if not sample_path.is_relative_to(path.parent) or sample_path.suffix.lower() != ".wav":
            raise ValueError("Sample must be a relative WAV inside instrument folder")
        root, low, high = (int(entry[k]) for k in ("root", "low", "high"))
        vl = int(entry.get("velocity_low", 1))
        vh = int(entry.get("velocity_high", 127))
        if not (0 <= low <= root <= high <= 127 and 1 <= vl <= vh <= 127):
            raise ValueError("Invalid pitch or velocity zone")
        with wave.open(str(sample_path), "rb") as wav:
            if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getcomptype() != "NONE":
                raise ValueError("Expected mono 16-bit PCM WAV")
            rate = wav.getframerate()
            samples = [s[0] / 32768 for s in struct.iter_unpack("<h", wav.readframes(wav.getnframes()))]
        if rate <= 0 or not samples:
            raise ValueError("Empty or invalid sample")
        zones.append((root, low, high, vl, vh, rate, samples))
    return zones

def render_sampled(events, zones, rate=44100, release=.12):
    """Sampled instrument renderer. MIDI event list stays unchanged."""
    if not 8000 <= rate <= 192000 or not 0 <= release <= 10:
        raise ValueError("Invalid render settings")
    if not events:
        return b""
    if any(start < 0 or duration <= 0 or not 0 <= pitch <= 127 or not 1 <= velocity <= 127
           for start, duration, pitch, velocity in events):
        raise ValueError("Invalid note event")
    length = math.ceil(max(start + duration + release for start, duration, _, _ in events) * rate)
    if length > rate * 120:
        raise ValueError("Maximum render duration: 120 seconds")
    mix = [0.0] * length
    for start, duration, pitch, velocity in events:
        candidates = [z for z in zones if z[1] <= pitch <= z[2] and z[3] <= velocity <= z[4]]
        if not candidates:
            raise ValueError("No sample zone for note %d velocity %d" % (pitch, velocity))
        # Prefer the closest root pitch; then narrowest velocity range.
        root, _, _, _, _, sample_rate, samples = min(
            candidates, key=lambda z: (abs(z[0] - pitch), z[4] - z[3]))
        increment = (sample_rate / rate) * 2 ** ((pitch - root) / 12)
        first = int(start * rate)
        frames = min(length - first, math.ceil((duration + release) * rate))
        for i in range(frames):
            src = i * increment
            idx = int(src)
            if idx + 1 >= len(samples):
                break
            fraction = src - idx
            amplitude = samples[idx] * (1 - fraction) + samples[idx + 1] * fraction
            t = i / rate
            # Release begins at note-off; no abrupt cut.
            env = 1.0 if t < duration else max(0.0, 1 - (t - duration) / max(release, 1e-8))
            mix[first + i] += amplitude * env * (velocity / 127)
    return b"".join(struct.pack("<h", round(32767 * math.tanh(x))) for x in mix)

def write_sampled_wav(destination, events, manifest_path, trifusion=False, rate=44100):
    pcm = render_sampled(events, load_instrument(manifest_path), rate)
    if trifusion and pcm:
        from melody_beats_synth import trifusion_process, trifusion_matrix
        pcm = trifusion_process(pcm, trifusion_matrix(events), rate=rate)
    with wave.open(str(destination), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(rate)
        out.writeframes(pcm)
