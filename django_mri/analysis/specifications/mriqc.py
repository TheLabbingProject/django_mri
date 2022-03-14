"""
Input and output specification dictionaries for MRIQC's interface.
"""
from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    DirectoryInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import ListOutputDefinition

#: *mriqc* input specification.
MRIQC_INPUT_SPECIFICATION = {
    "destination": {
        "type": StringInputDefinition,
        "dynamic_default": "{run_id}",
        "required": True,
        "description": "The directory where the output files should be stored. If you are running group level analysis this folder should be prepopulated with the results of the participant level analysis.",
    },
    "analysis_level": {
        "type": StringInputDefinition,
        "choices": ["participant", "group"],
        "required": False,
        "default": "participant",
        "description": "Level of the analysis that will be performed. Multiple participant level analyses can be run independently (in parallel) using the same output_dir.",
    },
    "participant_label": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "required": True,
        "description": "a space delimited list of participant identifiers or a single identifier (the sub- prefix can be removed)",  # noqa: E501
        "is_configuration": False,
    },
    "task-id": {
        "type": StringInputDefinition,
        "description": "Filter input dataset by task ID.",
    },
    "session-id": {
        "type": StringInputDefinition,
        "description": "Filter input dataset by session ID.",
    },
    "run-id": {
        "type": StringInputDefinition,
        "description": "Filter input dataset by run ID.",
    },
    "modalities": {
        "type": StringInputDefinition,
        "description": "Filter input dataset by MRI type.",
    },
    "dsname": {
        "type": StringInputDefinition,
        "description": "A dataset name.",
    },
    "nprocs": {
        "type": IntegerInputDefinition,
        "description": "Maximum number of threads across all processes.",
    },
    "omp-nthreads": {
        "type": IntegerInputDefinition,
        "description": "Maximum number of threads per-process.",
    },
    "mem": {
        "type": IntegerInputDefinition,
        "description": "Upper bound memory limit for MRIQC processes.",
    },
    "testing": {
        "type": BooleanInputDefinition,
        "description": "Use testing settings for a minimal footprint.",
    },
    "profile": {
        "type": BooleanInputDefinition,
        "description": "Hook up the resource profiler callback to nipype.",
    },
    "float32": {
        "type": BooleanInputDefinition,
        "description": "Cast the input data to float32 if it’s represented in higher precision (saves space and improves perfomance).",
    },
    "verbose-reports": {"type": BooleanInputDefinition, "description": "",},
    "write-graph": {
        "type": BooleanInputDefinition,
        "description": "Write workflow graph.",
    },
    "dry-run": {
        "type": BooleanInputDefinition,
        "description": "Do not run the workflow.",
    },
    "no-sub": {
        "type": BooleanInputDefinition,
        "description": "Turn off submission of anonymized quality metrics to MRIQC’s metrics repository.",
        "default": True,
    },
    "ants-float": {
        "type": BooleanInputDefinition,
        "description": "Use float number precision on ANTs computations.",
    },
    "fft-spikes-detector": {
        "type": BooleanInputDefinition,
        "description": "Turn on FFT based spike detector (slow).",
    },
    "fd_thres": {
        "type": FloatInputDefinition,
        "description": "Threshold on framewise displacement estimates to detect outliers.",
    },
    "deoblique": {
        "type": BooleanInputDefinition,
        "description": "Deoblique the functional scans during head motion correction preprocessing.",
    },
    "despike": {
        "type": BooleanInputDefinition,
        "description": "Despike the functional scans during head motion correction preprocessing.",
    },
    "start-idx": {
        "type": IntegerInputDefinition,
        "description": "Initial volume in functional timeseries that should be considered for preprocessing.",
    },
    "stop-idx": {
        "type": IntegerInputDefinition,
        "description": "Final volume in functional timeseries that should be considered for preprocessing.",
    },
    "correct-slice-timing": {
        "type": BooleanInputDefinition,
        "description": "Perform slice timing correction.",
    },
    "use-plugin": {
        "type": FileInputDefinition,
        "description": "nipype plugin configuration file.",
    },
    "work-dir": {
        "type": DirectoryInputDefinition,
        "description": "Path where intermediate results should be stored.",
        "default": "/out/work",
    },
}
#: *MRIQC* output specification.
MRIQC_OUTPUT_SPECIFICATION = {
    "scores": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "JSON files (one for each anatomical scan) containing the calculated QC metrics.",
    },
    "reports": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "HTML files (one for each anatomical scan) containing detailed visual reports.",
    },
    "logs": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Run logs.",
    },
}


# flake8: noqa: E501
