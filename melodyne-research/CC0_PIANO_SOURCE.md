# Melody Beats — verified candidate for free redistributable piano samples

Source: Meta Open Sound (Meta Creative Audio)
Repository: https://github.com/facebookincubator/Meta-open-sound
Collection: Meta Piano
Published license: CC0 1.0 Universal (verify collection LICENSE and manifest at exact downloaded revision before shipping)
Reported content: 352 recordings, 88 keys (A0–C8), four velocity layers.
Production WAV: 24-bit / 48 kHz, downloadable from the repository Releases page.
Sample maps: SFZ and manifest provided by publisher.

## Commercial distribution decision
The source explicitly states that the instrument collections are CC0 and may be modified, commercially used, and redistributed without attribution. This makes Meta Piano a candidate for bundling in Melody Beats without a sample-license purchase. Record source URL, release tag, checksum and license file with any bundled assets. Do not confuse with the Oculus Audio Pack, which is CC BY 4.0 and requires attribution.

## Implementation notes
- The current Python sampled_instrument.py only accepts mono 16-bit PCM WAV, while Meta's source WAVs are 24-bit/48k. Convert using a tested offline conversion step with clipping/dither considerations, or update the sampler for 24-bit decoding before integration.
- Map all velocity layers and pitch zones from the supplied SFZ, not just filename guesses.
- Verify downloaded file checksums and license, then run pitch, velocity, sustain, note-off, sample-rate and TriFusion tests.
- Current status: source identified and license terms checked against published repository description; assets have NOT been downloaded or bundled, and no acoustic piano quality claim is made.

Avoid Pianobook for bundled instrument libraries: its license permits use in music, but generally prohibits redistribution as sampler instruments.
