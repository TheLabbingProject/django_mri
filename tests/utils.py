import pydicom
from django_dicom.models import Image
from pathlib import Path


def restore_image_path(id: str, old_path: Path) -> None:
    img = Image.objects.get(uid=id)
    curr_path = Path(img.dcm.path)
    curr_path.rename(old_path / curr_path.name)
    img.dcm = str(old_path)


def restore_path(curr_path: str, old_path: str) -> None:
    for image in Path(curr_path).rglob("*.dcm"):
        str_path = str(image.absolute())  # Stringify the absolute path of the image
        id = pydicom.dcmread(str_path).get("SOPInstanceUID")
        restore_image_path(id, Path(old_path))
