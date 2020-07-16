"""
A module storing strings used to populate the fields' help_text_ attributes.

.. _help_text:
   https://docs.djangoproject.com/en/3.0/ref/forms/fields/#help-text
"""

SCAN_COMMENTS = (
    "If anything noteworthy happened during acquisition, it may be noted here."
)
SCAN_DESCRIPTION = "A short description of the scan's acqusition parameters."
SCAN_ECHO_TIME = "The time between the application of the radio-frequency excitation pulse and the peak of the signal induced in the coil (in milliseconds)."
SCAN_INVERSION_TIME = "The time between the 180-degree inversion pulse and the following spin-echo (SE) sequence (in milliseconds)."
SCAN_NUMBER = (
    "The number of this scan relative to the session in which it was acquired."
)
SCAN_REPETITION_TIME = (
    "The time between two successive RF pulses (in milliseconds)."
)
SCAN_TIME = "The time in which the scan was acquired."


# flake8: noqa: E501
