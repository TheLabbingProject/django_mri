"""
Contains the provided output parser classes dictionary.
"""
from django_mri.analysis.parsers import MriqcOutputParser, ReconAllOutputParser

MRI_OUTPUT_PARSERS = {
    "ReconAll": ReconAllOutputParser,
    "MRIQC": MriqcOutputParser,
}
