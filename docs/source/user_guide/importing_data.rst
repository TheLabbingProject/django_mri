Importing Data
==============

Currently, *django_mri* supports importing raw data only as DICOM files.
To import a directory of DICOM data, simply run:

.. code-block:: python
    :caption: Django shell

    >>> from django_mri.models import Scan

    >>> path = "/path/to/dicom/archive/"
    >>> Scan.objects.import_path(path)
    Importing DICOM data: <####>image [<##:##>, <##.##>image/s]

    Successfully imported DICOM data from <path>!
    Created:        <####>
