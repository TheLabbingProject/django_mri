import nibabel as nib
import numpy as np
import os

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_mri.utils.compression import compress, uncompress
from niwidgets import NiftiWidget
from pathlib import Path


class NIfTI(TimeStampedModel):
    """
    A model for maintaining NIfTI_ files.

    .. _NIfTI: https://nifti.nimh.nih.gov/nifti-1/
    """

    path = models.FilePathField(max_length=1000, unique=True)

    # is_raw is meant to be set according to whether the created instance
    # is the product of a direct conversion from the raw data to NIfTI (True),
    # or of a manipulation of the data (False).
    is_raw = models.BooleanField(default=False)

    class Meta:
        verbose_name = "NIfTI"

    def get_data(self) -> np.ndarray:
        """
        Uses nibabel_ to return the underlying pixel data as a NumPy_ array.

        .. _nibabel: https://nipy.org/nibabel/
        .. _NumPy: http://www.numpy.org/

        Returns
        -------
        np.ndarray
            Pixel data.
        """

        return nib.load(self.path).get_data()

    def get_b_value(self) -> list:
        """
        Returns the degree of diffusion weighting applied (b-value_) for each
        diffusion direction. This method relies on dcm2niix_'s default
        configuration in which when diffusion-weighted images (DWI_) are
        converted, another file with the same name and a "bval" extension is
        created alongside.

        .. _b-value: https://radiopaedia.org/articles/b-values-1
        .. _dcm2niix: https://github.com/rordenlab/dcm2niix
        .. _DWI: https://en.wikipedia.org/wiki/Diffusion_MRI

        Returns
        -------
        list
            b-value for each diffusion direction.
        """

        curr_path = str(self.path)
        file_name = curr_path.replace("nii.gz", "bval")
        if os.path.isfile(file_name):
            with open(file_name, "r") as file_object:
                content = file_object.read()
            content = content.splitlines()[0].split("\t")
            return [int(value) for value in content]
        return None

    def get_b_vector(self) -> list:
        """
        Returns the b-vectors_ representing the diffusion weighting gradient scheme.
        This method relies on dcm2niix_'s default configuration in which when
        diffusion-weighted images (DWI_) are converted, another file with the same
        name and a "bvec" extension is created alongside.

        .. _b-vectors: https://mrtrix.readthedocs.io/en/latest/concepts/dw_scheme.html
        .. _dcm2niix: https://github.com/rordenlab/dcm2niix
        .. _DWI: https://en.wikipedia.org/wiki/Diffusion_MRI

        Returns
        -------
        list
            b-value for each diffusion direction
        """
        curr_path = str(self.path)
        file_name = curr_path.replace("nii.gz", "bvec")
        if os.path.isfile(file_name):
            with open(file_name, "r") as file_object:
                content = file_object.read()
            return [
                [float(value) for value in vector.rstrip().split("\t")]
                for vector in content.rstrip().split("\n")
            ]
        return None

    def niwidgets_plot(self, **kwargs):
        widget = NiftiWidget(self.path)
        return widget.nifti_plotter(**kwargs)

    def plot(self, provider: str = "niwidgets", **kwargs):
        if provider == "niwidgets":
            return self.niwidgets_plot(**kwargs)

    def compress(self, keep_source: bool = False) -> Path:
        if not self.is_compressed:
            uncompressed_path = Path(self.path)
            compressed_path = compress(uncompressed_path, keep_source=keep_source)
            self.path = str(compressed_path)
            self.save()
        return Path(self.path)

    def uncompress(self, keep_source: bool = False) -> Path:
        if self.is_compressed:
            compressed_path = Path(self.path)
            uncompressed_path = uncompress(compressed_path, keep_source=keep_source)
            self.path = str(uncompressed_path)
            self.save()
        return Path(self.path)

    @property
    def b_value(self) -> list:
        return self.get_b_value()

    @property
    def b_vector(self) -> list:
        return self.get_b_vector()

    @property
    def is_compressed(self) -> bool:
        return Path(self.path).name.endswith(".gz")

    @property
    def compressed(self) -> Path:
        return self.compress()

    @property
    def uncompressed(self) -> Path:
        return self.uncompress()
