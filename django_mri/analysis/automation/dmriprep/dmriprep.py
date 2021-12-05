"""
Definition of the :class:`fMRIPrepRunner` class.
"""
from typing import List

from django.db.models import Q, QuerySet
from django_analyses.runner.queryset_runner import QuerySetRunner
from django_mri.analysis.interfaces.dmriprep.dmriprep import DmriPrep010
from django_mri.utils.utils import get_subject_model

#: Associated subject model.
Subject = get_subject_model()


class dMRIPrepRunner(QuerySetRunner):
    """
    Automates the execution of dMRIPrep over a queryset of subjects.
    """

    #: :class:`~django_analyses.models.analysis.Analysis` instance title.
    ANALYSIS_TITLE = "dMRIPrep"

    #: :class:`~django_analyses.models.analysis_version.AnalysisVersion`
    #: instance title.
    ANALYSIS_VERSION_TITLE = DmriPrep010.__version__

    #: :class:`~django_analyses.models.pipeline.node.Node` instance

    #: Input definition key.
    INPUT_KEY = "participant_label"

    #: The database model for scans (the base input class).
    DATA_MODEL = Subject

    #: Customize input preprocessing progressbar text.
    INPUT_GENERATION_PROGRESSBAR_KWARGS = {
        "unit": "subject",
        "desc": "Converting MRI scans to NIfTI",
    }

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
        q = (
            Q(mri_session_set__scan__dicom__sequence_type="dwi")
            and Q(mri_session_set__scan__dicom__sequence_type="mprage")
            and Q(mri_session_set__scan__dicom__sequence_type="dwi_fieldmap")
        )
        return queryset.filter(q)

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
