from django import forms
from django_mri.models import Scan


class ScanUpload(forms.ModelForm):
    path = forms.FileField()

    class Meta:
        model = Scan
        fields = []
