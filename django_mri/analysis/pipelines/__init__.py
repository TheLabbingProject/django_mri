"""
Proposed pipeline definitions for MRI data using commonplace neuroimaging
analysis interfaces.

Pipeline definitions are aggregated in
:mod:`~django_mri.analysis.pipeline_definitions` and may be added to the
database using the
:meth:`Pipeline.objects.from_list()
<~django_analyses.models.managers.pipeline.PipelineManager.from_list>`
method.

Example
-------

.. code-block:: py

    from django_analyses.models.pipeline import Pipeline
    from django_mri.analysis.pipeline_definitions import pipeline_definitions

    Pipeline.objects.from_list(pipeline_definitions)

"""
