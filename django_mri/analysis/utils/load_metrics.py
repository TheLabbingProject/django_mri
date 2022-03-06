from typing import List, Tuple

from django_mri.analysis.metric.definitions import METRIC_DEFINITIONS
from django_mri.models.metric import Metric


def load_metrics() -> List[Tuple[Metric, bool]]:
    return [
        Metric.objects.get_or_create(**metric_definition)
        for metric_definition in METRIC_DEFINITIONS
    ]
