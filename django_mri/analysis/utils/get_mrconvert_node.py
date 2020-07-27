"""
Definition of some utility functions to fetch the latest *MRConvert* version
or basic node.

References
----------
* MRtrix3 `mrconvert documentation`_
* nipype's `MRConvert interface`_

.. _mrconvert documentation:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/mrconvert.html
.. _MRConvert interface:
   https://nipype.readthedocs.io/en/1.5.0/api/generated/nipype.interfaces.mrtrix3.utils.html#mrconvert
"""

from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.pipeline.node import Node


def get_mrconvert_analysis_version():
    """
    Returns the latest *MRConvert* analysis version.

    See Also
    --------
    * :meth:`AnalysisVersion.objects.get_by_string_id()
      <django_analyses.models.managers.analysis_version.AnalysisVersionManager.from_string_id>`
    """

    try:
        return AnalysisVersion.objects.get_by_string_id("mrconvert")
    except AnalysisVersion.DoesNotExist:
        raise AnalysisVersion.DoesNotExist(
            "MRconvert interface not registered in database."
        )


def get_mrconvert_node():
    """
    Gets or creates a basic (default configuration) *MRConvert* node.

    See Also
    --------
    * :func:`get_mrconvert_analysis_version`
    """

    configuration = {}
    analysis_version = get_mrconvert_analysis_version()
    return Node.objects.get_or_create(
        analysis_version=analysis_version, configuration=configuration
    )
