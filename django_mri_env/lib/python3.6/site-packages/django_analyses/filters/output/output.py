from django_analyses.models.output.output import Output
from django_filters import rest_framework as filters


class OutputFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.output.output.Output`
    model.
    
    """

    class Meta:
        model = Output
        fields = ("run",)

