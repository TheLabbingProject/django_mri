from django_analyses.models.pipeline.pipe import Pipe
from django_filters import rest_framework as filters


class PipeFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.pipeline.pipe.Pipe`
    model.
    
    """

    class Meta:
        model = Pipe
        fields = (
            "pipeline",
            "source",
            "base_source_port",
            "destination",
            "base_destination_port",
        )

