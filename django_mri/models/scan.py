"""
Definition of the :class:`~django_mri.models.scan.Scan` model.
"""

import warnings

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_mri.analysis.interfaces.dcm2niix import Dcm2niix
from django_mri.models import help_text, messages
from django_mri.models.managers.scan import ScanManager
from django_mri.models.nifti import NIfTI
from django_mri.models.sequence_type import SequenceType
from django_mri.models.sequence_type_definition import SequenceTypeDefinition
from django_mri.utils.utils import get_subject_model, get_group_model
from django_mri.utils.utils import get_mri_root
from django_mri.utils.bids import Bids
from pathlib import Path


class Scan(TimeStampedModel):
    """
    A model used to represent an MRI scan independently from the file-format in
    which it is saved. This model handles any conversions between formats in
    case they are required, and allows for easy querying of MRI scans based on
    universal attributes.

    """

    #: The institution in which this scan was acquired.
    institution_name = models.CharField(max_length=64, blank=True, null=True)

    #: Acquisition datetime.
    time = models.DateTimeField(blank=True, null=True, help_text=help_text.SCAN_TIME)

    #: Short description of the scan's acquisition parameters.
    description = models.CharField(
        max_length=100, blank=True, null=True, help_text=help_text.SCAN_DESCRIPTION
    )

    #: The relative number of this scan in the session in which it was
    #: acquired.
    number = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=help_text.SCAN_NUMBER,
    )

    #: The time between the application of the radio-frequency excitation pulse
    #: and the peak of the signal induced in the coil (in milliseconds).
    echo_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=help_text.SCAN_ECHO_TIME,
    )

    #: The time between two successive RF pulses (in milliseconds).
    repetition_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=help_text.SCAN_REPETITION_TIME,
    )

    #: The time between the 180-degree inversion pulse and the following
    #: spin-echo (SE) sequence (in milliseconds).
    inversion_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=help_text.SCAN_INVERSION_TIME,
    )

    #: The spatial resolution of the image in millimeters.
    spatial_resolution = ArrayField(models.FloatField(), size=3, blank=True, null=True)

    #: Any other comments about this scan.
    comments = models.TextField(
        max_length=1000, blank=True, null=True, help_text=help_text.SCAN_COMMENTS,
    )

    #: If this instance's origin is a DICOM file, or it was saved as one, this
    #: field stores the association with the appropriate
    #: :class`django_dicom.models.series.Series` instance.
    dicom = models.OneToOneField(
        "django_dicom.Series",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="scan",
        verbose_name="DICOM Series",
    )

    #: Keeps track of whether we've updated the instance's fields from DICOM
    #: header data or not.
    is_updated_from_dicom = models.BooleanField(default=False)

    #: If converted to NIfTI, keep a reference to the resulting instance.
    #: The reason it is suffixed with an underline is to allow for "nifti"
    #: to be used as a property that automatically returns an existing instance
    #: or creates one.
    _nifti = models.OneToOneField(
        "django_mri.NIfTI", on_delete=models.SET_NULL, blank=True, null=True
    )

    #: Associates this scan with some subject. Subjects are expected to be
    #: represented by a model specified as `SUBJECT_MODEL` in the project's
    #: settings.
    subject = models.ForeignKey(
        get_subject_model(),
        on_delete=models.PROTECT,
        related_name="mri_scans",
        blank=True,
        null=True,
    )

    #: Individual scans may be associated with multiple `Group` instances.
    #: This is meant to provide flexibility in managing access to data between
    #: researchers working on different studies.
    #: The `Group` model is expected to be specified as `STUDY_GROUP_MODEL` in
    #: the project's settings.
    study_groups = models.ManyToManyField(
        get_group_model(), related_name="mri_scans", blank=True
    )

    #: Keeps a record of the user that added this scan.
    added_by = models.ForeignKey(
        get_user_model(),
        related_name="mri_uploads",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    objects = ScanManager()

    class Meta:
        verbose_name_plural = "MRI Scans"

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation of this instance
        """

        return self.description

    def save(self, *args, **kwargs) -> None:
        """
        Overrides the model's :meth:`~django.db.models.Model.save` method to
        provide custom validation.

        Hint
        ----
        For more information, see Django's documentation on `overriding model
        methods`_.

        .. _overriding model methods:
           https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-model-methods
        """

        if self.dicom and not self.is_updated_from_dicom:
            self.update_fields_from_dicom()
        super().save(*args, **kwargs)

    def update_fields_from_dicom(self) -> None:
        """
        Sets instance fields from related DICOM series.

        Raises
        ------
        AttributeError
            If not DICOM series is related to this scan
        """

        if self.dicom:
            self.institution_name = self.dicom.institution_name
            self.number = self.dicom.number
            self.time = self.dicom.datetime
            self.description = self.dicom.description
            self.echo_time = self.dicom.echo_time
            self.inversion_time = self.dicom.inversion_time
            self.repetition_time = self.dicom.repetition_time
            self.spatial_resolution = self.dicom.spatial_resolution
            self.is_updated_from_dicom = True
        else:
            raise AttributeError(f"No DICOM data associated with MRI scan {self.id}!")

    def infer_sequence_type_from_dicom(self) -> SequenceType:
        """
        Returns the appropriate :class:`django_mri.SequenceType` instance
        according to the scan's "*ScanningSequence*" and "*SequenceVariant*"
        header values.

        Returns
        -------
        SequenceType
            The inferred sequence type
        """

        try:
            sequence_definition = SequenceTypeDefinition.objects.get(
                scanning_sequence=self.dicom.scanning_sequence,
                sequence_variant=self.dicom.sequence_variant,
            )
            return sequence_definition.sequence_type
        except models.ObjectDoesNotExist:
            return None

    def infer_sequence_type(self) -> SequenceType:
        """
        Tries to infer the sequence type using associated data.

        Returns
        -------
        SequenceType
            The inferred sequence type
        """

        if self.dicom:
            return self.infer_sequence_type_from_dicom()

    def get_default_nifti_dir(self) -> Path:
        """
        Returns the default location for the creation of a NIfTI version of the
        scan. Currently only conversion from DICOM is supported.

        Returns
        -------
        str
            Default location for conversion output
        """

        if self.dicom:
            path = str(self.dicom.path).replace("DICOM", "NIfTI")
            return Path(path)

    def get_default_nifti_name(self) -> str:
        """
        Returns the default file name for a NIfTI version of this scan.

        Returns
        -------
        str
            Default file name
        """

        return str(self.id)

    def get_default_nifti_destination(self) -> Path:
        """
        Returns the default path for a NIfTI version of this scan.

        Returns
        -------
        str
            Default path for NIfTI file
        """

        directory = self.get_default_nifti_dir()
        name = self.get_default_nifti_name()
        return directory / name

    def get_bids_destination(self) -> Path:
        """
        Returns the BIDS-compatible destination of this scan's associated
        :class:`~django_mri.models.nifti.NIfTI` file.

        Returns
        -------
        pathlib.Path
            BIDS-compatible NIfTI file destination
        """

        bids_path = Bids(self).compose_bids_path()
        return bids_path

    def compile_to_bids(self, bids_path: Path):
        Bids(self).clean_unwanted_files(bids_path)
        Bids(self).fix_functional_json(bids_path)

    def dicom_to_nifti(
        self,
        destination: Path = None,
        compressed: bool = True,
        generate_json: bool = True,
    ) -> NIfTI:
        """
        Convert this scan from DICOM to NIfTI using _dcm2niix.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Parameters
        ----------
        destination : Path, optional
            The desired path for conversion output (the default is None, which
            will create the file in some default location)

        Raises
        ------
        AttributeError
            If no DICOM series is related to this scan

        Returns
        -------
        NIfTI
            A :class:`django_mri.NIfTI` instance referencing the conversion
            output
        """

        if self.sequence_type and self.sequence_type.title == "Localizer":
            warnings.warn("Localizer scans may not converted to NIfTI.")
            return None
        if self.dicom:
            dcm2niix = Dcm2niix()
            if destination is None:
                try:
                    destination = self.get_bids_destination()
                except ValueError as e:
                    print(e.args)
                    destination = self.get_default_nifti_destination()
            elif not isinstance(destination, Path):
                destination = Path(destination)
            destination.parent.mkdir(exist_ok=True, parents=True)
            nifti_path = dcm2niix.convert(
                self.dicom.get_path(),
                destination,
                compressed=compressed,
                generate_json=generate_json,
            )
            self.compile_to_bids(destination)
            nifti = NIfTI.objects.create(path=nifti_path, is_raw=True)
            return nifti
        else:
            message = messages.DICOM_TO_NIFTI_NO_DICOM.format(scan_id=self.id)
            raise AttributeError(message)

    def warn_subject_mismatch(self, subject):
        """
        Warns the user regarding a mismatch in subject identity.

        Parameters
        ----------
        subject : django.db.models.Model
            Suggested subject identity
        """

        message = messages.SUBJECT_MISMATCH.format(
            scan_id=self.id,
            existing_subject_id=self.subject.id,
            assigned_subject_id=subject.id,
        )
        warnings.warn(message)

    def suggest_subject(self, subject) -> None:
        if subject is not None:
            # If this scan actually belongs to a different subject (and
            # self.subject is not None), warn the user and return.
            mismatch = self.subject != subject
            if self.subject and mismatch:
                self.warn_subject_mismatch(subject)
            # Else, if this scan is not assigned to any subject but a subject
            # was provided (and not None), associate this scan with it.
            else:
                self.subject = subject
                self.save()

    def convert_to_mif(self) -> Path:
        """
        Creates a *.mif* version of this scan using mrconvert_.

        .. _mrconvert:
           https://mrtrix.readthedocs.io/en/latest/reference/commands/mrconvert.html

        Returns
        -------
        Path
            Created file path
        """
        from django_mri.analysis.utils.get_mrconvert_node import get_mrconvert_node

        node, created = get_mrconvert_node()
        out_file = self.get_default_mif_path()
        if not out_file.parent.exists():
            out_file.parent.mkdir()
        return node.run(inputs={"in_file": self.nifti.path, "out_file": out_file})

    def get_default_mif_path(self) -> Path:
        """
        Returns the default *.mif* path for this scan.

        Returns
        -------
        Path
            Default *.mif* path
        """

        return get_mri_root() / "mif" / f"{self.id}.mif"

    @property
    def mif(self) -> Path:
        """
        Returns the *.mif* version of this scan, creating it if it doesn't
        exist.

        Returns
        -------
        Path
            *.mif* file path

        See Also
        --------
        * :meth:`convert_to_mif`
        """

        destination = self.get_default_mif_path()
        if not destination.exists():
            self.convert_to_mif()
        return destination

    @property
    def sequence_type(self) -> SequenceType:
        """
        Returns the sequence type instance fitting this scan if one exists.

        See Also
        --------
        * :meth:`infer_sequence_type`
        * :class:`django_mri.models.sequence_type.SequenceType`

        Returns
        -------
        SequenceType
            Inferred sequence type
        """

        return self.infer_sequence_type()

    @property
    def nifti(self) -> NIfTI:
        """
        Returns the associated :class:`~django_mri.models.nifti.NIfTI` instance
        if one exists, or tries to create one if it doesn't.

        Returns
        -------
        NIfTI
            Associated NIfTI instance
        """

        if not isinstance(self._nifti, NIfTI):
            self._nifti = self.dicom_to_nifti()
            self.save()
        return self._nifti
