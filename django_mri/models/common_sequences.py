"""
A list of common MRI sequences and their respective DICOM header attributes.

"""


sequences = [
    {
        "title": "MPRAGE",
        "description": "",
        "scanning_sequence": ["GR", "IR"],
        "sequence_variant": ["SK", "SP", "MP"],
    },
    {
        "title": "Localizer",
        "description": "",
        "scanning_sequence": ["GR"],
        "sequence_variant": ["SP", "OSP"],
    },
    {
        "title": "IR-EPI",
        "description": "",
        "scanning_sequence": ["EP", "IR"],
        "sequence_variant": ["SK", "SP", "MP", "OSP"],
    },
    {
        "title": "FLAIR",
        "description": "",
        "scanning_sequence": ["SE", "IR"],
        "sequence_variant": ["SK", "SP", "MP"],
    },
    {
        "title": "DWI",
        "description": "",
        "scanning_sequence": ["EP"],
        "sequence_variant": ["SK", "SP"],
    },
    {
        "title": "Resting-state fMRI",
        "description": "",
        "scanning_sequence": ["EP"],
        "sequence_variant": ["SK", "SS"],
    },
]
