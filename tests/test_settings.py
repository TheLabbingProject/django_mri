import environ
import os


env = environ.Env(
    DB_NAME=(str, "django_mri"),
    DB_USER=(str, ""),
    DB_PASSWORD=(str, ""),
    DB_HOST=(str, "localhost"),
    DB_PORT=(int, 5432),
    APP_IP=(str, "127.0.0.1"),
)
environ.Env.read_env()

DEBUG = False
ALLOWED_HOSTS = "*"
SECRET_KEY = "sa8!1ep_9#36qw@i-3j(a4uikiobleh03jl8v_3!n^^dsm9oyc"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "django_mri",
    "django_dicom",
    "django_analyses",
    "tests",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ]
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = (os.path.join(BASE_DIR, "static"),)

MEDIA_ROOT = os.path.join(BASE_DIR, "tests")
MEDIA_URL = "/media/"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

ANALYSIS_BASE_PATH = os.path.join(BASE_DIR, "media", "analysis")

ROOT_URLCONF = "tests.urls"

SUBJECT_MODEL = "tests.Subject"
STUDY_GROUP_MODEL = "tests.Group"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

MIGRATION_MODULES = {
    "tests": "tests.migrations",
    "django_mri": "django_mri.migrations",
}

KEEP_ORIGINAL_DICOM = True
DICOM_IMPORT_MODE = "minimal"
TESTING_MODE = True
APP_IP=env("APP_IP")
