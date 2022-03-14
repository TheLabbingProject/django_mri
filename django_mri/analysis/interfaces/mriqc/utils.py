"""
Utilities for the :mod:`~django_mri.analysis.interfaces.mriqc` module.
"""

#: Command line template to format for execution.
COMMAND = "singularity run -e -B {bids_parent}:/data:ro,{destination_parent}:/out:rw {singularity_image_root}/mriqc-{version}.simg /data/{bids_name} /out/{destination_name} {analysis_level}"  # noqa: E501

#: "Flags" indicate parameters that are specified without any arguments, i.e.
#: they are a switch for some binary configuration.
FLAGS = (
    "testing",
    "float32",
    "verbose-reports",
    "write-graph",
    "dry-run",
    "profile",
    "no-sub",
    "ants-float",
    "fft-spikes-detector",
    "deoblique",
    "despike",
    "correct-slice-timing",
)
