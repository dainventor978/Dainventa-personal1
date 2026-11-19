#!/usr/bin/env python3
"""Melody Beats: playable, sample-free polyphonic MIDI synthesizer prototype.
Uses Python standard library only. Produces WAV audio from MIDI-note events.
No drums or percussion. Instrument patches are synthesized approximations.
Run: python3 melody_beats_synth.py --out demo.wav --patch warm_pad
"""
import argparse
import math
import struct
import wave
from dataclasses import dataclass

RATE = 44100
TAU = math.tau

@dataclass(frozen=True)
class Patch:
    name: str
    wave: str
    attack: float
    decay: float
    sustain: float
    release: float
    brightness: float

PATCHES = {
    "grand_piano": Patch("Grand piano (synthetic)", "piano", .006, .45, .24, .24, .68),
    "electric_keys": Patch("Electric keys (synthetic)", "fm", .008, .3, .44, .3, .45),
    "finger_bass": Patch("Finger bass (synthetic)", "triangle", .004, .16, .65, .14, .38),
    "synth_bass": Patch("Synth bass", "saw", .003, .18, .62, .15, .42),
    "clean_guitar": Patch("Clean guitar (synthetic)", "pluck", .003, .3, .2, .22, .63),
    "harp": Patch("Harp (synthetic)", "pluck", .003, .8, .08, .3, .74),
    "violin": Patch("Violin (synthetic)", "saw", .12, .2, .8, .35, .47),
    "string_ensemble": Patch("String ensemble (synthetic)", "strings", .24, .24, .78, .6, .46),
    "trumpet": Patch("Trumpet (synthetic)", "brass", .05, .2, .82, .2, .7),
    "saxophone": Patch("Saxophone (synthetic)", "reed", .06, .18, .76, .24, .6),
    "flute": Patch("Flute (synthetic)", "sine", .07, .12, .85, .28, .3),
    "warm_pad": Patch("Warm pad", "strings", .3, .3, .85, .8, .38),
}

def oscillator(kind, phase, brightness):
    s = math.sin(phase)
    if kind == "sine":
        return s
    if kind == "triangle":
        return (2 / math.pi) * math.asin(s)
    if kind == "saw":
        return (2 / math.pi) * math.atan(3 * math.sin(phase) - 1.2 * math.sin(2 * phase))
    if kind == "strings":
        return .65 * s + .23 * math.sin(2 * phase) + .12 * math.sin(3 * phase)
    if kind == "brass":
        return .55 * s + brightness * (.3 * math.sin(2 * phase) + .18 * math.sin(3 * phase))
    if kind == "reed":
        return .7 * s + brightness * (.2 * math.sin(3 * phase) + .12 * math.sin(5 * phase))
    if kind == "fm":
        return math.sin(phase + 1.3 * brightness * math.sin(2 * phase))
    if kind == "piano":
        return .65 * s + .22 * math.sin(2.001 * phase) + .13 * math.sin(3.004 * phase)
    if kind == "pluck":
        return .7 * s + .2 * math.sin(2 * phase) + .1 * math.sin(3 * phase)
    raise ValueError(kind)

def envelope(t, held, patch):
    if t < 0:
        return 0.
    if t < patch.attack:
        return t / max(patch.attack, 1e-6)
    if t < patch.attack + patch.decay:
        return 1 - (1 - patch.sustain) * ((t - patch.attack) / max(patch.decay, 1e-6))
    if t < held:
        return patch.sustain
    # At release, continue envelope smoothly rather than jumping to sustain.
    if held < patch.attack:
        start = held / max(patch.attack, 1e-6)
    elif held < patch.attack + patch.decay:
        start = 1 - (1 - patch.sustain) * ((held - patch.attack) / max(patch.decay, 1e-6))
    else:
        start = patch.sustain
    return start * max(0., 1 - (t - held) / max(patch.release, 1e-6))

