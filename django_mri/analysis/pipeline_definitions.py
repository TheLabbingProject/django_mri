"""
Aggregates pipeline definitions from :mod:`django_mri.analysis.pipelines`.
The created list (*pipeline_definitions*) may easily be imported to the
database using the
:meth:`~django_analysis.models.managers.pipline.PipelineManager.from_list`
method.

Example
-------

.. code-block:: py

    from django_analyses.models.pipeline import Pipleine
    from django_mri.analysis.pipeline_definitions import pipeline_definitions

    Pipeline.objects.from_list(pipeline_definitions)

"""

from django_mri.analysis.pipelines.basic_fsl_preprocessing import (
    BASIC_FSL_PREPROCESSING,
)

pipeline_definitions = [BASIC_FSL_PREPROCESSING]
