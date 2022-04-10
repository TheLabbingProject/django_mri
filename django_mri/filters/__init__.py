"""
Filters for app's models.

Notes
-----
For more information, see:

    * `Django REST Framework`_ `filtering documentation`_.
    * django-filter_'s documentation for `Integration with DRF`_.

.. _django-filter: https://django-filter.readthedocs.io/en/stable/index.html
.. _Django REST Framework: https://www.django-rest-framework.org/
.. _filtering documentation:
   https://www.django-rest-framework.org/api-guide/filtering/
.. _Integration with DRF:
   https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html
"""

from django_mri.filters.atlas_filter import AtlasFilter
from django_mri.filters.irb_approval_filter import IrbApprovalFilter
from django_mri.filters.metric_filter import MetricFilter
from django_mri.filters.region_filter import RegionFilter
from django_mri.filters.scan_filter import ScanFilter
from django_mri.filters.score_filter import ScoreFilter

# flake8: noqa: E401