def render(events, patch_name="warm_pad", rate=RATE):
    """events: (start_seconds, duration_seconds, midi_pitch, velocity 1..127)."""
    patch = PATCHES[patch_name]
    if not events:
        return b""
    if any(start < 0 or duration <= 0 or not 0 <= pitch <= 127 or not 1 <= velocity <= 127
           for start, duration, pitch, velocity in events):
        raise ValueError("Invalid MIDI note event")
    length = math.ceil(max(start + duration + patch.release for start, duration, _, _ in events) * rate)
    if length > rate * 120:
        raise ValueError("Maximum render duration: 120 seconds")
    mix = [0.] * length
    for start, duration, pitch, velocity in events:
        freq = 440 * 2 ** ((pitch - 69) / 12)
        first = int(start * rate)
        count = min(length - first, math.ceil((duration + patch.release) * rate))
        amp = (velocity / 127) ** 1.5 * .18
        for i in range(count):
            t = i / rate
            phase = TAU * freq * t
            mix[first + i] += amp * envelope(t, duration, patch) * oscillator(patch.wave, phase, patch.brightness)
    # Smooth bounded output, no clipping.
    return b"".join(struct.pack("<h", int(32767 * math.tanh(x))) for x in mix)

# Instrument-aware TriFusion defaults. Conservative settings preserve acoustic transients.
INSTRUMENT_MATRICES = {
    "grand_piano": {"drive": 1.15, "ceiling": .82, "output": .94, "eq_low": 0.0, "eq_high": .06},
    "electric_keys": {"drive": 1.35, "ceiling": .80, "output": .91, "eq_low": 0.0, "eq_high": .03},
    "finger_bass": {"drive": 1.35, "ceiling": .74, "output": .88, "eq_low": .14, "eq_high": -.12},
    "synth_bass": {"drive": 1.45, "ceiling": .73, "output": .86, "eq_low": .18, "eq_high": -.12},
    "clean_guitar": {"drive": 1.25, "ceiling": .80, "output": .90, "eq_low": -.04, "eq_high": .07},
    "harp": {"drive": 1.10, "ceiling": .84, "output": .94, "eq_low": -.04, "eq_high": .09},
    "violin": {"drive": 1.15, "ceiling": .80, "output": .92, "eq_low": -.04, "eq_high": -.03},
    "string_ensemble": {"drive": 1.20, "ceiling": .77, "output": .90, "eq_low": .02, "eq_high": -.04},
    "trumpet": {"drive": 1.20, "ceiling": .75, "output": .87, "eq_low": -.04, "eq_high": -.10},
    "saxophone": {"drive": 1.22, "ceiling": .77, "output": .89, "eq_low": .01, "eq_high": -.05},
    "flute": {"drive": 1.08, "ceiling": .84, "output": .95, "eq_low": -.07, "eq_high": .04},
    "warm_pad": {"drive": 1.30, "ceiling": .77, "output": .90, "eq_low": .04, "eq_high": -.04},
}

def instrument_matrix(patch_name, events):
    """Combine instrument profile and MIDI-aware control, without modifying notes."""
    if patch_name not in PATCHES:
        raise ValueError("Unknown instrument patch")
    base = dict(INSTRUMENT_MATRICES[patch_name])
    if events:
        dynamic = trifusion_matrix(events)
        base["drive"] = max(.5, min(3., base["drive"] * dynamic["drive"] / 1.8))
        base["ceiling"] = max(.5, min(.95, min(base["ceiling"], dynamic["ceiling"])))
    return base


def trifusion_matrix(events):
    """Map melody-note statistics to safe TriFusion processing parameters.
    This control matrix reads MIDI events; it does not alter or generate notes.
    """
    if not events:
        return {"drive": 1.0, "ceiling": 0.8, "output": 0.9}
    if any(start < 0 or duration <= 0 or not 0 <= pitch <= 127 or not 1 <= velocity <= 127
           for start, duration, pitch, velocity in events):
        raise ValueError("Invalid MIDI note event")
    mean_velocity = sum(v for _, _, _, v in events) / (127.0 * len(events))
    mean_pitch = sum(p for _, _, p, _ in events) / len(events)
    length = max(start + duration for start, duration, _, _ in events)
    density = min(1.0, len(events) / max(length * 8.0, 1.0))
    # More notes and louder performances get less saturation and more headroom.
    drive = max(1.0, min(2.5, 2.3 - 0.55 * density - 0.35 * mean_velocity))
    ceiling = max(0.62, min(0.85, 0.85 - 0.14 * density - 0.03 * (mean_pitch / 127.0)))
    return {"drive": drive, "ceiling": ceiling, "output": 0.9}


