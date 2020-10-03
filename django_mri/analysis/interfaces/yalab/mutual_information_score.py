import nibabel as nib
import numpy as np

from pathlib import Path
from sklearn.metrics import mutual_info_score


class MutualInformationScore:
    NIFTI_SUFFIXES = [[".nii"], [".nii", ".gz"]]

    def __init__(self, bins: int = 10):
        self.bins = bins

    def read_nifti(self, path: Path) -> np.ndarray:
        return nib.load(str(path)).get_data().flatten()

    def read_data(self, path: Path) -> np.ndarray:
        is_nifti = Path(path).suffixes in self.NIFTI_SUFFIXES
        if is_nifti:
            return self.read_nifti(path)
        raise ValueError(
            "Input file must be a NIfTI format file (.nii/.nii.gz)!"
        )

    def run(self, anatomical_1: Path, anatomical_2: Path) -> dict:
        data_1 = self.read_data(anatomical_1)
        data_2 = self.read_data(anatomical_2)
        histogram = np.histogram2d(data_1, data_2, self.bins)[0]
        score = mutual_info_score(None, None, contingency=histogram)
        return {"score": score}
