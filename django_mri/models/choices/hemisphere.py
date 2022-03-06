"""
Definition of the :class:`Hemisphere` choice Enum.
"""
from dicom_parser.utils.choice_enum import ChoiceEnum


class Hemisphere(ChoiceEnum):
    L = "Left"
    R = "Right"
