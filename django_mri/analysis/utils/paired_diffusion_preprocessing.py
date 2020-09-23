from django_mri.models.scan import Scan
from django_mri.analysis.pipelines.dwi_preprocessing import (
    DWI_PREPROCESSING_PIPELINE,
)
from django_mri.analysis.utils.dwi_preprocessing_wrapper import (
    dwi_preprocessing_wrapper,
)
from django_mri.analysis.utils import get_template_fa
from django_mri.models.session import Session
from django_analyses.models.pipeline import Pipeline
from django_analyses.pipeline_runner import PipelineRunner


def paired_diffusion_preprocessing(
    before_session: Session, after_session: Session
):
    ten2met_v = AnalysisVersion.objects.get(analysis__title="tensor2metric")
    ten2met_node, _ = Node.objects.get_or_create(analysis_version=ten2met)
    metrices_results = []
    for session in [before_session, after_session]:
        AP = [
            scan
            for scan in session.scan_set.filter(description__icontains="AP")
            if scan.sequence_type.title == "DWI"
        ][0]
        PA = [
            scan
            for scan in session.scan_set.filter(description__icontains="PA")
            if scan.sequence_type.title == "DWI"
        ][0]
        T1w = [
            scan
            for scan in session.scan_set.filter(
                description__icontains="mprage"
            )
            if "corrected" in str(scan.nifti.path)
        ][0]
        dwi_preprocessing_results = dwi_preprocessing_wrapper(AP, PA, T1w)
        metrices_results.append(dwi_preprocessing_results.get(ten2met_node))
    fas = []
    for run in metrices_results:
        for out_file in metrices_results.output_set:
            if out_file.definition.key == "fa":
                fas.append(out_file)
    reference = get_template_fa()  ## REPLACE WITH MNI BRAIN



docker run -ti --rm \
-v /media/groot/Data/BeforeAfterCovid19_BIDS_dataset:/bids_dataset \
-v /media/groot/Data/BeforeAfterCovid19_derivatives/ndmg_derivatives:/outputs \
bids/ndmg \
/bids_dataset /outputs participant --participant_label 0010
