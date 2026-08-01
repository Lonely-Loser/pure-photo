from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ImageInfo:
    """
    Information about the currently loaded image.
    """
    file_path: Path
    width: int
    height: int
    image_format: str
    file_size: int

    @property
    def file_name(self) -> str:
        return self.file_path.name

    @property
    def directory(self) -> str:
        return str(self.file_path.parent)