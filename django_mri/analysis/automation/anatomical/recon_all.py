"""
Definition of the :class:`ReconAllRunner` class.
"""
from typing import List

from django_mri.analysis.automation.anatomical.preprocessing import (
    AnatomicalPreprocessing,
)
from django_mri.models.scan import Scan
from nipype.interfaces.freesurfer import ReconAll


class ReconAllRunner(AnatomicalPreprocessing):
    """
    Automate ReconAll execution over a provided queryset of
    :class:`~django_mri.models.scan.Scan` instances.
    """

    #: :class:`~django_analyses.models.analysis.Analysis` instance title.
    ANALYSIS_TITLE = "ReconAll"

    #: :class:`~django_analyses.models.analysis_version.AnalysisVersion`
    #: instance title.
    ANALYSIS_VERSION_TITLE = ReconAll().version

    #: :class:`~django_analyses.models.pipeline.node.Node` instance
    #: configuration.
    ANALYSIS_CONFIGURATION = {}

    #: Input definition key.
    INPUT_KEY = "T1_files"

    def get_instance_representation(self, instance: Scan) -> List[str]:
        """
        ReconAll expects a list of T1-weighted scans.

        Parameters
        ----------
        instance : Scan
            Scan to create the input representation for

        Returns
        -------
        List[str]
            A list containing the provided scan's path
        """
        nii_path = super().get_instance_representation(instance)
        return [nii_path]
