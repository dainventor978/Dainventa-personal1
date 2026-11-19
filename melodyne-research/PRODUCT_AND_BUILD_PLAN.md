# Original pitch-editing plugin — product specification and build plan
Date: 2026-11-19
Status: researched design; NOT a completed plugin or verified build.

## Competitor capabilities and gap
- Celemony Melodyne 5: note blobs, manual pitch/timing/duration, formants and sibilants, audio-to-MIDI, chord-note editing in Editor/Studio, multitrack editing in Studio. Official comparison: https://www.celemony.com/en/melodyne/melodyne-5-editions
- Antares Auto-Tune Pro: live automatic tuning plus graphical correction.
- Synchro Arts RePitch / Revoice: graphical pitch editing and alignment of layered vocals.
- Differentiation is a proposed workflow, not a claim of unprecedented technology. No feature should be marketed as never-before-seen without a patent and prior-art review.

## Proposed product: unified live + offline editor
1. Live Mode: key/scale-selectable correction, retune speed, humanize, wet/dry, bypass, MIDI note guidance; explicit latency indicator.
2. Edit Mode: import/capture audio, detect monophonic voiced segments, display editable note blobs on piano roll, drag pitch/timing/duration, undo/redo, before/after A/B.
3. Voice Integrity: separately adjustable vibrato preservation, pitch drift, breath/sibilance protection, formant preservation, transient-aware timing.
4. Harmony Workshop: optional generated thirds/fifths/octaves with per-voice panning and level, harmony MIDI export.
5. Smart Assistant (proposed): highlight suspicious notes with confidence scores; suggest corrections without silently overwriting performance. Keep fully manual controls.
6. CPU Guard: configurable quality tiers, offline high-quality render, CPU/latency meter and clipping LEDs, safe bypass on analysis failure.
7. Session Recall: deterministic serialization of edits, source audio hashes, missing-media warning, preset migration.
8. Accessibility: keyboard navigation, scalable interface, high-contrast note colors and readable labels.

## Engineering architecture
- JUCE C++17 plugin targets: macOS Intel AU/VST3 first; avoid AAX until licensed SDK access.
- Real-time path: bounded-allocation audio callback, lock-free handoff, no disk I/O or model inference on audio thread.
- Offline analysis: pitch estimator (YIN/pYIN candidate), voiced/unvoiced classifier, onset detection, note segmentation, confidence output. Validate on known ground-truth samples.
- Rendering: prototype phase-vocoder/PSOLA-like algorithm for monophonic voice, preserve formants where feasible; benchmark artifacts before making quality claims.
- Editor: timeline + piano keyboard + waveform + note rectangles; draggable controls and snapping; non-destructive edit model.
- ARA: separate later milestone requiring host compatibility and SDK/licensing review. Do not promise it in first installer.
- Polyphonic direct-note editing: research milestone only; significantly harder than monophonic tuning and NOT in MVP.
- User-supplied source audio never uploaded without explicit permission.

## Delivery gates (each must have evidence)
G1. Offline command-line WAV analysis outputs time-stamped notes and confidence; synthetic tests pass.
G2. Offline WAV pitch correction renders actual changed audio; compare pitch error, artifacts and preservation of unvoiced sounds.
G3. Interactive drag-edit GUI and undo/redo; automated editor-state tests.
G4. Real-time plugin audio path with bypass and CPU/latency instrumentation; no allocations in callback.
G5. Build Intel macOS AU + VST3 and package signed/notarized installer only when credentials available; unsigned build labeled clearly.
G6. Validate in at least two DAWs and report actual CPU, latency, pitch accuracy, stability.
G7. Advanced formant, harmonies, and assistive suggestions; polyphonic and ARA only after separate feasibility gates.

## Acceptance examples
- Pure 440 Hz A4 sample maps to A4 within specified tolerance and never produces NaN.
- Silence, breath, plosives and clipped input do not invent confident sustained notes.
- Dragging note +100 cents produces a reproducible pitch change in rendered output.
- Mix=0 and bypass output bit-identical input when latency compensation is disabled.
- Saved edits survive project reopen and source mismatch is clearly indicated.
- No audio-thread allocation, no crashes after repeated sample-rate/buffer-size changes.

## Immediate implementation order
Implement and test G1 first, then G2; do not build an attractive fake piano roll without real analysis/rendering. Keep this project distinct from OV1/OV2/TriFusion until independently working.
