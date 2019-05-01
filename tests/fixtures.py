import os
import pytz

from datetime import datetime


TEST_SCAN_FIELDS = {
    "time": datetime(2018, 5, 1, 12, 37, 55, 433000, pytz.UTC),
    "description": "Ax1D_advdiff_d12D21_TE51_B1000",
    "number": 4,
    "echo_time": 51.0,
    "repetition_time": 2500.0,
    "spatial_resolution": [1.5, 1.5, 3],
    "subject_id": "304848286",
}

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_FILES_PATH = os.path.join(TESTS_DIR, "files")
DICOM_IMAGE_PATH = os.path.join(TEST_FILES_PATH, "test.dcm")
IMPORTED_DIR = os.path.join(TESTS_DIR, "MRI")
