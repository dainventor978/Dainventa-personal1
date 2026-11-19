# Melody Beats — 63-instrument target (2026-11-19)
Source: https://www.ableton.com/en/live/compare-editions (Live 12 Suite lists 21 software instruments at research time). 21 x 3 = 63.
IMPORTANT: This counts software instrument devices, NOT individual presets or distinct acoustic instrument sounds. Ableton shop pages sometimes show 20; benchmark chosen is the current detailed comparison at research time.

## Melody Beats requirement
63 playable melodic instrument **patches** in the first sound bank, with 63 independently selectable instrument identities/timbres, and a scalable engine. This is not a claim of 63 distinct synth engines. Separate eventual target: 63 engines only if technically justified. NO DRUMS, PERCUSSION OR DRUM KITS.

### 63 proposed melodic patches
Piano & keys (9): grand piano, upright piano, felt piano, bright piano, electric tine piano, electric reed piano, clavinet, harpsichord, celesta.
Bass (9): finger bass, pick bass, fretless bass, upright bass, synth sub bass, analog bass, FM bass, slap bass, warm pad bass.
Guitar & plucked strings (9): nylon guitar, steel guitar, jazz guitar, clean electric guitar, muted guitar, overdriven guitar, harp, mandolin, sitar.
Orchestral strings (9): solo violin, solo viola, solo cello, contrabass, violin ensemble, viola ensemble, cello ensemble, full string ensemble, pizzicato strings.
Brass (9): trumpet, muted trumpet, flugelhorn, trombone, bass trombone, French horn, tuba, brass section, soft brass ensemble.
Woodwinds & reeds (9): soprano sax, alto sax, tenor sax, baritone sax, clarinet, bass clarinet, flute, oboe, bassoon.
Synths & textures (9): analog lead, FM lead, pluck lead, soft pad, evolving pad, string pad, bell synth, glass keys, ambient texture.

## Implementation and validation
- Instrument identity = patch, not full independent synthesis engine. Use original synth patches initially, then legally licensed samples where acoustic realism is necessary.
- Store notes as separate MIDI clips. Assign or drag patch to track; changing patch must not modify MIDI notes.
- Preview each patch, expose volume/ADSR, show clipping/CPU indicators, implement preset loading and missing-asset reporting.
- Build 500 melody-only MIDI clips categorized by genre; verify unique patterns and MIDI export.
- Acceptance: enumerate exactly 63 non-percussion patches, render audible output for all, avoid stuck notes, preserve MIDI when swapping patches, validate Mac Intel AU/VST3 build.
- Current status: specification committed; 63 playable patches NOT yet implemented or tested.