def trifusion_process(pcm, matrix=None, rate=RATE):
    """TriFusion post-engine: DC blocker, saturation, envelope gain control.
    Adapted from trifusion/trifusion.cpp; independent from MIDI synthesis.
    Operates on signed 16-bit mono PCM. Prototype, not real-time optimized.
    """
    if len(pcm) % 2:
        raise ValueError("PCM data must contain complete 16-bit samples")
    if rate <= 0:
        raise ValueError("Sample rate must be positive")
    matrix = matrix or {"drive": 2.0, "ceiling": 0.8, "output": 0.9}
    drive, ceiling, output = (matrix[k] for k in ("drive", "ceiling", "output"))
    if not (0.5 <= drive <= 3.0 and 0.5 <= ceiling <= 0.95 and 0 <= output <= 1):
        raise ValueError("Invalid TriFusion matrix settings")
    eq_low = matrix.get("eq_low", 0.0)
    eq_high = matrix.get("eq_high", 0.0)
    if not (-.3 <= eq_low <= .3 and -.3 <= eq_high <= .3):
        raise ValueError("Invalid instrument EQ settings")
    low_state = 0.0
    # Approximate a 175 Hz low shelf pivot consistently across sample rates.
    low_alpha = 1.0 - math.exp(-TAU * 175.0 / rate)
    last_input = last_output = envelope_peak = 0.0
    result = bytearray(len(pcm))
    for i in range(0, len(pcm), 2):
        sample = struct.unpack_from("<h", pcm, i)[0] / 32768.0
        dc = sample - last_input + 0.995 * last_output
        last_input, last_output = sample, dc
        # Simple two-band tilt EQ: low-pass state plus complementary high band.
        low_state += low_alpha * (dc - low_state)
        shaped = dc + eq_low * low_state + eq_high * (dc - low_state)
        saturated = math.tanh(shaped * drive) / math.tanh(drive)
        envelope_peak = max(abs(saturated), envelope_peak * 0.9995)
        gain = ceiling / envelope_peak if envelope_peak > ceiling else 1.0
        processed = max(-0.98, min(0.98, saturated * gain * output))
        struct.pack_into("<h", result, i, round(processed * 32767))
    return bytes(result)

def render_track(events, patch_name="warm_pad", trifusion=False, rate=RATE):
    """Render MIDI notes through selected instrument and optional TriFusion stage.

    Offline reference path. No audio-thread or low-latency performance claim.
    """
    pcm = render(events, patch_name, rate)
    if trifusion and pcm:
        pcm = trifusion_process(pcm, instrument_matrix(patch_name, events), rate=rate)
    return pcm

def write_wav(filename, events, patch_name="warm_pad", trifusion=False):
    pcm = render_track(events, patch_name, trifusion)
    with wave.open(str(filename), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(pcm)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="melody_beats_demo.wav")
    parser.add_argument("--patch", choices=sorted(PATCHES), default="warm_pad")
    parser.add_argument("--trifusion", action="store_true", help="Enable second processing engine")
    args = parser.parse_args()
    # Identical notes with any patch: changing patch never changes MIDI.
    melody = [(0., .35, 60, 110), (.4, .35, 64, 105), (.8, .35, 67, 105), (1.2, .7, 72, 115)]
    write_wav(args.out, melody, args.patch, trifusion=args.trifusion)
    print("Rendered", args.out, "using", args.patch, "TriFusion:", args.trifusion)
