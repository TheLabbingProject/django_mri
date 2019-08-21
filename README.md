# _django_mri_

A django app to manage MRI data.

Currently only supports data in the [DICOM](https://www.dicomstandard.org/) format, and will soon also support [NIfTI](https://nifti.nimh.nih.gov/).

> This app is being built and maintained as part of the [_pylabber_](https://github.com/ZviBaratz/pylabber) project.

## Quick start

1. Add _django_mri_ and _django_dicom_ to your INSTALLED_APPS setting:

```python
    INSTALLED_APPS = [
        ...
        'django_dicom',
        'django_mri',
    ]
```

2. Include the dicom URLconf in your project urls.py:

```python
    path("api/", include("django_mri.urls", namespace="mri")),

    # Optional:
    path("api/", include("django_dicom.urls", namespace="dicom")),
    # if you would like to also expose the django_dicom API.
```

3. Run `python manage.py migrate` to create the dicom models.

4. Start the development server and visit http://127.0.0.1:8000/admin/.

5. Visit http://127.0.0.1:8000/mri/.
