from django import forms
from django_mri.models import Scan
from django_mri.widgets import BootstrapDateTimePickerInput


class ScanReview(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M:%S"],
        widget=BootstrapDateTimePickerInput,
        required=False,
    )

    class Meta:
        model = Scan
        exclude = ["is_updated_from_dicom", "_nifti", "dicom"]
        localized_fields = ("time",)
        labels = {"subject_id": "Subject ID"}
