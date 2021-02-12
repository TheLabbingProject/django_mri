from pathlib import Path

import django_mri.utils.utils as utils
from django.conf import settings
from django.test import TestCase

from .models import Group, Subject


class UtilsTestCase(TestCase):
    def test_get_subject_model(self):
        result = utils.get_subject_model()
        self.assertEqual(result, Subject)

    def test_get_group_model(self):
        result = utils.get_group_model()
        self.assertEqual(result, Group)

    def test_get_mri_root(self):
        expected = Path(settings.MEDIA_ROOT, "MRI")
        result = utils.get_mri_root()
        self.assertEqual(result, expected)

    def test_get_dicom_root(self):
        expected = Path(settings.MEDIA_ROOT, "MRI", "DICOM")
        result = utils.get_dicom_root()
        self.assertEqual(result, expected)
