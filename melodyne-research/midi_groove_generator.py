#!/usr/bin/env python3
"""Generate melodic and harmonic MIDI phrase clips (standard MIDI format 1).
No drums, audio, samples, or virtual instruments are embedded.
Run: python3 midi_groove_generator.py --out grooves
"""
import argparse
from pathlib import Path
import struct

PPQ = 480
BPM = 120
# name, GM drum note, hits in 16 steps, velocities
# Each bass/keys clip uses pitch-relative note events. Users can transpose after drag/drop.
MELODIC = {
    "bass_pulse": [(0,0,2,105),(4,0,2,96),(7,7,1,90),(8,0,2,110),(12,5,2,93),(15,7,1,90)],
    "bass_syncopated": [(0,0,2,108),(3,0,1,92),(6,7,2,98),(10,5,2,98),(14,7,2,88)],
    "minor_arpeggio": [(0,0,2,90),(2,3,2,80),(4,7,2,85),(6,12,2,84),(8,7,2,90),(10,3,2,82),(12,0,2,87),(14,7,2,81)],
    "major_chords": [(0,0,4,82),(0,4,4,78),(0,7,4,77),(8,5,4,80),(8,9,4,77),(8,12,4,75)],
    "offbeat_stabs": [(2,0,1,86),(2,3,1,84),(2,7,1,82),(6,0,1,86),(6,3,1,84),(6,7,1,82),(10,5,1,88),(10,8,1,84),(10,12,1,80),(14,5,1,88),(14,8,1,84),(14,12,1,80)],
}

def vlq(value):
    if value < 0:
        raise ValueError("Negative delta")
    chunks = [value & 0x7f]
    value >>= 7
    while value:
        chunks.insert(0, 0x80 | (value & 0x7f))
        value >>= 7
    return bytes(chunks)

def track(events):
    events.sort(key=lambda x: (x[0], x[1]))
    data = bytearray()
    previous = 0
    for tick, order, message in events:
        data += vlq(tick - previous) + message
        previous = tick
    data += b"\x00\xff\x2f\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + data

def midi_file(notes, channel=0, bars=4, bpm=BPM):
    if not 1 <= bpm <= 300:
        raise ValueError("BPM must be 1..300")
    if not 1 <= bars <= 128:
        raise ValueError("Bars must be 1..128")
    events = [(0, -2, b"\xff\x51\x03" + round(60000000/bpm).to_bytes(3, "big"))]
    for bar in range(bars):
        for step, pitch, duration, velocity in notes:
            start = bar * 16 * (PPQ // 4) + step * (PPQ // 4)
            end = start + duration * (PPQ // 4)
            if not 0 <= pitch <= 127:
                raise ValueError("Invalid pitch")
            events.append((start, 1, bytes([0x90 | channel, pitch, velocity])))
            events.append((end, 0, bytes([0x80 | channel, pitch, 0])))
    t = track(events)
    return b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ) + t

def generate(out, bpm=120, bars=4, root=48):
    out.mkdir(parents=True, exist_ok=True)
    for name, pattern in MELODIC.items():
        notes = [(step, root + offset, duration, velocity) for step, offset, duration, velocity in pattern]
        (out / f"{name}.mid").write_bytes(midi_file(notes, bars=bars, bpm=bpm))
    return len(MELODIC)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("grooves"))
    parser.add_argument("--bpm", type=int, default=120)
    parser.add_argument("--bars", type=int, default=4)
    parser.add_argument("--root", type=int, default=48, help="MIDI root note (48 = C3 by common convention)")
    args = parser.parse_args()
    count = generate(args.out, args.bpm, args.bars, args.root)
    print(f"Created {count} MIDI-only groove clips in {args.out}")
