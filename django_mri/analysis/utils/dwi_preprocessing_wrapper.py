from django_analyses.models.pipeline import Pipeline
from django_analyses.pipeline_runner import PipelineRunner

from django_mri.analysis.pipelines.dwi_preprocessing import \
    DWI_PREPROCESSING_PIPELINE
from django_mri.models.scan import Scan

# from django_analyses.tasks import execute_pipeline


def dwi_preprocessing_wrapper(AP: Scan, PA: Scan):
    bvec_file = AP.nifti.b_vector_file
    bval_file = AP.nifti.b_value_file
    n_dwi_volumes = int(AP.nifti.get_data().shape[-1])
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
    mrconvert_extract_fmap_inputs = {"coord": "3 0:0"}
    mrconvert_extract_dwi_inputs = {"coord": f"3 1:{n_dwi_volumes}"}
    mrconvert_list = [
        dwi_convert_inputs,
        fmap_convert_inputs,
        mrconvert_extract_fmap_inputs,
        mrconvert_extract_dwi_inputs,
    ]

    dwigradcheck_inputs = {
        "fslgrad": [str(bvec_file), str(bval_file)],
    }
    dwifslpreproc_inputs = {
        "json_import": str(dwi_json_file),
    }
    dwi_pipeline = Pipeline.objects.from_dict(DWI_PREPROCESSING_PIPELINE)
    mrconvert_node = dwi_pipeline.node_set.filter(
        analysis_version__analysis__title="mrconvert"
    ).last()
    dwigradcheck_node = dwi_pipeline.node_set.get(
        analysis_version__analysis__title="dwigradcheck"
    )
    dwifslpreproc_node = dwi_pipeline.node_set.get(
        analysis_version__analysis__title="dwifslpreproc"
    )
    inputs = {
        mrconvert_node.id: mrconvert_list,
        dwigradcheck_node.id: dwigradcheck_inputs,
        dwifslpreproc_node.id: dwifslpreproc_inputs,
    }
    # return execute_pipeline.delay(pipeline_id=dwi_pipeline.id, inputs=inputs)
    runner = PipelineRunner(dwi_pipeline)
    return runner.run(inputs=inputs)
