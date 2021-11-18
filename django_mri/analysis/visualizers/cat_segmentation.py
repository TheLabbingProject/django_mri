from typing import Iterable

import nibabel as nib
import numpy as np
from django_analyses.models.run import Run
from nilearn.plotting import view_img

from django_mri.analysis.visualizers.segmentation import SegmentationVisualizer


class CatSegmentationVisualizer(SegmentationVisualizer):
    def visualize(self, run) -> None:
        grey_matter = run.get_output("modulated_grey_matter")
        white_matter = run.get_output("modulated_white_matter")
        super().visualize(grey_matter=grey_matter, white_matter=white_matter)


def plot_mean_results(
    runs: Iterable[Run], output_key: str = "modulated_grey_matter"
):
    results = [
        np.nan_to_num(nib.load(run.get_output(output_key)).get_fdata())
        for run in runs
    ]
    stacked = np.stack(results, axis=0)
    mean_modulated_gm_data = np.mean(stacked, axis=0)
    affine = nib.load(runs[0].get_output(output_key)).affine
    mean_image = nib.Nifti1Image(mean_modulated_gm_data, affine=affine)
    return view_img(mean_image)
