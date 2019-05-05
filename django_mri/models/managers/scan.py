from django.db import models
from django_dicom.models import Series

# from django_mri.models import NIfTI


class ScanManager(models.Manager):
    """
    A `manager <https://docs.djangoproject.com/en/2.2/topics/db/managers/>`_
    class for the :class:`~django_dicom.models.scan.Scan`_ model.
    
    """

    def get_orphan_dicom_series(self) -> models.QuerySet:
        """
        Returns :class:`~django_dicom.models.series.Series` instances with no parent
        :class:`~django_mri.models.scan.Scan` instance.
        
        Returns
        -------
        :class:`~django.db.models.QuerySet`_
            DICOM series with no affiliated :class:`~django_mri.models.scan.Scan` instance.
        """

        return Series.objects.filter(scan__isnull=True)
