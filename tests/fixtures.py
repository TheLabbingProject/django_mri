import os
import pytz

from datetime import datetime

# Find the path for the base tests directory
TESTS_DIR = os.path.dirname(os.path.realpath(__file__))

# Set the test files path
TEST_FILES_PATH = os.path.join(TESTS_DIR, "files")

# The name of the directory where imported files will be put
# (supposed to be deleted at the end of the tests execution)
IMPORTED_DIR = os.path.join(TESTS_DIR, "MRI")

#########
# DICOM #
#########

# Base DICOM data directory for tests
DICOM_FILES_PATH = os.path.join(TEST_FILES_PATH, "DICOM")

# Simple sample series (Siemens localizer)
DICOM_SERIES_PATH = os.path.join(DICOM_FILES_PATH, "Localizer")


# DWI
# ~~~
DICOM_DWI_PATH = os.path.join(DICOM_FILES_PATH, "DWI")

# Siemens
SIEMENS_DWI_SERIES_PATH = os.path.join(DICOM_DWI_PATH, "Siemens")
SIEMENS_DWI_SERIES = {
    "time": datetime(2018, 5, 1, 12, 37, 55, 433000, pytz.UTC),
    "description": "Ax1D_advdiff_d12D21_TE51_B1000",
    "number": 4,
    "echo_time": 51.0,
    "repetition_time": 2500.0,
    "spatial_resolution": [1.5, 1.5, 3.0],
    "subject_id": "304848286",
    "b_value": [
        0,
        0,
        0,
        0,
        0,
        15,
        25,
        40,
        60,
        80,
        100,
        130,
        160,
        195,
        230,
        270,
        315,
        360,
        410,
        460,
        520,
        580,
        640,
        705,
        775,
        845,
        920,
        1000,
    ],
    "b_vector": [
        [
            0.57735,
            0.57735,
            0.57735,
            -0.57735,
            -0.57735,
            4.14689e-08,
            4.14689e-08,
            4.14689e-08,
            4.14689e-08,
            4.14689e-08,
            4.14689e-08,
            4.14689e-08,
            4.14689e-08,
            -0.000176026,
            -0.00014847,
            -0.000126469,
            -0.000108742,
            -9.48424e-05,
            -8.32712e-05,
            -7.38943e-05,
            -6.59012e-05,
            -5.90562e-05,
            -5.33309e-05,
            -4.83417e-05,
            -4.4091e-05,
            -4.03349e-05,
            -3.70069e-05,
            -3.41171e-05,
        ],
        [
            0.57735,
            0.57735,
            0.57735,
            -0.57735,
            -0.57735,
            0.999504,
            0.999504,
            0.999504,
            0.999504,
            0.999504,
            0.999504,
            0.999504,
            0.999504,
            0.999653,
            0.999631,
            0.999613,
            0.999599,
            0.999587,
            0.999577,
            0.999569,
            0.999563,
            0.999557,
            0.999552,
            0.999547,
            0.999543,
            0.99954,
            0.999537,
            0.999535,
        ],
        [
            0.57735,
            0.57735,
            0.57735,
            -0.57735,
            -0.57735,
            0.0315058,
            0.0315058,
            0.0315058,
            0.0315058,
            0.0315058,
            0.0315058,
            0.0315058,
            0.0315058,
            0.0263565,
            0.0271625,
            0.027806,
            0.0283244,
            0.028731,
            0.0290694,
            0.0293436,
            0.0295774,
            0.0297775,
            0.029945,
            0.0300909,
            0.0302152,
            0.0303251,
            0.0304224,
            0.0305069,
        ],
    ],
}
