"""
Definition of the :class:`AnatomicalPreprocessing` base class.
"""
import logging
from typing import Tuple

from django.db.models import Q, QuerySet
from django_analyses.runner.queryset_runner import QuerySetRunner
from django_mri.analysis.automation.anatomical import messages
from django_mri.models.scan import Scan

#: Anatomical sequences to be in included in the input queryset.
ANATOMICAL_SEQUENCES: Tuple[str] = ("mprage", "spgr")
#: Joined MPRAGE and SPGR query.
DICOM_ANATOMICAL_QUERY = Q(dicom__sequence_type__in=ANATOMICAL_SEQUENCES)


class AnatomicalPreprocessing(QuerySetRunner):
    """
    Base class for anatomical MRI preprocessing over a queryset of
    :class:`~django_mri.models.scan.Scan` instances. If no queryset is
    provided, call the :func:`get_default_queryset` method to generate a
    default execution queryset.
    """

    #: The database model for scans (the base input class).
    DATA_MODEL = Scan

    #: Override
    #: :attr:`~django_analyses.runner.queryset_runner.QuerysetRunner.
    #: FILTER_QUERYSET_START` to log a more informative message.
    FILTER_QUERYSET_START = messages.FILTER_QUERYSET_START

    #: Override
    #: :attr:`~django_analyses.runner.queryset_runner.QuerysetRunner.
    #: NO_CANDIDATES` to log a more informative warning.
    NO_CANDIDATES = messages.NO_T1_WEIGHTED

    #: Customize input preprocessing progressbar text.
    INPUT_GENERATION_PROGRESSBAR_KWARGS = {
        "unit": "scan",
        "desc": "Preparing NIfTI file inputs",
    }

    def filter_queryset(
        self, queryset: QuerySet, log_level: int = logging.INFO
    ) -> QuerySet:
        """
        Returns a queryset of exclusively T1-weighted scans.

        Parameters
        ----------
        queryset : QuerySet
            All scan instances
        log_level : int, optional
            Logging level to use, by default 20 (INFO)

        Returns
        -------
        QuerySet
            T1-weighted scans
        """
        queryset = super().filter_queryset(queryset, log_level)
        self.log_filter_start(log_level)
        dicom_candidates = list(
            queryset.filter(DICOM_ANATOMICAL_QUERY).values_list(
                "id", flat=True
            )
        )
        nifti_candidates = [
            scan.id
            for scan in queryset.filter(
                dicom__isnull=True, _nifti__isnull=False
            )
            if scan.sequence_type in ANATOMICAL_SEQUENCES
        ]
        candidate_ids = dicom_candidates + nifti_candidates
        queryset = queryset.filter(id__in=candidate_ids).order_by("-time")
        self.log_filter_end(n_candidates=queryset.count(), log_level=log_level)
        return queryset

    def get_instance_representation(self, instance: Scan) -> str:
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
        return str(instance.nifti.path)

    def has_run(self, instance: Scan) -> bool:
        """
        In order to prevent NIfTI generation when checking for existing runs,
        this method is overriden to first check if the scan's
        :class:`~django_mri.models.scan.Scan._nifti` field is populated.

        Parameters
        ----------
        instance : Scan
            Anatomical scan to query an existing run for

        Returns
        -------
        bool
            Whether the provided scan has an existing run or not
        """
        if instance._nifti:
            value = self.get_instance_representation(instance)
            return self.input_set.filter(value=value).exists()
        return False
