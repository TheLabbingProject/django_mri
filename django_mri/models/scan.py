import os
import pytz

from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_mri.interfaces.dcm2niix import Dcm2niix
from django_mri.models.nifti import NIfTI
from django_mri.models.sequence_type import SequenceType


class Scan(TimeStampedModel):
    """
    A model used to represent an MRI scan independently from the file-format in
    which it is saved. This model handles any conversions between formats in case
    they are required, and allows for easy querying of MRI scans based on universal
    attributes.

    """

    institution_name = models.CharField(max_length=64, blank=True, null=True)
    time = models.DateTimeField(
        blank=True, null=True, help_text="The time in which the scan was acquired."
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="A short description of the scan's acqusition parameters.",
    )
    number = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="The number of this scan relative to the session in which it was acquired.",
    )

    # Relatively universal MRI scan attributes. These might be infered from the
    # raw file's meta-data.
    echo_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="The time between the application of the radiofrequency excitation pulse and the peak of the signal induced in the coil (in milliseconds).",
    )
    repetition_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="The time between two successive RF pulses (in milliseconds).",
    )
    inversion_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="The time between the 180-degree inversion pulse and the following spin-echo (SE) sequence (in milliseconds).",
    )
    spatial_resolution = ArrayField(models.FloatField(), size=3, blank=True, null=True)

    comments = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="If anything noteworthy happened during acquisition, it may be noted here.",
    )

    # If this instance's origin is a DICOM file, or it was saved as one, this field
    # keeps the relation to that django_dicom.Series instance.
    dicom = models.OneToOneField(
        "django_dicom.Series",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="scan",
        verbose_name="DICOM Series",
    )
    # Keep track of whether we've updated the instance's fields from the DICOM
    # header data.
    is_updated_from_dicom = models.BooleanField(default=False)

    # If converted to NIfTI, keep a reference to the resulting instance.
    # The reason it is suffixed with an underline is to allow for "nifti"
    # to be used as a property that automatically returns an existing instance
    # or creates one.
    nifti = models.OneToOneField(
        "django_mri.NIfTI", on_delete=models.SET_NULL, blank=True, null=True
    )

    subject = models.ForeignKey(
        settings.SUBJECT_MODEL,
        on_delete=models.PROTECT,
        related_name="mri_scans",
        blank=True,
        null=True,
    )

    study_groups = models.ManyToManyField(
        settings.STUDY_GROUP_MODEL, related_name="mri_scans", blank=True
    )

    added_by = models.ForeignKey(
        get_user_model(),
        related_name="mri_uploads",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ("time",)
        verbose_name_plural = "MRI Scans"

    def update_fields_from_dicom(self) -> None:
        """
        Sets instance fields from related DICOM series.
        TODO: Needs refactoring.

        Raises
        ------
        AttributeError
            If not DICOM series is related to this scan.
        """

        if self.dicom:
            self.institution_name = self.dicom.institution_name
            self.number = self.dicom.number
            self.time = datetime.combine(
                self.dicom.date, self.dicom.time, tzinfo=pytz.UTC
            )
            self.description = self.dicom.description
            self.echo_time = self.dicom.echo_time
            self.inversion_time = self.dicom.inversion_time
            self.repetition_time = self.dicom.repetition_time
            self.spatial_resolution = self.get_spatial_resolution_from_dicom()
            self.is_updated_from_dicom = True
        else:
            raise AttributeError(f"No DICOM data associated with MRI scan {self.id}!")

    def get_spatial_resolution_from_dicom(self) -> list:
        """
        Returns the spatial resolution of the MRI scan as infered from a
        related DICOM series. In DICOM headers, "*x*" and "*y*" resolution
        (the rows and columns of each instance) are listed as "`Pixel Spacing`_"
        and the "*z*" plane resolution corresponds to "`Slice Thickness`_".
        `Pixel Spacing`_ is a `required (type 1)`_ DICOM attribute, and therefore
        has to be returned, however `Slice Thickness`_ may be empty (`type 2`).

        .. _Pixel Spacing: https://dicom.innolitics.com/ciods/mr-image/image-plane/00280030
        .. _Slice Thickness: https://dicom.innolitics.com/ciods/mr-image/image-plane/00180050
        .. _required (type 1): http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_7.4.html
        .. _type 2: http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_7.4.html

        Returns
        -------
        list
            "*[x, y, z]*" spatial resolution in millimeters.
        """

        sample_image = self.dicom.image_set.first()
        slice_thickness = sample_image.header.get_value("SliceThickness")
        if slice_thickness:
            return self.dicom.pixel_spacing + [slice_thickness]
        else:
            return self.dicom.pixel_spacing

    def infer_sequence_type_from_dicom(self) -> SequenceType:
        """
        Returns the appropriate :class:`django_mri.SequenceType` instance according to
        the scan's "*ScanningSequence*" and "*SequenceVariant*" header values.


        Returns
        -------
        SequenceType
            A SequenceType instance.
        """

        try:
            return SequenceType.objects.get(
                scanning_sequence=self.dicom.scanning_sequence,
                sequence_variant=self.dicom.sequence_variant,
            )
        except models.ObjectDoesNotExist:
            return None

    def infer_sequence_type(self) -> SequenceType:
        if self.dicom:
            return self.infer_sequence_type_from_dicom()

    def get_default_nifti_dir(self) -> str:
        """
        Returns the default location for the creation of a NIfTI version of the
        scan. Currently only conversion from DICOM is supported.

        Returns
        -------
        str
            Default location for conversion output.
        """

        if self.dicom:
            return self.dicom.get_path().replace("DICOM", "NIfTI")

    def get_default_nifti_name(self) -> str:
        """
        Returns the default file name for a NIfTI version of this scan.

        Returns
        -------
        str
            Default file name.
        """

        return str(self.id)

    def get_default_nifti_destination(self) -> str:
        """
        Returns the default path for a NIfTI version of this scan.

        Returns
        -------
        str
            Default path for NIfTI file.
        """

        directory = self.get_default_nifti_dir()
        name = self.get_default_nifti_name()
        return os.path.join(directory, name)

    def dicom_to_nifti(
        self,
        destination: str = None,
        compressed: bool = True,
        generate_json: bool = False,
    ) -> NIfTI:
        """
        Convert this scan from DICOM to NIfTI using _dcm2niix.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Parameters
        ----------
        destination : str, optional
            The desired path for conversion output (the default is None, which
            will create the file in some default location).

        Raises
        ------
        AttributeError
            If no DICOM series is related to this scan.

        Returns
        -------
        NIfTI
            A :class:`django_mri.NIfTI` instance referencing the conversion output.
        """

        if self.dicom:
            dcm2niix = Dcm2niix()
            destination = destination or self.get_default_nifti_destination()
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            nifti_path = dcm2niix.convert(
                self.dicom.get_path(),
                destination,
                compressed=compressed,
                generate_json=generate_json,
            )
            nifti = NIfTI.objects.create(path=nifti_path, parent=self, is_raw=True)
            return nifti
        else:
            raise AttributeError(
                f"Failed to convert scan #{self.id} from DICOM to NIfTI! No DICOM series is related to this scan."
            )

    @property
    def sequence_type(self) -> SequenceType:
        return self.infer_sequence_type()
