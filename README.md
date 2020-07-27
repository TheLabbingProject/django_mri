[![PyPI version](https://img.shields.io/pypi/v/django-mri.svg)](https://pypi.python.org/pypi/django-mri/)
[![PyPI status](https://img.shields.io/pypi/status/django-mri.svg)](https://pypi.python.org/pypi/django-mri/)
[![CircleCI](https://circleci.com/gh/TheLabbingProject/django_mri.svg?style=shield)](https://app.circleci.com/pipelines/github/TheLabbingProject/django-mri)
[![Documentation Status](https://readthedocs.org/projects/django-mri/badge/?version=latest)](http://django-mri.readthedocs.io/?badge=latest)
[![codecov.io](https://codecov.io/gh/TheLabbingProject/django_mri/coverage.svg?branch=master)](https://codecov.io/github/TheLabbingProject/mri?branch=master)

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
