"""
Definition of the :class:`fMRIPrepRunner` class.
"""
from typing import List

from django.db.models import Q, QuerySet
from django_analyses.runner.queryset_runner import QuerySetRunner

from django_mri.analysis.interfaces.fmriprep.fmriprep import FmriPrep2025
from django_mri.models.scan import Scan
from django_mri.utils.utils import get_subject_model

#: Associated subject model.
Subject = get_subject_model()


class fMRIPrepRunner(QuerySetRunner):
    """
    Automates the execution of fMRIPrep over a queryset of subjects.
    """

    #: :class:`~django_analyses.models.analysis.Analysis` instance title.
    ANALYSIS_TITLE = "fMRIPrep"

    #: :class:`~django_analyses.models.analysis_version.AnalysisVersion`
    #: instance title.
    ANALYSIS_VERSION_TITLE = FmriPrep2025.__version__

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

    #: Subject scan filtering to apply before running NIfTI conversion.
    SCAN_QUERY: Q = Q(_nifti__isnull=True) & ~(
        Q(description__icontains="IR-EPI")
        | Q(description__icontains="IREPI")
        | Q(description__icontains="localizer")
        | Q(description__icontains="cmrr")
    )

    def get_base_queryset(self) -> QuerySet:
        """
        Overrides
        :func:`~django_analyses.runner.queryset_runner.QuerySetRunner.get_base_queryset`
        to return only subjects with functional MRI data.

        Returns
        -------
        QuerySet
            Subjects with fMRI data
        """
        queryset = super().get_base_queryset()
        subject_ids = set(
            Scan.objects.filter_by_sequence_type("fMRI")
            .exclude(description__icontains="dmri")
            .values_list("session__subject", flat=True)
        )
        return queryset.filter(id__in=subject_ids)

    def get_instance_representation(self, instance: Subject) -> List[str]:
        """
        Returns the expected :attr:`INPUT_KEY` value for the given subject.

        Parameters
        ----------
        instance : Subject
            Subject instance

        Returns
        -------
        List[str]
            List containing subject ID string
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
        """
        scans = instance.mri_session_set.get_scan_set()
        for scan in scans.filter(self.SCAN_QUERY):
            bids_destination = scan.get_bids_destination()
            if bids_destination:
                try:
                    scan.nifti
                except RuntimeError:
                    pass
        return super().create_input_specification(instance)
