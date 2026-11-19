# OV comparison plugins — experimental rebuild

Four distinct JUCE plugins are configured: OV1, OV2, OV1TriFusion and OV2TriFusion. The two baseline processors use different static saturation curves. The two TriFusion-labeled test variants add a peak-shaping stage; this is **not** the full original TriFusion engine.

The macOS CI workflow is intended to produce an unsigned Intel macOS package with VST3 and Audio Unit bundles for all four. A committed workflow is not evidence of a passing build. No Mac build, installation, DAW compatibility or CPU comparison has been verified here.

## Build locally (developer reference)

```sh
cmake -S ov-rebuild -B build -G Xcode
cmake --build build --config Release
```

The source uses JUCE fetched from its public repository. Review JUCE licensing before distributing binaries commercially. For a meaningful comparison, use the same audio file, host buffer size, sample rate and settings, and measure both CPU use and audio output.
