"""
A ChoiceEnum to represent SequenceVariant_ values.

.. _SequenceVariant: https://dicom.innolitics.com/ciods/mr-image/mr-image/00180021

"""

from dicom_parser.utils.choice_enum import ChoiceEnum


class SequenceVariant(ChoiceEnum):
    SK = "Segmented k-Space"
    MTC = "Magnetization Transfer Contrast"
    SS = "Steady State"
    TRSS = "Time Reversed Steady State"
    SP = "Spoiled"
    MP = "MAG Prepared"
    OSP = "Oversampling Phase"
    NONE = "None"
