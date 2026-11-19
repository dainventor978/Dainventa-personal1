#include <juce_audio_processors/juce_audio_processors.h>
#include <juce_gui_extra/juce_gui_extra.h>
#include <cmath>
class OVProcessor final : public juce::AudioProcessor {
public:
  OVProcessor() : juce::AudioProcessor(BusesProperties().withInput("Input",juce::AudioChannelSet::stereo(),true).withOutput("Output",juce::AudioChannelSet::stereo(),true)),
    state(*this,nullptr,"Parameters",makeLayout()) {}
  static juce::AudioProcessorValueTreeState::ParameterLayout makeLayout() {
    std::vector<std::unique_ptr<juce::RangedAudioParameter>> p;
    p.push_back(std::make_unique<juce::AudioParameterFloat>("drive","Drive",juce::NormalisableRange<float>(0.f,24.f,0.01f),6.f));
    p.push_back(std::make_unique<juce::AudioParameterFloat>("mix","Mix",juce::NormalisableRange<float>(0.f,1.f,0.001f),1.f));
    p.push_back(std::make_unique<juce::AudioParameterFloat>("output","Output",juce::NormalisableRange<float>(-24.f,12.f,0.01f),0.f));
    return {p.begin(),p.end()};
  }
  const juce::String getName() const override {
#if defined(OV_PRODUCT_OV1)
    return "OV1";
#else
    return "OV2";
#endif
  }
  void prepareToPlay(double,int) override {}
  void releaseResources() override {}
  bool isBusesLayoutSupported(const BusesLayout& l) const override {
    return l.getMainInputChannelSet()==juce::AudioChannelSet::stereo() && l.getMainOutputChannelSet()==juce::AudioChannelSet::stereo();
  }
  void processBlock(juce::AudioBuffer<float>& b,juce::MidiBuffer&) override {
    juce::ScopedNoDenormals noDenormals;
    const float drive=juce::Decibels::decibelsToGain(state.getRawParameterValue("drive")->load());
    const float output=juce::Decibels::decibelsToGain(state.getRawParameterValue("output")->load());
    const float mix=state.getRawParameterValue("mix")->load();
    const float normalizer=1.f/std::tanh(drive);
    for(int c=0;c<b.getNumChannels();++c) {
      auto* samples=b.getWritePointer(c);
      for(int i=0;i<b.getNumSamples();++i) {
        const float dry=samples[i];
#if defined(OV_PRODUCT_OV1)
        const float wet=std::tanh(dry*drive)*normalizer;
#else
        const float wet=std::atan(dry*drive)*(2.f/juce::MathConstants<float>::pi);
#endif
        samples[i]=output*(dry+(wet-dry)*mix);
      }
    }
  }
  juce::AudioProcessorEditor* createEditor() override {return new juce::GenericAudioProcessorEditor(*this);}
  bool hasEditor() const override {return true;}
  double getTailLengthSeconds() const override {return 0;}
  bool acceptsMidi() const override {return false;}
  bool producesMidi() const override {return false;}
  bool isMidiEffect() const override {return false;}
  int getNumPrograms() override {return 1;}
  int getCurrentProgram() override {return 0;}
  void setCurrentProgram(int) override {}
  const juce::String getProgramName(int) override {return {};}
  void changeProgramName(int,const juce::String&) override {}
  void getStateInformation(juce::MemoryBlock& dest) override {
    auto xml=state.copyState().createXml();
    copyXmlToBinary(*xml,dest);
  }
  void setStateInformation(const void* data,int size) override {
    std::unique_ptr<juce::XmlElement> xml(getXmlFromBinary(data,size));
    if(xml && xml->hasTagName(state.state.getType())) state.replaceState(juce::ValueTree::fromXml(*xml));
  }
private:
  juce::AudioProcessorValueTreeState state;
};
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter(){return new OVProcessor();}
