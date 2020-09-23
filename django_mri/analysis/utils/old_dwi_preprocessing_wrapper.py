from django_mri.models.scan import Scan
from django_mri.analysis.pipelines.old_dwi_preprocessing import (
    DWI_PREPROCESSING_PIPELINE,
)
from django_analyses.models.pipeline import Pipeline
from django_analyses.pipeline_runner import PipelineRunner


def dwi_preprocessing_wrapper(AP: Scan, PA: Scan, T1w: Scan):
    bvec_file = AP.nifti.b_vector_file
    bval_file = AP.nifti.b_value_file
    json_file = AP.nifti.json_file
    pe_dir = AP.nifti.get_phase_encoding_direction()
    fslroi_inputs = {"in_file": AP.nifti}
    # bet_inputs = {"in_file": T1w.nifti}
    flirt_inputs = {"in_file": T1w.nifti}
    fslmerge_inputs = {"in_files": [PA.nifti]}
    denoise_inputs = {"in_file": AP}
    dwifslpreproc_inputs = {
        "json_import": str(json_file),
        "fslgrad": [str(bvec_file), str(bval_file)],
        "pe_dir": pe_dir,
    }
    dwi_pipeline = Pipeline.objects.from_dict(DWI_PREPROCESSING_PIPELINE)
    runner = PipelineRunner(dwi_pipeline)
    fslroi_node = dwi_pipeline.node_set.get(
        analysis_version__analysis__title="fslroi"
    )
    flirt_node = dwi_pipeline.node_set.get(
        analysis_version__analysis__title="FLIRT"
    )
    fslmerge_node = dwi_pipeline.node_set.get(
        analysis_version__analysis__title="fslmerge"
    )
    dwifslpreproc_node = dwi_pipeline.node_set.get(
        analysis_version__analysis__title="dwifslpreproc"
    )
    denoise_node = dwi_pipeline.node_set.get(
        analysis_version__analysis__title="denoise"
    )
    return runner.run(
        inputs={
            fslroi_node: fslroi_inputs,
            flirt_node: flirt_inputs,
            fslmerge_node: fslmerge_inputs,
            dwifslpreproc_node: dwifslpreproc_inputs,
            denoise_node: denoise_inputs,
        }
    )
