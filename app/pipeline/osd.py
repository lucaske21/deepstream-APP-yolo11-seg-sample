"""OSD service abstraction for bounding boxes, labels, confidence, and masks."""


class OsdService:
    """Represents nvdsosd overlay stage."""

    def describe(self) -> str:
        return (
            "post_osd: nvdsosd(bbox=true,label=true,confidence=true,"
            "mask=true,alpha=0.4,class_colors=distinct)"
        )

    def gst_elements(self) -> list[str]:
        return ["nvdsosd"]
