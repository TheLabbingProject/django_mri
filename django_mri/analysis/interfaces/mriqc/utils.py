"""
Utilities for the :mod:`~django_mri.analysis.interfaces.mriqc` module.
"""

#: Command line template to format for execution.
COMMAND = "docker run --tmpfs /run --tmpfs /tmp --rm -it -v {bids_parent}:/data:ro -v {destination_parent}:/out nipreps/mriqc:{version} /data/{bids_name} /out/{destination_name} {analysis_level}"  # noqa: E501

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
