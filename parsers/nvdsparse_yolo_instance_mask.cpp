#include "nvdsparse_yolo_instance_mask.h"

#include <algorithm>
#include <cmath>
#include <cstring>
#include <stdexcept>
#include <string>

namespace {

struct Candidate {
  int class_id{0};
  float score{0.0F};
  float left{0.0F};
  float top{0.0F};
  float width{0.0F};
  float height{0.0F};
  std::vector<float> mask_coeffs;
};

float Sigmoid(float x) {
  return 1.0F / (1.0F + std::exp(-x));
}

float IoU(const Candidate& a, const Candidate& b) {
  const float ax2 = a.left + a.width;
  const float ay2 = a.top + a.height;
  const float bx2 = b.left + b.width;
  const float by2 = b.top + b.height;

  const float x1 = std::max(a.left, b.left);
  const float y1 = std::max(a.top, b.top);
  const float x2 = std::min(ax2, bx2);
  const float y2 = std::min(ay2, by2);

  const float inter_w = std::max(0.0F, x2 - x1);
  const float inter_h = std::max(0.0F, y2 - y1);
  const float inter = inter_w * inter_h;

  const float union_area = a.width * a.height + b.width * b.height - inter;
  return union_area > 0.0F ? (inter / union_area) : 0.0F;
}

void ApplyNms(std::vector<Candidate>& candidates, float iou_threshold) {
  std::sort(candidates.begin(), candidates.end(), [](const Candidate& lhs, const Candidate& rhs) {
    return lhs.score > rhs.score;
  });

  std::vector<bool> keep(candidates.size(), true);
  for (size_t i = 0; i < candidates.size(); ++i) {
    if (!keep[i]) {
      continue;
    }
    for (size_t j = i + 1; j < candidates.size(); ++j) {
      if (!keep[j]) {
        continue;
      }
      if (candidates[i].class_id == candidates[j].class_id && IoU(candidates[i], candidates[j]) > iou_threshold) {
        keep[j] = false;
      }
    }
  }

  std::vector<Candidate> filtered;
  filtered.reserve(candidates.size());
  for (size_t i = 0; i < candidates.size(); ++i) {
    if (keep[i]) {
      filtered.push_back(std::move(candidates[i]));
    }
  }
  candidates.swap(filtered);
}

std::vector<uint8_t> DecodeMask(
    const Candidate& candidate,
    const float* proto_data,
    int proto_c,
    int proto_h,
    int proto_w,
    float threshold = 0.5F) {
  std::vector<uint8_t> mask(static_cast<size_t>(proto_h) * static_cast<size_t>(proto_w), 0U);
  if (candidate.mask_coeffs.empty() || proto_data == nullptr) {
    return mask;
  }

  for (int y = 0; y < proto_h; ++y) {
    for (int x = 0; x < proto_w; ++x) {
      float value = 0.0F;
      const int index = y * proto_w + x;
      for (int c = 0; c < proto_c && c < static_cast<int>(candidate.mask_coeffs.size()); ++c) {
        value += candidate.mask_coeffs[static_cast<size_t>(c)] * proto_data[c * proto_h * proto_w + index];
      }
      mask[static_cast<size_t>(index)] = Sigmoid(value) > threshold ? 255U : 0U;
    }
  }
  return mask;
}

}  // namespace

extern "C" bool NvDsInferInitializeInputLayers(std::vector<NvDsInferLayerInfo> const&) {
  return true;
}

extern "C" bool NvDsInferParseCustomYolo11Seg(
    std::vector<NvDsInferLayerInfo> const& outputLayersInfo,
    NvDsInferNetworkInfo const& networkInfo,
    NvDsInferParseDetectionParams const& detectionParams,
    std::vector<NvDsInferInstanceMaskInfo>& objectList) {
  if (outputLayersInfo.size() < 2U) {
    return false;
  }

  const auto* det_data = reinterpret_cast<const float*>(outputLayersInfo[0].buffer);
  const auto* proto_data = reinterpret_cast<const float*>(outputLayersInfo[1].buffer);
  if (det_data == nullptr || proto_data == nullptr) {
    return false;
  }

  const auto& det_dims = outputLayersInfo[0].inferDims;
  const auto& proto_dims = outputLayersInfo[1].inferDims;
  if (det_dims.numDims < 2 || proto_dims.numDims < 3) {
    return false;
  }

  const int num_candidates = det_dims.d[0];
  const int values_per_candidate = det_dims.d[1];
  const int num_classes = static_cast<int>(detectionParams.numClassesConfigured);
  const int mask_coeff_offset = 4 + num_classes;

  const int proto_c = proto_dims.d[0];
  const int proto_h = proto_dims.d[1];
  const int proto_w = proto_dims.d[2];

  std::vector<Candidate> candidates;
  candidates.reserve(static_cast<size_t>(num_candidates));

  for (int i = 0; i < num_candidates; ++i) {
    const float* row = det_data + static_cast<size_t>(i) * static_cast<size_t>(values_per_candidate);
    const float cx = row[0];
    const float cy = row[1];
    const float w = row[2];
    const float h = row[3];

    int best_class = -1;
    float best_score = 0.0F;
    for (int cls = 0; cls < num_classes; ++cls) {
      if (row[4 + cls] > best_score) {
        best_score = row[4 + cls];
        best_class = cls;
      }
    }

    if (best_class < 0) {
      continue;
    }
    const float threshold = detectionParams.perClassPreclusterThreshold[best_class];
    if (best_score < threshold) {
      continue;
    }

    Candidate candidate;
    candidate.class_id = best_class;
    candidate.score = best_score;
    candidate.left = (cx - w * 0.5F) * static_cast<float>(networkInfo.width);
    candidate.top = (cy - h * 0.5F) * static_cast<float>(networkInfo.height);
    candidate.width = w * static_cast<float>(networkInfo.width);
    candidate.height = h * static_cast<float>(networkInfo.height);

    for (int m = mask_coeff_offset; m < values_per_candidate; ++m) {
      candidate.mask_coeffs.push_back(row[m]);
    }

    candidates.push_back(std::move(candidate));
  }

  ApplyNms(candidates, 0.5F);

  for (const auto& candidate : candidates) {
    NvDsInferInstanceMaskInfo info{};
    info.classId = candidate.class_id;
    info.detectionConfidence = candidate.score;
    info.left = candidate.left;
    info.top = candidate.top;
    info.width = candidate.width;
    info.height = candidate.height;

    const auto mask = DecodeMask(candidate, proto_data, proto_c, proto_h, proto_w);
    info.mask_width = proto_w;
    info.mask_height = proto_h;
    info.mask_size = static_cast<unsigned int>(mask.size());
    // DeepStream frees `mask` when NvDsInferInstanceMaskInfo is released downstream.
    info.mask = static_cast<uint8_t*>(std::malloc(mask.size()));

    if (info.mask != nullptr) {
      std::memcpy(info.mask, mask.data(), mask.size());
      objectList.push_back(info);
    }
  }

  return true;
}
