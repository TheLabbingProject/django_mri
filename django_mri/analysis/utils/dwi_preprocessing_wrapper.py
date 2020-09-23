from django_mri.models.scan import Scan
from django_mri.analysis.pipelines.dwi_preprocessing import (
    DWI_PREPROCESSING_PIPELINE,
)
from django_analyses.models.pipeline import Pipeline
from django_analyses.pipeline_runner import PipelineRunner


def dwi_preprocessing_wrapper(AP: Scan, PA: Scan):
    bvec_file = AP.nifti.b_vector_file
    bval_file = AP.nifti.b_value_file
    dwi_json_file = AP.nifti.json_file
    fmap_json_file = PA.nifti.json_file
    dwi_convert_inputs = {
        "in_file": AP.nifti.path,
        "fslgrad": [str(bvec_file), str(bval_file)],
        "json_import": str(dwi_json_file),
    }
    fmap_convert_inputs = {
        "in_file": str(PA.nifti.path),
        "json_import": str(fmap_json_file),
    }
    dwifslpreproc_inputs = {
        "json_import": str(dwi_json_file),
        "fslgrad": [str(bvec_file), str(bval_file)],
    }
    dwi_pipeline = Pipeline.objects.from_dict(DWI_PREPROCESSING_PIPELINE)
    runner = PipelineRunner(dwi_pipeline)
    mrconvert_node = dwi_pipeline.node_set.filter(
        analysis_version__analysis__title="mrconvert"
    ).last()
    dwifslpreproc_node = dwi_pipeline.node_set.get(
        analysis_version__analysis__title="dwifslpreproc"
    )
    return runner.run(
        inputs={
            mrconvert_node: [dwi_convert_inputs, fmap_convert_inputs],
            dwifslpreproc_node: dwifslpreproc_inputs,
        }
    )
