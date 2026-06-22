import unittest

from app.main import build_service
from app.pipeline.sink import SinkConfig, SinkService
from app.probes.osd_probe import summarize_object_meta


class PipelineConfigTest(unittest.TestCase):
    def test_build_service_loads_all_components(self) -> None:
        chain = build_service("configs/pipeline.yaml")
        self.assertEqual(5, len(chain))
        descriptions = [component.describe() for component in chain]
        self.assertTrue(descriptions[0].startswith("pre_source(rtsp)"))
        self.assertIn("inf_segment", descriptions[1])
        self.assertIn("post_tracker", descriptions[2])
        self.assertIn("post_osd", descriptions[3])
        self.assertIn("post_sink(rtsp)", descriptions[4])

    def test_osd_probe_summary(self) -> None:
        text = summarize_object_meta({"label": "person", "confidence": 0.93, "has_mask": True})
        self.assertEqual("label=person confidence=0.93 mask=True", text)

    def test_sink_selects_h265_payloader(self) -> None:
        sink = SinkService(SinkConfig(rtsp_port=8554, mount_path="/output", codec="h265", bitrate=4_000_000))
        self.assertEqual(["nvv4l2h265enc", "rtph265pay", "gst-rtsp-server"], sink.gst_elements())


if __name__ == "__main__":
    unittest.main()
