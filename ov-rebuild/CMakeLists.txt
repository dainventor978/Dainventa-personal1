cmake_minimum_required(VERSION 3.22)
project(OVPlugins VERSION 0.1.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
include(FetchContent)
FetchContent_Declare(JUCE GIT_REPOSITORY https://github.com/juce-framework/JUCE.git GIT_TAG 8.0.10 GIT_SHALLOW TRUE)
FetchContent_MakeAvailable(JUCE)
foreach(PRODUCT IN ITEMS OV1 OV2 TriFusion)
  juce_add_plugin(${PRODUCT}
    COMPANY_NAME "Sound Head Developments"
    BUNDLE_ID "com.soundhead.${PRODUCT}"
    PLUGIN_MANUFACTURER_CODE ShDv
    PLUGIN_CODE ${PRODUCT}A
    FORMATS VST3 AU
    PRODUCT_NAME "${PRODUCT}"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    COPY_PLUGIN_AFTER_BUILD FALSE)
  target_sources(${PRODUCT} PRIVATE PluginProcessor.cpp)
  target_compile_definitions(${PRODUCT} PRIVATE JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0 OV_PRODUCT_${PRODUCT}=1)
  target_link_libraries(${PRODUCT} PRIVATE juce::juce_audio_utils juce::juce_dsp juce::juce_recommended_config_flags juce::juce_recommended_warning_flags)
endforeach()
