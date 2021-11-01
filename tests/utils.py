from pathlib import Path

import pydicom
from django.db import models
from django_dicom.models import Image


def restore_image_path(id: str, old_path: Path) -> None:
    img = Image.objects.get(uid=id)
    curr_path = Path(img.dcm.path)
    curr_path.rename(old_path / curr_path.name)
    img.dcm = str(old_path)


def restore_path(curr_path: str, old_path: str) -> None:
    for image in Path(curr_path).rglob("*.dcm"):
        str_path = str(
            image.absolute()
        )  # Stringify the absolute path of the image
        id = pydicom.dcmread(str_path).get("SOPInstanceUID")
        restore_image_path(id, Path(old_path))


class CharNullField(models.CharField):
    """
    Subclass of the CharField that allows empty strings to be stored as NULL.
    """

    description = "CharField that stores NULL but returns ''."

    def from_db_value(self, value, expression, connection):
        """
        Gets value right out of the db and changes it if its ``None``.
        """
        if value is None:
            return ""
        else:
            return value

    def to_python(self, value):
        """
        Gets value right out of the db or an instance, and changes it if its
        `None`.
        """
        if isinstance(value, models.CharField):
            # If an instance, just return the instance.
            return value
        if value is None:
            # If db has NULL, convert it to ''.
            return ""

        # Otherwise, just return the value.
        return value

    def get_prep_value(self, value):
        """
        Catches value right before sending to db.
        """
        if value == "":
            # If Django tries to save an empty string, send the db None (NULL).
            return None
        else:
            # Otherwise, just pass the value.
            return value
