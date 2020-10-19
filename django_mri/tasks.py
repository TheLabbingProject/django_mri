from celery import shared_task
from django_mri.models.data_directory import DataDirectory


@shared_task(name="django_mri.import-data")
def import_data(data_directory_id: int) -> list:
    """
    Imports new data (unfamiliar subdirectories) from the provided
    :class:`~django_mri.models.data_directory.DataDirectory` instance.

    Parameters
    ----------
    data_directory_id : int
        DataDirectory instance ID

    Returns
    -------
    list
        The names of the subdirectories within the DataDirectory that were
        imported
    """

    source = DataDirectory.objects.get(id=data_directory_id)
    imported_subdirectories = source.sync(progressbar=False, report=True)
    return imported_subdirectories
