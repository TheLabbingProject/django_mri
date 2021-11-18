"""
Definition of the :class:`NIfTI` model.
"""
import json
import logging
from pathlib import Path
from typing import List, Union

import nibabel as nib
import numpy as np
from django.db import models
from django_analyses.models.input import FileInput, ListInput
from django_extensions.db.models import TimeStampedModel

from django_mri.models.messages import NIFTI_FILE_MISSING
from django_mri.utils.compression import compress, uncompress


class NIfTI(TimeStampedModel):
    """
    A model representing a NIfTI_ file in the database.

    .. _NIfTI: https://nifti.nimh.nih.gov/nifti-1/
    """

    #: Path of the *.nii* file within the application's media directory.
    path = models.FilePathField(max_length=1000, unique=True)

    #: Whether the created instance is the product of a direct conversion from
    #: some raw format to NIfTI or of a manipulation of the data.
    is_raw = models.BooleanField(default=False)

    # Used to cache JSON data to prevent multiple reads.
    _json_data = None

    # Logger instance for this model.
    _logger = logging.getLogger("data.mri.nifti")

    class Meta:
        verbose_name = "NIfTI"
        ordering = ("-id",)

    def get_data(self, dtype: np.dtype = np.float64) -> np.ndarray:
        """
        Uses NiBabel_ to return the underlying pixel data as a NumPy_ array.

        .. _NiBabel: https://nipy.org/nibabel/
        .. _NumPy: http://www.numpy.org/

        Returns
        -------
        np.ndarray
            Pixel data.
        """

        return nib.load(str(self.path)).get_fdata(dtype=dtype)

    def get_b_value(self) -> List[int]:
        """
        Returns the degree of diffusion weighting applied (b-value_) for each
        diffusion direction. This method relies on dcm2niix_'s default
        configuration in which when diffusion-weighted images (DWI_) are
        converted, another file with the same name and a "bval" extension is
        created alongside.

        .. _b-value: https://radiopaedia.org/articles/b-values-1
        .. _dcm2niix: https://github.com/rordenlab/dcm2niix
        .. _DWI: https://en.wikipedia.org/wiki/Diffusion_MRI

        Hint
        ----
        For more information, see dcm2niix's `Diffusion Tensor Imaging`_
        section of the user guide.

        .. _Diffusion Tensor Imaging:
           https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage#Diffusion_Tensor_Imaging

        See Also
        --------
        * :attr:`b_value`

        Returns
        -------
        List[int]
            b-value for each diffusion direction.
        """
        file_name = self.b_value_file
        if file_name:
            with open(file_name, "r") as file_object:
                content = file_object.read()
            content = content.splitlines()[0].split(" ")
            return [int(value) for value in content]
        return None

    def get_b_vector(self) -> List[List[float]]:
        """
        Returns the b-vectors_ representing the diffusion weighting gradient
        scheme. This method relies on dcm2niix_'s default configuration in
        which when diffusion-weighted images (DWI_) are converted, another file
        with the same name and a "bvec" extension is created alongside.

        .. _b-vectors:
           https://mrtrix.readthedocs.io/en/latest/concepts/dw_scheme.html
        .. _dcm2niix: https://github.com/rordenlab/dcm2niix
        .. _DWI: https://en.wikipedia.org/wiki/Diffusion_MRI

        Hint
        ----
        For more information, see dcm2niix's `Diffusion Tensor Imaging`_
        section of the user guide.

        .. _Diffusion Tensor Imaging:
           https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage#Diffusion_Tensor_Imaging

        See Also
        --------
        * :attr:`b_vector`

        Returns
        -------
        List[List[float]]
            b-value for each diffusion direction
        """
        file_name = self.b_vector_file
        if file_name:
            with open(file_name, "r") as file_object:
                content = file_object.read()
            return [
                [float(value) for value in vector.rstrip().split(" ")]
                for vector in content.rstrip().split("\n")
            ]

    def read_json(self) -> dict:
        """
        Returns the JSON data generated alognside *.nii* files generated
        using dcm2niix_\'s *"BIDS sidecar"* option.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Notes
        -----
        * For more information about dcm2niix and the BIDS sidecar, see
          dcm2niix's `general usage manual`_.
        * For more information about the extracted properties and their usage
          see `Acquiring and Using Field-maps`_

        .. _Acquiring and Using Field-maps:
           https://lcni.uoregon.edu/kb-articles/kb-0003
        .. _general usage manual:
            https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage#General_Usage

        Returns
        -------
        dict
            BIDS sidecar information stored in a JSON file, or *{}* if the file
            doesn't exist
        """
        if self.json_file.is_file():
            with open(self.json_file, "r") as f:
                return json.load(f)
        return {}

    def get_total_readout_time(self) -> float:
        """
        Reads the total readout time extracted by dcm2niix_ upon conversion.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Hint
        ----
        Total readout time is defined as the time from the center of the first
        echo to the center of the last (in seconds).

        Returns
        -------
        float
            Total readout time
        """
        return self.json_data.get("TotalReadoutTime")

    def get_effective_spacing(self) -> float:
        """
        Reads the effective echo spacing value extracted by dcm2niix_ upon
        conversion.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Returns
        -------
        float
            Effective echo spacing
        """
        return self.json_data.get("EffectiveEchoSpacing")

    def get_phase_encoding_direction(self) -> float:
        """
        Reads the phase encoding direction value extracted by dcm2niix_ upon
        conversion.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Returns
        -------
        float
            Phase encoding direction
        """
        return self.json_data.get("PhaseEncodingDirection")

    def compress(self, keep_source: bool = False) -> Path:
        """
        Compress the associated *.nii* using gzip, if it isn't already
        compressed.

        Parameters
        ----------
        keep_source : bool, optional
            Whether to keep a copy of the uncompressed file, by default False

        Returns
        -------
        Path
            Path of the compressed (*.nii.gz*) file
        """
        if not self.is_compressed:
            uncompressed_path = Path(self.path)
            compressed_path = compress(
                uncompressed_path, keep_source=keep_source
            )
            self.path = str(compressed_path)
            self.save()
        return Path(self.path)

    def uncompress(self, keep_source: bool = False) -> Path:
        """
        Uncompress the associated *.nii* using gzip, if it isn't already
        uncompressed.

        Parameters
        ----------
        keep_source : bool, optional
            Whether to keep a copy of the compressed file, by default False

        Returns
        -------
        Path
            Path of the uncompressed (*.nii*) file
        """
        if self.is_compressed:
            compressed_path = Path(self.path)
            uncompressed_path = uncompress(
                compressed_path, keep_source=keep_source
            )
            self.path = str(uncompressed_path)
            self.save()
        return Path(self.path)

    def _resolve_compression_state(self) -> None:
        """
        Fixed the instance's path in case it's out of sync with compression
        state. This method is used for testing and Should not be required
        under normal circumstances.

        Raises
        ------
        FileNotFoundError
            No associated file found in the file system
        """
        path = Path(self.path)
        is_compressed = path.suffix == ".gz"
        compressed_path = path if is_compressed else path.with_suffix(".gz")
        uncompressed_path = path if not is_compressed else path.with_suffix("")
        valid_compressed = is_compressed and compressed_path.exists()
        valid_uncompressed = uncompressed_path.exists() and not is_compressed
        if not valid_compressed and uncompressed_path.exists():
            self.path = str(path.with_suffix(""))
            self.save()
        elif not valid_uncompressed and compressed_path.exists():
            self.path = str(path.with_suffix(".gz"))
            self.save()
        elif valid_compressed or valid_uncompressed:
            return
        else:
            message = NIFTI_FILE_MISSING.format(pk=self.id, path=self.path)
            raise FileNotFoundError(message)

    def rename(
        self, destination: Union[Path, str], log_level: int = logging.DEBUG
    ):
        source = Path(self.path)
        destination = Path(destination)
        self._logger.log(log_level, f"Moving NIfTI #{self.id}...")
        self._logger.log(log_level, f"Source:\t{source}")
        self._logger.log(log_level, f"Destination:\t{destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        source.rename(destination)
        json_sidecar = source.parent / (source.name.split(".")[0] + ".json")
        if json_sidecar.exists():
            self._logger.log(log_level, "Moving JSON sidecar...")
            json_destination = destination.parent / (
                destination.name.split[0] + ".json"
            )
            json_sidecar.rename(json_destination)
            self._logger.log(log_level, "JSON sidecar moved.")
        if self.is_raw and self.scan:
            self._logger.log(
                log_level, f"Found associated scan (#{self.scan.id})."
            )
            self._logger.log(
                log_level, "Querying scan's input set for changed runs..."
            )
            for input_instance in self.scan.input_set.all():
                is_file_input = isinstance(input_instance, FileInput)
                is_list_input = isinstance(input_instance, ListInput)
                if is_file_input and input_instance.value == str(source):
                    self._logger.log(
                        log_level,
                        f"Found changed file input instance:\n{input_instance}",
                    )
                    self._logger.log(log_level, "Updating file input value...")
                    input_instance.value = str(destination)
                    input_instance.save()
                    self._logger.log(log_level, "done!")
                elif is_list_input and str(source) in input_instance.value:
                    self._logger.log(
                        log_level,
                        f"Found changed list input instance:\n{input_instance}",
                    )
                    self._logger.log(log_level, "Updating list input value...")
                    input_instance.value = [
                        path if path != str(source) else str(destination)
                        for path in input_instance.value
                    ]
                    input_instance.save()
                    self._logger.log(log_level, "done!")
        self.path = str(destination)
        self._logger.log(
            log_level, f"NIfTI {self.id} file successfully moved."
        )
        self.save()

    @property
    def json_file(self) -> Path:
        """
        Return path to the corresponding json file.
        Returns
        -------
        Path
            Corresponding json file
        """
        base_name = Path(self.path).name.split(".")[0]
        return (Path(self.path).parent / base_name).with_suffix(".json")

    @property
    def json_data(self) -> dict:
        """
        Reads BIDS sidecar information and caches within a local variable to
        prevent multiple reads.

        See Also
        --------
        * :meth:`read_json`

        Returns
        -------
        dict
            "BIDS sidecar" JSON data
        """
        if self._json_data is None:
            self._json_data = self.read_json()
        return self._json_data

    @property
    def b_value_file(self) -> Path:
        """
        Return FSL format b-value file path

        Returns
        -------
        Path
            FSL format b-value file path
        """
        p = Path(self.path)
        bval_file = p.parent / Path(p.stem).with_suffix(".bval")
        if bval_file.is_file():
            return bval_file

    @property
    def b_vector_file(self) -> Path:
        """
        Return FSL format b-vector file path.

        Returns
        -------
        Path
            FSL format b-vector file path
        """
        p = Path(self.path)
        bvec_file = p.parent / Path(p.stem).with_suffix(".bvec")
        if bvec_file.is_file():
            return bvec_file

    @property
    def b_value(self) -> List[int]:
        """
        Returns the B-value of DWI scans as calculated by dcm2niix_.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        See Also
        --------
        * :meth:`get_b_value`

        Returns
        -------
        List[int]
            B-value
        """
        return self.get_b_value()

    @property
    def b_vector(self) -> List[List[float]]:
        """
        Returns the B-vector of DWI scans as calculated by dcm2niix_.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        See Also
        --------
        * :meth:`get_b_vector`

        Returns
        -------
        List[List[float]]
            B-vector
        """
        return self.get_b_vector()

    @property
    def is_compressed(self) -> bool:
        """
        Whether the associated *.nii* file is compressed with gzip or not.

        Returns
        -------
        bool
            Associated *.nii* file gzip compression state
        """

        return Path(self.path).suffix == ".gz"

    @property
    def compressed(self) -> Path:
        """
        Compresses the associated *.nii* file using gzip if it isn't and
        returns its path.

        Returns
        -------
        Path
            Compressed *.nii.gz* file associated with this instance
        """
        return self.compress()

    @property
    def uncompressed(self) -> Path:
        """
        Uncompresses the associated *.nii* file using gzip if it isn't and
        returns its path.

        Returns
        -------
        Path
            Uncompressed *.nii* file associated with this instance
        """
        return self.uncompress()
