from typing import Callable

from django_analyses.models.run import Run
from django_mri.analysis.score.mriqc import create_mriqc_scores
from django_mri.analysis.score.recon_all import create_recon_all_scores

SCORERS = {"ReconAll": create_recon_all_scores, "MRIQC": create_mriqc_scores}


def get_scorer(run: Run) -> Callable:
    analysis_scorers = SCORERS.get(run.analysis_version.analysis.title, {})
    if isinstance(analysis_scorers, Callable):
        return analysis_scorers
    else:
        return analysis_scorers.get(run.analysis_version.title)
