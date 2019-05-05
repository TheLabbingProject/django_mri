from django import forms


class ScanUpload(forms.Form):
    file = forms.FileField()
