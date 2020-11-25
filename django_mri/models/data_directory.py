"""
Definition of the :class:`DataDirectory` model.
"""
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from django_mri.models.scan import Scan
from django_mri.utils.utils import get_data_share_root
from pathlib import Path


class DataDirectory(TitleDescriptionModel, TimeStampedModel):
    """
    Represents a local data directory that is periodically updated with new
    data.
    """

    path = models.FilePathField(
        path=get_data_share_root, allow_files=False, allow_folders=True
    )
    known_subdirectories = models.JSONField(default=list)

    class Meta:
        verbose_name_plural = "Data Directories"

    def __str__(self) -> str:
        """
        Returns the string representation of the instance.

        Returns
        -------
        str
            This instance's string representation
        """
        return self.title

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for this instance.
        For more information see the `Django documentation`_.

        .. _Django documentation:
           https://docs.djangoproject.com/en/3.0/ref/models/instances/#get-absolute-url

        Returns
        -------
        str
            This instance's absolute URL path
        """

        return reverse("mri:datadirectory-detail", args=[str(self.id)])

    def import_new_subdirectories(
        self, progressbar: bool = False, report: bool = False
    ) -> list:
        """
        Imports any new subdirectories under the root data directory path.

        Parameters
        ----------
        progressbar : bool
            Whether to display a progressbar or not, default is False
        report : bool
            Whether to display a sumamry report or not, default is False

        Returns
        -------
        list
            Imported subdirectory names
        """

        root = Path(self.path)
        new_subdirectories = []
        for path in root.iterdir():
            if path.is_dir() and path.name not in self.known_subdirectories:
                Scan.objects.import_path(
                    path, progressbar=progressbar, report=report
                )
                self.known_subdirectories.append(path.name)
                new_subdirectories.append(path.name)
        return new_subdirectories

    def remove_old_subdirectories(self) -> None:
        """
        Removes any old subdirectories under the root data directory path.
        """

        root = Path(self.path)
        for name in self.known_subdirectories:
            if not (root / name).is_dir():
                self.known_subdirectories.pop(name)

    def sync(self, progressbar: bool = False, report: bool = False) -> list:
        """
        Imports new subdirectories and removes old subdirectories from the root
        data directory.

        Parameters
        ----------
        progressbar : bool
            Whether to display a progressbar or not, default is False
        report : bool
            Whether to display a sumamry report or not, default is False

        Returns
        -------
        list
            Imported subdirectory names
        """

        new_subdirectories = self.import_new_subdirectories(
            progressbar=progressbar, report=report
        )
        self.remove_old_subdirectories()
        self.save()
        return new_subdirectories
