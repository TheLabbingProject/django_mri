from django_mri.models.scan import Scan
from django_mri.analysis.pipelines.dwi_preprocessing import (
    DWI_PREPROCESSING_PIPELINE,
)
from django_analyses.models.pipeline import Pipeline
from django_analyses.pipeline_runner import PipelineRunner


def dwi_preprocessing_wrapper(AP: Scan, PA: Scan):
    bvec_file = AP.nifti.bvec_file
    bval_file = AP.nifti.bval_file
    json_file = AP.nifti.json_file
    pe_dir = AP.nifti.get_phase_encoding_direction()
    fslroi_inputs = {"in_file": AP.nifti}
    fslmerge_inputs = {"in_files": PA.nifti}
    dwifslpreproc_inputs = {
        "json_import": str(json_file),
        "fslgrad": [str(bvec_file), str(bval_file)],
        "pe_dir": pe_dir,
    }
    denoise_inputs = {"in_file": AP}
    dwi_pipeline, _ = Pipeline.objects.from_dict(DWI_PREPROCESSING_PIPELINE)
    runner = PipelineRunner(dwi_pipeline)
    fslroi_node = Pipeline.node_set.get(
        analysis_version__analysis__title="fslroi"
    )
    fslmerge_node = Pipeline.node_set.get(
        analysis_version__analysis__title="fslmerge"
    )
    dwifslpreproc_node = Pipeline.node_set.get(
        analysis_version__analysis__title="dwifslpreproc"
    )
    denoise_node = Pipeline.node_set.get(
        analysis_version__analysis__title="denoise"
    )
    return runner.run(
        inputs={
            fslroi_node: fslroi_inputs,
            fslmerge_node: fslmerge_inputs,
            dwifslpreproc_node: dwifslpreproc_inputs,
            denoise_node: denoise_inputs,
        }
    )
