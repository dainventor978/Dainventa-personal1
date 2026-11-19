#!/usr/bin/env python3
"""Melody Beats: offline sample-triggered beat sequencer, Python stdlib.

Usage: python beat_sampler.py --kit kit.json --pattern pattern.json --out beat.wav
Kit JSON: {"kick":"samples/kick.wav","snare":"samples/snare.wav"}
Pattern JSON: {"bpm":120,"steps":16,"bars":2,"hits":[
 {"step":0,"sound":"kick","velocity":1.0},{"step":4,"sound":"snare"}]}
Samples must be mono/stereo 16-bit PCM WAV. No samples are bundled.
"""
import argparse
import json
import math
import struct
import wave
from pathlib import Path

def read_sample(path, output_rate):
    with wave.open(str(path), "rb") as f:
        channels, width, rate = f.getnchannels(), f.getsampwidth(), f.getframerate()
        if channels not in (1, 2) or width != 2 or f.getcomptype() != "NONE":
            raise ValueError("Only mono/stereo 16-bit PCM WAV supported: " + str(path))
        frames = f.readframes(f.getnframes())
    raw = [x[0] / 32768 for x in struct.iter_unpack("<h", frames)]
    stereo = [(raw[i], raw[i] if channels == 1 else raw[i+1])
              for i in range(0, len(raw), channels)]
    if not stereo:
        raise ValueError("Empty sample: " + str(path))
    count = max(1, math.ceil(len(stereo) * output_rate / rate))
    result = []
    for i in range(count):
        position = min((len(stereo)-1), i * rate / output_rate)
        a = int(position)
        b = min(a+1, len(stereo)-1)
        fraction = position-a
        result.append((stereo[a][0]*(1-fraction)+stereo[b][0]*fraction,
                       stereo[a][1]*(1-fraction)+stereo[b][1]*fraction))
    return result

def render_beat(kit_path, pattern_path, out_path, rate=44100):
    kit_path = Path(kit_path).resolve()
    pattern = json.loads(Path(pattern_path).read_text(encoding="utf-8"))
    kit = json.loads(kit_path.read_text(encoding="utf-8"))
    bpm = float(pattern["bpm"])
    steps = int(pattern.get("steps",16))
    bars = int(pattern.get("bars",1))
    if not (30 <= bpm <= 300 and steps in (4,8,16,32,64) and 1 <= bars <= 128):
        raise ValueError("BPM, steps, or bars out of range")
    if not (8000 <= rate <= 192000):
        raise ValueError("Invalid sample rate")
    hits = pattern.get("hits",[])
    if len(hits) > 10000:
        raise ValueError("Too many hits")
    samples = {}
    for sound, filename in kit.items():
        sample_path = (kit_path.parent / filename).resolve()
        if not sample_path.is_relative_to(kit_path.parent):
            raise ValueError("Sample path escapes kit directory")
        samples[sound] = read_sample(sample_path,rate)
    # Steps are subdivisions of each 4/4 bar.
    step_duration = 240.0 / bpm / steps
    total_frames = math.ceil(bars * steps * step_duration * rate)
    longest = max((len(v) for v in samples.values()), default=0)
    if (total_frames + longest) > rate * 600:
        raise ValueError("Maximum output duration: 10 minutes")
    left = [0.0] * (total_frames+longest)
    right = [0.0] * (total_frames+longest)
    for hit in hits:
        sound = hit["sound"]
        step = int(hit["step"])
        velocity = float(hit.get("velocity",1.0))
        if sound not in samples or not (0 <= step < bars*steps) or not (0 <= velocity <= 1):
            raise ValueError("Invalid sound, step, or velocity")
        start = round(step*step_duration*rate)
        for i,(l,r) in enumerate(samples[sound]):
            left[start+i] += l*velocity
            right[start+i] += r*velocity
    with wave.open(str(out_path),"wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(rate)
        pcm = bytearray()
        for l,r in zip(left,right):
            pcm.extend(struct.pack("<hh",round(32767*math.tanh(l)),
                                   round(32767*math.tanh(r))))
        output.writeframes(pcm)
    return len(left)/rate

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--kit",required=True)
    parser.add_argument("--pattern",required=True)
    parser.add_argument("--out",required=True)
    parser.add_argument("--rate",type=int,default=44100)
    args=parser.parse_args()
    print("Rendered %.2f seconds" % render_beat(args.kit,args.pattern,args.out,args.rate))
