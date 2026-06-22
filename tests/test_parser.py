import unittest
from pathlib import Path


class ParserFilesTest(unittest.TestCase):
    def test_parser_exports_expected_symbols(self) -> None:
        parser_file = Path("parsers/nvdsparse_yolo_instance_mask.cpp")
        content = parser_file.read_text(encoding="utf-8")

        self.assertIn("NvDsInferParseCustomYolo11Seg", content)
        self.assertIn("NvDsInferInstanceMaskInfo", content)
        self.assertIn("ApplyNms", content)
        self.assertIn("DecodeMask", content)


if __name__ == "__main__":
    unittest.main()
