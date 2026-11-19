# Melody Beats + TriFusion: low-latency engineering requirements
Date: 2026-11-19. Specification, not measured performance.

## Targets
- Real-time MIDI note-on to audible synthesis: process in the host's next available block, without blocking locks, disk I/O, Python execution, or heap allocations in the audio callback.
- Support 32-, 64-, 128-, 256-, and 512-frame host buffers; prioritize stable 64-frame operation at 48 kHz on Intel Mac.
- At 48 kHz, one 64-frame block spans 1.333 ms. This is not full input/output round-trip latency.
- TriFusion Live mode: zero lookahead and no added algorithmic delay wherever practical; report any actual plugin delay to the host.
- Offline Quality mode may use lookahead, oversampling, and slower analysis; must clearly indicate extra latency.
- Use parameter smoothing, denormal protection, preallocated voice pool, bounded polyphony and lock-free control exchange.
- Preserve instrument transients: avoid aggressive compression on piano, harp and guitar; profile-dependent dynamics.
- CPU guard should measure processing time per block, warn before deadline overruns, and degrade optional quality features rather than mute/drop notes.
- Avoid sample-rate-specific fixed filter coefficients; recompute coefficients when host rate changes.
- Instrument changes should not block the audio thread. Load resources off-thread, atomically swap ready preset states, fade between voices to avoid clicks.
- MIDI generation and note analysis must run on worker threads or offline; never inside the real-time audio callback.
- TriFusion must remain switchable, and bypass should not modify the original MIDI event data.

## Tests needed
1. Measure plugin latency and callback time at 44.1/48/96 kHz and 32/64/128/256/512 sample buffers.
2. Test sustained polyphony and rapid preset changes without stuck notes, glitches or allocations.
3. Compare CPU use and latency with TriFusion enabled and bypassed.
4. Test real DAWs (Logic Pro, Ableton Live) on the user's Intel Mac before claiming latency targets achieved.

## Current limitations
Existing melody_beats_synth.py is an offline Python WAV renderer, not a low-latency audio plugin. This specification is a requirement; no measured 1.33 ms end-to-end performance or live VST/AU implementation is claimed.
