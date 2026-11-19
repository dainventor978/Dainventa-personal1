# Melody Beats — Professional Instrument Quality Standard
Date: 2026-11-19
Status: Product and engineering requirements. No sampled instrument library is included yet.

## Instrument architecture
- Keep MIDI note events independent of instrument choice. Changing a preset must never rewrite pitches, velocities, or timing.
- Two instrument sources: licensed multisampled acoustic instruments and programmable synthesizers.
- Use a common voice interface with note-on, note-off, pitch bend, expression, sustain pedal, sample-rate changes and preset changes.
- Route either source through the optional TriFusion processing engine; allow dry/wet comparison and bypass.

## Realistic sampled instruments
- Grand piano: multiple velocity layers, key release, sustain and pedal behavior, sympathetic resonance where resources permit.
- Electric piano: velocity-sensitive tone and release characteristics.
- Guitar and bass: separate attack/release behavior, slides, muted notes, hammer-ons and realistic round-robin samples where licensed.
- Saxophone, trumpet, flute: legato, staccato, vibrato and breath/expression control; avoid claiming one static sample sounds like a live player.
- Strings: sustained and short articulations, dynamics, legato transitions and ensemble variations.
- Use legally distributable samples, with verified commercial redistribution rights and provenance. Do not copy another product's factory samples or presets.

## Performance
- Load/decode sample data on worker threads; prefetch attacks and stream tails as needed.
- No filesystem reads, blocking locks, unbounded allocations, or heavy MIDI analysis in the real-time callback.
- Preallocate bounded voice pools; smooth preset changes; implement voice stealing with click prevention.
- TriFusion Live mode: avoid lookahead, adapt per instrument, and report any actual plugin latency to the DAW.
- Validate at 44.1/48/96 kHz, multiple buffer sizes and polyphony loads; do not promise unmeasured latency.

## Catalog and acceptance
- First playable milestone: one legally distributable, convincing sampled grand piano and one synthesized instrument, both driven by identical MIDI clips.
- Validate note timing, velocity response, sustain, release, CPU cost, memory use, and audible quality before scaling the catalog.
- Long-term goal: 500+ meaningfully different playable presets; preset count does not equal independent engines or acoustic realism.
- Quality gate: blind listening comparisons against recorded references, plus measured performance and regression tests.
- Existing Python prototype: 12 synthesized patches. These are not recorded acoustic instruments or a finished VST3/AU plugin.
