Installation
============

    1. Install from `PyPi <https://pypi.org/project/django-mri/>`_:

        .. code-block:: console

            $ pip install django_mri

    2. Add "django_mri" to your project's INSTALLED_APPS_ setting:

        .. code-block:: python
            :caption: settings.py

            INSTALLED_APPS = [
                ...,
                "django_mri",
            ]

        .. _INSTALLED_APPS:
           https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-INSTALLED_APPS

    3. Include the app's URLconf in your prject *urls.py*:

        .. code-block:: python
            :caption: urls.py

            urlpatterns = [
                ...,
                path("api/", include("django_mri.urls", namespace="mri")),
            ]

    4. Run:

        .. code-block:: console

            $ python manage.py migrate

    5. Start the development server and visit http://127.0.0.1:8000/admin/.

    6. Visit http://127.0.0.1:8000/api/mri/.

