"""
Celery tasks provided by the *django_mri* app.
"""
from datetime import datetime
from pathlib import Path
from typing import Iterable, Union

from celery import shared_task
from django_analyses.models.run import Run

from django_mri.models.data_directory import DataDirectory
from django_mri.models.scan import Scan
from django_mri.models.score import Score
from django_mri.utils.utils import get_subject_model


@shared_task(name="django_mri.create-scores")
def create_scores(run_id: int):
    run = Run.objects.get(id=run_id)
    Score.objects.from_run(run)


@shared_task(name="django_mri.import-data")
def import_data(
    data_directory: Union[int, str, Path], today_only: bool = False
) -> list:
    """
    Imports new data (unfamiliar subdirectories) from the provided
    :class:`~django_mri.models.data_directory.DataDirectory` instance.

    Parameters
    ----------
    data_directory : Union[int, str, Path]
        Directory path or DataDirectory instance ID
    today_only : bool
        Whether to look for a '<year>/<month>/<day>' subdirectory to import,
        default is False

    Returns
    -------
    list
        The names of the subdirectories within the DataDirectory that were
        imported
    """

    if isinstance(data_directory, int):
        source = DataDirectory.objects.get(id=data_directory)
        imported_subdirectories = source.sync(progressbar=False, report=True)
        return imported_subdirectories
    else:
        if today_only:
            today = datetime.today()
            data_directory = (
                Path(data_directory)
                / str(today.year)
                / str(today.month)
                / str(today.day)
            )
        Scan.objects.import_path(
            data_directory, progressbar=False, report=False
        )


@shared_task(name="django_mri.build-bids-directory")
def build_bids_directory(
    subject_ids: Iterable[str], force: bool = False, persistent: bool = True
):
    Subject = get_subject_model()
    subjects = Subject.objects.filter(id__in=subject_ids)
    subjects.build_bids_directory(
        progressbar=False, force=force, persistent=persistent
    )
