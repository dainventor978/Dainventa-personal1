#pragma once
#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <string>

namespace trifusion {

struct AudioFeatures {
    float rms = 0.0f;
    float peak = 0.0f;
    float crest_factor = 0.0f;
    float zero_crossing_rate = 0.0f;
    bool valid = false;
};

// Deterministic, allocation-free block analysis. This is signal analysis,
// not a trained/neural classifier and does not modify the input.
class AudioAnalyzer {
public:
    static AudioFeatures analyze(const float* samples, std::size_t count) noexcept {
        AudioFeatures result;
        if (samples == nullptr || count == 0) return result;
        double sumSquares = 0.0;
        float peak = 0.0f;
        std::size_t crossings = 0;
        float previous = samples[0];
        if (!std::isfinite(previous)) return result;
        for (std::size_t i = 0; i < count; ++i) {
            const float x = samples[i];
            if (!std::isfinite(x)) return result;
            sumSquares += static_cast<double>(x) * x;
            peak = std::max(peak, std::abs(x));
            if (i > 0 && ((x >= 0.0f && previous < 0.0f) ||
                          (x < 0.0f && previous >= 0.0f))) ++crossings;
            previous = x;
        }
        result.rms = static_cast<float>(std::sqrt(sumSquares / count));
        result.peak = peak;
        result.crest_factor = result.rms > 1.0e-12f ? peak / result.rms : 0.0f;
        result.zero_crossing_rate = count > 1
            ? static_cast<float>(crossings) / static_cast<float>(count - 1) : 0.0f;
        result.valid = true;
        return result;
    }
};

enum class ControlKind : std::uint8_t { Analysis, PresetHint, Transport, Health };

struct CrossFusionMessage {
    std::uint32_t protocolVersion = 1;
    std::uint64_t sequence = 0;
    std::uint32_t sampleRate = 0;
    std::uint32_t blockSize = 0;
    std::uint32_t reportedLatencySamples = 0;
    ControlKind kind = ControlKind::Analysis;
    char sourceProduct[24] = {};
    char targetProduct[24] = {};

    bool valid() const noexcept {
        return protocolVersion == 1 && sequence > 0 &&
               sampleRate >= 8000 && sampleRate <= 384000 &&
               blockSize > 0 && blockSize <= 65536 &&
               sourceProduct[0] != '\0' && targetProduct[0] != '\0';
    }
};

// Advisory scheduler: returns a safe per-block work budget. It never changes
// audio quality or drops work by itself; the host/engine must honor the result.
struct ResourceBudget {
    float cpuFraction = 0.0f;
    std::uint32_t maxWorkUnits = 0;
    bool overloadRisk = false;
};

class ResourceGuardian {
public:
    static ResourceBudget budget(float measuredCpuFraction,
                                 float configuredLimit,
                                 std::uint32_t requestedWorkUnits) noexcept {
        ResourceBudget result;
        if (!std::isfinite(measuredCpuFraction) || !std::isfinite(configuredLimit) ||
            configuredLimit <= 0.0f || configuredLimit > 1.0f) {
            result.overloadRisk = true;
            return result;
        }
        const float measured = std::clamp(measuredCpuFraction, 0.0f, 1.0f);
        result.cpuFraction = measured;
        const float headroom = std::max(0.0f, configuredLimit - measured);
        result.overloadRisk = measured >= configuredLimit;
        if (requestedWorkUnits == 0 || result.overloadRisk) return result;
        const float availableRatio = std::clamp(headroom / configuredLimit, 0.0f, 1.0f);
        result.maxWorkUnits = static_cast<std::uint32_t>(
            std::floor(static_cast<float>(requestedWorkUnits) * availableRatio));
        return result;
    }
};

} // namespace trifusion
