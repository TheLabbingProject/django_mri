"""
Messages for the
:class:`~django_mri.analysis.interfaces.fmriprep.fmriprep.FmriPrep` interface.
"""

#: FreeSurfer license could not be found.
FS_LICENSE_MISSING: str = "FreeSurfer license file could not be found!\nPlease either provide the 'fs-license-file' argument to the interface, or make sure $FREESURFER_HOME is set and the license is found within it."

#: Run failure.
RUN_FAILURE: str = "Failed to run fmriprep!\nExecuted command:\t{command}\nRaised exception:\t{exception}"

# flake8: noqa: E501
