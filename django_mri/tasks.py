from celery import shared_task
from django_mri.models.data_directory import DataDirectory


@shared_task(name="django_mri.import-data")
def import_data(data_directory_id: int) -> None:
    source = DataDirectory.objects.get(id=data_directory_id)
    imported_subdirectories = source.sync(progressbar=False, report=True)
    return {"imported": imported_subdirectories}
