import pydicom
from django_dicom.models import Image
from pathlib import Path


def restore_image_path(id: str, old_path: str) -> None:
    img = Image.objects.get(uid=id)
    curr_path = Path(img.dcm.path)
    curr_path.rename(old_path)
    img.dcm = str(old_path)


def restore_path(curr_path: str, old_path: str) -> None:
    for image in Path(curr_path).glob("*.dcm"):
        str_path = str(image)
        id = pydicom.dcmread(str_path).get("SOPInstanceUID")
        restore_image_path(id, str_path)
