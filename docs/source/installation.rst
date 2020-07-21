Installation
============

    1. Install from `PyPi <https://pypi.org/project/django-mri/>`_:

        .. code-block:: console

            $ pip install django_mri

    2. Add "django_mri" and "django_dicom" to your project's INSTALLED_APPS_
       setting:

        .. code-block:: python
            :caption: <project>/settings.py

            INSTALLED_APPS = [
                ...,
                "django_dicom",
                "django_mri",
            ]

        .. _INSTALLED_APPS:
           https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-INSTALLED_APPS

        .. note::
            *django_mri* uses django_dicom_ to manage data imported as DICOM
            files.

            .. _django_dicom:
               https://django-dicom.readthedocs.io/en/latest/

    3. Include the app's URLconf in your prject *urls.py*:

        .. code-block:: python
            :caption: <project>/urls.py

            urlpatterns = [
                ...,
                path("api/", include("django_mri.urls", namespace="mri")),
            ]

    4. Run:

        .. code-block:: console

            $ python manage.py migrate

    5. *\[Optional\]* Load preconfigured sequence types and analyses:

        .. code-block:: python
            :caption: Django shell

            >>> from django_mri.analysis.utils import load_mri_analyses
            >>> from django_mri.models import SequenceType
            >>> from django_mri.models.common_sequences import sequences

            # Create analyses and pipelines
            >>> load_mri_analyses()

            # Create common MRI sequence definitions
            >>> for sequence in sequences:
            >>>     SequenceType.objects.create(**sequence)

    6. Start the development server and visit http://127.0.0.1:8000/admin/.

    7. Visit http://127.0.0.1:8000/api/mri/.

