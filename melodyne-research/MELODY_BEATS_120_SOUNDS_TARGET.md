# Melody Beats: 120 playable melodic sounds — target
2026-11-19. Design target only; not yet implemented or tested.

## Benchmark and important distinction
Ableton Live 12 Suite's detailed edition comparison lists 21 software instrument devices (shop page lists 20); these are engines/devices, not individual sound presets. https://www.ableton.com/en/live/compare-editions and https://www.ableton.com/en/shop/live/
Therefore do not falsely claim 120 sounds exceeds Ableton's actual preset count. This project targets a broader user-facing catalog of 120 distinct melodic sounds, not 120 independently engineered synth engines.

## 120 melodic sound slots — 12 families x 10
1. Pianos: concert grand, upright, felt, bright, mellow, honky-tonk, cinematic, lo-fi, intimate, prepared.
2. Electric keys: tine EP, reed EP, bell EP, chorused EP, clavinet, soft organ, gospel organ, drawbar organ, analog keys, digital keys.
3. Basses: finger, picked, fretless, upright, slap, muted, sub, analog, FM, synth pluck.
4. Guitars: nylon, steel, jazz hollowbody, clean electric, muted electric, chorus electric, crunchy electric, sustained electric, twelve-string, ambient guitar.
5. Plucked strings: harp, mandolin, ukulele, banjo, sitar, koto, dulcimer, lute, pizzicato pluck, synthetic harp.
6. Solo strings: violin, viola, cello, contrabass, expressive violin, legato cello, spiccato violin, tremolo violin, lyrical viola, synthetic bowed string.
7. String ensembles: chamber strings, lush strings, cinematic strings, soft strings, staccato strings, pizzicato ensemble, high strings, low strings, swelling strings, synthetic string ensemble.
8. Brass: trumpet, muted trumpet, flugelhorn, trombone, bass trombone, French horn, tuba, warm brass, bright brass, cinematic brass.
9. Reeds: soprano sax, alto sax, tenor sax, baritone sax, clarinet, bass clarinet, oboe, bassoon, harmonica, expressive reed synth.
10. Flutes and winds: concert flute, piccolo, alto flute, recorder, pan flute, shakuhachi, ocarina, breathy flute, airy wind synth, wind ensemble.
11. Synth leads and plucks: analog mono lead, saw lead, square lead, FM lead, glide lead, acid lead, glass pluck, digital pluck, bell pluck, warm pluck.
12. Synth pads and textures: warm pad, analog pad, evolving pad, airy pad, dark pad, cinematic pad, string pad, choir-like synth, granular texture, ambient shimmer.

## Product behavior
- No drums, percussion, kits or rhythm-only patterns.
- 500 unique melody/harmony MIDI clips across genres, with key/BPM filters.
- Drag a clip to track; drag any instrument sound to track; instrument swap changes sound but leaves MIDI events unchanged.
- Every slot must produce audible audio before it is counted as implemented. Distinct names alone do not count.
- Synthesized approximations must be labeled; realistic acoustic sounds need legal samples or robust modeling.
- No claim that presets are equivalent to 120 distinct synthesis engines.

## Acceptance
- Automated inventory reports exactly 120 unique sound IDs, zero percussion IDs.
- Each sound renders a non-silent, finite output for a playable MIDI note.
- Instrument switching preserves MIDI note bytes; no stuck notes or crashes.
- Test Mac Intel VST3/AU host compatibility and real CPU/latency.
Status: specification, not a completed instrument library.
