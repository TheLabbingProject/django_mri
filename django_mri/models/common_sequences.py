"""
A list of common MRI sequences and their respective DICOM header attributes.

"""


sequences = [
    {
        "title": "MPRAGE",
        "description": "A T1-weighted 3D magnetization prepared-rapid acquisition gradient echo sequence. See https://pubs.rsna.org/doi/10.1148/radiology.182.3.1535892 for more information.",
        "scanning_sequence": ["GR", "IR"],
        "sequence_variant": ["SK", "SP", "MP"],
    },
    {
        "title": "Localizer",
        "description": "A set of three-plane, low-resolution, large field-of view scans that are obtained to be used for configuring the execution of subsequent scans.",
        "scanning_sequence": ["GR"],
        "sequence_variant": ["SP", "OSP"],
    },
    {
        "title": "IR-EPI",
        "description": "180° inversion pulse to prepare magnetization and then a RF excitation pulse which results in T1-weighting.",
        "scanning_sequence": ["EP", "IR"],
        "sequence_variant": ["SK", "SP", "MP", "OSP"],
    },
    {
        "title": "FLAIR",
        "description": "Fluid-attenuated inversion recovery is an MRI sequence with an inversion recovery set to null fluids. ",
        "scanning_sequence": ["SE", "IR"],
        "sequence_variant": ["SK", "SP", "MP"],
    },
    {
        "title": "DWI",
        "description": "Diffusion-weighted magnetic resonance imaging (DWI or DW-MRI) is the use of specific MRI sequences as well as software that generates images from the resulting data, that uses the diffusion of water molecules to generate contrast in MR images.",
        "scanning_sequence": ["EP"],
        "sequence_variant": ["SK", "SP"],
    },
    {
        "title": "fMRI",
        "description": "Functional magnetic resonance imaging or functional MRI (fMRI) measures brain activity by detecting changes associated with blood flow. This technique relies on the fact that cerebral blood flow and neuronal activation are coupled. When an area of the brain is in use, blood flow to that region also increases.",
        "scanning_sequence": ["EP"],
        "sequence_variant": ["SK", "SS"],
    },
]
