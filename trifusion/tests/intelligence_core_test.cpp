#include "IntelligenceCore.h"
#include <cassert>
#include <cmath>
#include <cstdint>
#include <limits>

int main() {
    const float signal[] = {0.0f, 0.5f, -0.5f, 0.5f, -0.5f};
    const auto features = trifusion::AudioAnalyzer::analyze(signal, 5);
    assert(features.valid);
    assert(features.peak == 0.5f);
    assert(features.rms > 0.0f);
    assert(features.zero_crossing_rate > 0.0f);

    const float bad[] = {0.0f, std::numeric_limits<float>::quiet_NaN()};
    assert(!trifusion::AudioAnalyzer::analyze(bad, 2).valid);
    assert(!trifusion::AudioAnalyzer::analyze(nullptr, 1).valid);

    trifusion::CrossFusionMessage message;
    message.sequence = 1;
    message.sampleRate = 48000;
    message.blockSize = 128;
    message.sourceProduct[0] = 'T';
    message.targetProduct[0] = 'Q';
    assert(message.valid());
    message.blockSize = 0;
    assert(!message.valid());

    const auto normal = trifusion::ResourceGuardian::budget(0.25f, 0.80f, 1000);
    assert(!normal.overloadRisk);
    assert(normal.maxWorkUnits > 0 && normal.maxWorkUnits <= 1000);
    const auto overloaded = trifusion::ResourceGuardian::budget(0.90f, 0.80f, 1000);
    assert(overloaded.overloadRisk && overloaded.maxWorkUnits == 0);
    const auto invalid = trifusion::ResourceGuardian::budget(0.2f, 0.0f, 1000);
    assert(invalid.overloadRisk);
    return 0;
}
