"""
A module storing strings used to populate the fields' help_text_ attributes.

.. _help_text:
   https://docs.djangoproject.com/en/3.0/ref/forms/fields/#help-text
"""

SCAN_COMMENTS: str = (
    "If anything noteworthy happened during acquisition, it may be noted here."
)
SCAN_DESCRIPTION: str = "A short description of the scan's acqusition parameters."
SCAN_ECHO_TIME: str = "The time between the application of the radio-frequency excitation pulse and the peak of the signal induced in the coil (in milliseconds)."
SCAN_INVERSION_TIME: str = "The time between the 180-degree inversion pulse and the following spin-echo (SE) sequence (in milliseconds)."
SCAN_NUMBER: str = (
    "The number of this scan relative to the session in which it was acquired."
)
SCAN_REPETITION_TIME: str = "The time between two successive RF pulses (in milliseconds)."
SCAN_TIME: str = "The time in which the scan was acquired."

SESSION_COMMENTS: str = "General comments about MRI scanning session."

ATLAS_TITLE: str = "The title of this atlas."
ATLAS_DESCRIPTION: str = "A description of this atlas."
ATLAS_SYMMETRIC: str = "Whether this atlas is symmetric or not."

REGION_ATLAS: str = "The atlas in which the region is defined."
REGION_HEMISPHERE: str = "The hemisphere in which this region is defined."
REGION_TITLE: str = "A title describing this region."
REGION_INDEX: str = "The index of this region within the atlas."
REGION_DESCRIPTION: str = "A description of this region."
REGION_SUBCORTICAL: str = "Whether this region is subcortical or not."

SCORE_REGION: str = "The brain region for which this score was calculated."
SCORE_METRIC: str = "The metric represented by this score."
SCORE_VALUE: str = "Calculated score value."
SCORE_RUN: str = "The run from which this score was exrtacted."

METRIC_TITLE: str = "A title for this metric."
METRIC_DESCRIPTION: str = "A description of this metric's meaning and significance."


# flake8: noqa: E501
