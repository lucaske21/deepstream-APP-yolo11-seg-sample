#pragma once

#include <vector>

#include "nvdsinfer_custom_impl.h"

extern "C" bool NvDsInferParseCustomYolo11Seg(
    std::vector<NvDsInferLayerInfo> const& outputLayersInfo,
    NvDsInferNetworkInfo const& networkInfo,
    NvDsInferParseDetectionParams const& detectionParams,
    std::vector<NvDsInferInstanceMaskInfo>& objectList);

extern "C" bool NvDsInferInitializeInputLayers(std::vector<NvDsInferLayerInfo> const& inputLayersInfo);
