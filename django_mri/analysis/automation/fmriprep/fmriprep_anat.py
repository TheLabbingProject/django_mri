from django.db.models import QuerySet
from django_mri.analysis.automation.fmriprep.fmriprep import fMRIPrepRunner
from django_mri.models.scan import Scan


class fMRIPrepAnatRunner(fMRIPrepRunner):
    #: :class:`~django_analyses.models.pipeline.node.Node` instance
    #: configuration.
    ANALYSIS_CONFIGURATION = {
        "output-spaces": ["anat", "MNI152NLin2009cAsym"],
        "use-aroma": True,
        "anat-only": True,
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
        subject_ids = set(
            Scan.objects.filter_by_sequence_type("fMRI")
            .exclude(description__icontains="dmri")
            .values_list("session__subject", flat=True)
        )
        return queryset.exclude(id__in=subject_ids)
