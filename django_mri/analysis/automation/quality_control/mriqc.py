"""
Definition of the :class:`MriqcRunner` class.
"""
from typing import List

from django.db.models import Q, QuerySet
from django_analyses.runner.queryset_runner import QuerySetRunner
from django_mri.analysis.interfaces.mriqc.mriqc import MRIQC2100rc2
from django_mri.utils.utils import get_subject_model

#: Associated subject model.
Subject = get_subject_model()


class MriqcRunner(QuerySetRunner):
    """
    Automates the execution of Mriqc over a queryset of subjects.
    """

    #: :class:`~django_analyses.models.analysis.Analysis` instance title.
    ANALYSIS_TITLE = "MRIQC"

    #: :class:`~django_analyses.models.analysis_version.AnalysisVersion`
    #: instance title.
    ANALYSIS_VERSION_TITLE = MRIQC2100rc2.__version__

    #: :class:`~django_analyses.models.pipeline.node.Node` instance
    #: configuration.
    ANALYSIS_CONFIGURATION = {
        "no-sub": True,
        "float32": True,
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
    SCAN_QUERY: Q = Q(_nifti__isnull=True) & (Q(dicom__sequence_type="mprage") | Q(dicom__sequence_type="flair") | Q(dicom__sequence_type="t2w") | Q(dicom__sequence_type="bold"))

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
        return queryset.filter(
            mri_session_set__scan__dicom__sequence_type__in=("mprage", "t2w")
        ).distinct()

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
        scans.filter(self.SCAN_QUERY).convert_to_nifti(
            force=False, persistent=True, progressbar=False
        )
        return super().create_input_specification(instance)
