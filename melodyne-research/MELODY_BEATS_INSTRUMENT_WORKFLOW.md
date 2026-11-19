# Melody Beats: MIDI clip + instrument swap specification
2026-11-19. Design specification; not yet implemented.

## Product behavior
- Library of 500 melodic/harmonic MIDI phrases in multiple genres. NO drums, percussion, drum tracks or percussion grooves.
- Drag a melody clip from Melody Beats to a DAW MIDI track (or to an internal arrangement lane).
- Drag an instrument preset onto the same track to change its sound while preserving all MIDI notes, velocities, durations, and timing.
- Instrument categories: acoustic/electric bass, acoustic/electric guitar, piano/keys, strings, saxophone, trumpet/brass, synth leads/pads. MIDI remains instrument-independent.
- Click an instrument to audition the selected melody. Show instrument name, patch source, licensing, load status and latency.
- Keep note clip and instrument assignment as separate data models: MidiClip{events,tempo,key,genre,id}; InstrumentSlot{engine,preset_id,level,pan}; Track{clips,slot}.
- Replacing an InstrumentSlot never rewrites MidiClip events. Undo restores the prior instrument assignment.
- External DAW export: .mid contains note data only; instrument audio playback requires a host instrument, built-in synth/sampler, or legally redistributable samples.
- Plugin hosting inside a plugin is host-dependent and difficult; first implement internal sample/synth instrument engine, then support DAW-native instrument swaps through exported MIDI.
- Drag-and-drop across DAWs requires native OS file drag, or host-specific APIs; validate Logic and Ableton separately rather than promising universal support.

## Build milestones
1. Produce and test 500 unique MIDI-only phrases, with deterministic seed, named genre, key, tempo, phrase length, note count, and duplicate detection. No percussion channel 10 or GM drum kits.
2. MIDI browser with piano-roll preview, genre/key/BPM filters, audition and export.
3. Instrument engine: synthesis presets for bass, keys, strings, brass and reeds, with ADSR, velocity and polyphony management. Label synthesized timbres honestly; do not claim sampled realism.
4. Track lanes and independent instrument slots, drag-to-assign, undo/redo, save/reload.
5. Mac Intel VST3/AU build and actual DAW validation; CPU and audio quality tests.

## Test cases
- Reassign piano -> bass -> sax -> trumpet -> strings without changing MIDI event bytes.
- Instrument patch change does not shift note pitch or timing; transpose is a separate explicit command.
- Notes outside instrument range get a visible warning; don't silently delete them.
- Changing a patch during playback does not crash or leave stuck notes.
- Exported MIDI loads in both Logic and Ableton with the same notes.
- No audio or samples inside exported MIDI files.

## Scope
This is a new Melody Beats product workflow, distinct from Celemony Melodyne pitch correction. Both can eventually share a note editor but they are not the same feature.
