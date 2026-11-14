# Dainventa Personal — Storm FX Vol. 1

**Status:** first audio pack generated and locally QA-checked on November 14, 2026. This public repository holds *only metadata/documentation*, not the full WAV archive or future personal voice tags.

## What was created
- 120 original procedural sound effects
- 20 Lightning cracks
- 20 High-voltage arcs
- 20 Deep thunder sounds
- 20 Rain beds
- 20 Wind/weather sounds
- 20 Cinematic storm impacts
- Each source WAV is 48 kHz / 24-bit PCM. Some are mono one-shots, others stereo beds.
- A 12-excerpt MP3 listening montage, SHA-256 manifests (CSV/JSON), and the Python generator are included with the full download in the owning ChatGPT conversation.

## Synthesis and source disclosure
The sounds were designed with generated noise, oscillators, frequency sweeps, envelopes, filtering, and layered transients using Python/NumPy/SciPy. **No third-party recorded samples are intentionally incorporated.** They are synthetic effects, not field recordings. Human-authorship and copyright eligibility are fact-dependent and not guaranteed. Content matching may still occur.

## QA and limitations
File counts, WAV format, sample finiteness/level spot-checks, and ZIP CRC integrity were checked during packaging. The packs have not been tested on the owner's physical DAWs/hardware. Rain beds have not been verified as seamless loops. Master archive is about 132 MiB. There are **20**, not 200, sounds per category in this volume.

## File list
The downloadable archive contains:
- `WAV_24bit_48k/` — all six categories
- `STORM_LISTEN_FIRST.mp3`
- `Manifest.json` and `Manifest.csv` (file-level SHA-256)
- `README_START_HERE.md`
- `storm_generate.py`

## Personal collection safety
Do not commit large audio assets, third-party licensed samples, or uploaded name-tag/voice recordings to this public repository. Store the full audio pack in private storage or convert the repository to private before uploading personal assets. Large WAV datasets should use a suitable release/storage or Git LFS strategy, not hundreds of regular Git blobs.

## Reproducibility
The pack's ZIP includes the **actual Python source** used to generate these WAVs. Requires Python, NumPy, SciPy, and SoundFile; FFmpeg was used for the optional MP3 preview. Use original generator/checksum manifest from the supplied pack rather than a reconstruction.
