"""
Definition of the :class:`AnatomicalPreprocessing` base class.
"""
import logging

from django.db.models import Q, QuerySet
from django_analyses.runner.queryset_runner import QuerySetRunner
from django_mri.utils.utils import get_subject_model
from django_mri.analysis.interfaces.fmriprep.fmriprep import fMRIprep

Subject = get_subject_model()


class fMRIPrepRunner(QuerySetRunner):
    """
    Base class for anatomical MRI preprocessing over a queryset of
    :class:`~django_mri.models.scan.Scan` instances. If no queryset is
    provided, call the :func:`get_default_queryset` method to generate a
    default execution queryset.
    """

    #: :class:`~django_analyses.models.analysis.Analysis` instance title.
    ANALYSIS_TITLE = "fMRIPrep"

    #: :class:`~django_analyses.models.analysis_version.AnalysisVersion`
    #: instance title.
    ANALYSIS_VERSION_TITLE = fMRIprep.__version__

    #: :class:`~django_analyses.models.pipeline.node.Node` instance
    #: configuration.
    ANALYSIS_CONFIGURATION = {
        "output-spaces": ["anat", "MNI152NLin2009cAsym"],
        "use-aroma": True,
    }

    #: Input definition key.
    INPUT_KEY = "participant_label"

    #: The database model for scans (the base input class).
    DATA_MODEL = Subject

    #: Customize input preprocessing progressbar text.
    INPUT_GENERATION_PROGRESSBAR_KWARGS = {
        "unit": "subject",
        "desc": "Converting MRI scans to NIfTI",
    }

    def get_instance_representation(self, instance: Subject) -> str:
        """
        The most common input format for anatomical preprocessing scripts is
        NIfTI, so by default this method returns the path of the scan
        instance's NIfTI-format file.

        Parameters
        ----------
        instance : Scan
            Scan instance

        Returns
        -------
        str
            Path of the scan's NIfTI-format file
        """
        return [str(instance.id)]

    def create_input_specification(self, instance: Subject) -> dict:
        """
        Returns an input specification dictionary with the given data
        *instance* as input.

        Parameters
        ----------
        instance : Model
            Data instance to be processed

        Returns
        -------
        dict
            Input specification dictionary

        See Also
        --------
        :func:`create_inputs`
        """
        q = Q(_nifti__isnull=True) & ~(
            Q(description__icontains="IR-EPI")
            | Q(description__icontains="IREPI")
            | Q(description__icontains="localizer")
            | Q(description__icontains="cmrr")
        )
        scans = instance.mri_session_set.get_scan_set()
        for scan in scans.filter(q):
            bids_destination = scan.get_bids_destination()
            if bids_destination:
                print(scan.description)
                print(instance.id)
                try:
                    scan.nifti
                except RuntimeError:
                    pass
        return super().create_input_specification(instance)
