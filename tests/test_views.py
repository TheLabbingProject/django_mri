import factory
import sys
import shutil
from pathlib import Path

from django.test import TestCase
from django.urls import reverse
from django_mri.models import Scan
from django_dicom.models import Image, Series
from django.db.models import signals
from django_dicom.models.utils.utils import get_group_model
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import SubjectFactory
from tests.fixtures import SIEMENS_DWI_SERIES_PATH, IMPORTED_DIR
from django_mri.models.sequence_type import SequenceType
from django_mri.models.common_sequences import sequences

User = get_user_model()
Group = get_group_model()


class LoggedOutScanViewTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        """
        Creates instances to be used in the tests.


        References
        ----------
        * `Django's TestCase documentation`_

        .. _Django's TestCase documentation:
           https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
        """

        Scan.objects.all().delete()
        subject = SubjectFactory()
        Image.objects.import_path(SIEMENS_DWI_SERIES_PATH)
        series = Series.objects.first()
        Scan.objects.create(dicom=series, subject=subject)

    # @classmethod
    # def tearDownClass(cls):
    #     for subdir in Path(IMPORTED_DIR).iterdir():
    #         shutil.rmtree(subdir)

    def setUp(self):
        self.test_instance = Scan.objects.last()

    def test_scan_list_unautherized(self):
        url = reverse("mri:scan-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_scan_detail_unautherized(self):
        url = reverse("mri:scan-detail", args=(self.test_instance.dicom.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_scan_from_file_unautherized(self):
    #     url = reverse("mri:from_file")
    #     subject = Subject.objects.last()
    #     response = self.client.post(
    #         url,
    #         data={
    #             "file": open(os.path.join(LONELY_FILES_PATH, "001.dcm"), "rb"),
    #             "subject_id": subject.id,
    #         },
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LoggedInScanViewTestCase(APITestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        """
        Creates instances to be used in the tests.
        For more information see Django's :class:`~django.test.TestCase` documentation_.

        .. _documentation: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
        """

        Scan.objects.all().delete()
        subject = SubjectFactory()
        Image.objects.import_path(SIEMENS_DWI_SERIES_PATH)
        Scan.objects.create(dicom=Image.objects.first().series, subject=subject)
        cls.user = User.objects.create_user(
            username="test", password="pass", is_staff=True
        )

    def setUp(self):
        self.test_scan = Scan.objects.last()

    def test_list_view(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("mri:scan-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_view(self):
        self.client.force_authenticate(self.user)
        url = reverse("mri:scan-detail", args=(self.test_scan.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_scan_from_file_dcm_view(self):
    #     url = reverse("mri:from_file")
    #     subject = Subject.objects.last()
    #     f = open(os.path.join(LONELY_FILES_PATH, "001.dcm"), "rb")
    #     response = self.client.post(url, data={"file": f, "subject_id": subject.id})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_scan_from_file_zip_view(self):
    #     url = reverse("mri:from_file")
    #     subject = Subject.objects.last()
    #     f = open(os.path.join(LONELY_FILES_PATH, "001.zip"), "rb")
    #     response = self.client.post(url, data={"file": f, "subject_id": subject.id})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_scan_from_dicom_bad_request(self):
        self.client.force_authenticate(self.user)
        url = reverse("mri:from_dicom", args=(sys.maxsize,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_scan_from_dicom_view(self):
        self.client.force_authenticate(self.user)
        url = reverse("mri:from_dicom", args=(self.test_scan.dicom.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @factory.django.mute_signals(signals.post_save)
    def test_scan_from_dicom_view_seperate_dicom(self):
        series = Series.objects.create(uid="123")
        self.client.force_authenticate(self.user)
        url = reverse("mri:from_dicom", args=(series.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_scan_plot_view(self):
    #     self.client.force_authenticate(self.user)
    #     url = reverse("mri:plot", args=(self.test_scan.dicom.pk,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_scan_create(self):
    # # TODO figure out how to access the create function in
    # # the Scan_serializer and complete the test
    # url = "/mri/scan/"
    # study = Study.objects.create()
    # SIEMENS_DWI_SERIES_FOR_CREATE_SCAN["study_id"] = study.id
    # Series.objects.create(**SIEMENS_DWI_SERIES_FOR_CREATE_SCAN)
    # dicom = Series.objects.last()
    # response = self.client.post(url, data={"dicom": dicom})
    # self.assertEqual(response.status_code, status.HTTP_200_OK)
    # pass


class LoggedOutNIfTIViewTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        """
        Creates instances to be used in the tests.
        For more information see Django's :class:`~django.test.TestCase` documentation_.

        .. _documentation: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
        """
        # subject = Subject.objects.create()
        Scan.objects.all().delete()
        subject = SubjectFactory()
        Image.objects.import_path(SIEMENS_DWI_SERIES_PATH)
        scan = Scan.objects.create(dicom=Image.objects.first().series, subject=subject)
        cls.test_nifti = scan.nifti

    def test_scan_list_unautherized(self):
        url = reverse("mri:nifti-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_scan_detail_unautherized(self):
        url = reverse("mri:nifti-detail", args=(self.test_nifti.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LoggedInNIfTIViewTestCase(APITestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        """
        Creates instances to be used in the tests.
        For more information see Django's :class:`~django.test.TestCase` documentation_.

        .. _documentation: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
        """
        # subject = Subject.objects.create()
        Scan.objects.all().delete()
        subject = SubjectFactory()
        Image.objects.import_path(SIEMENS_DWI_SERIES_PATH)
        Scan.objects.create(dicom=Image.objects.first().series, subject=subject)
        cls.user = User.objects.create_user(
            username="test", password="pass", is_staff=True
        )
        scan = Scan.objects.last()
        cls.test_nifti = scan.nifti

    def test_list_view(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("mri:nifti-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_view(self):
        self.client.force_authenticate(self.user)
        url = reverse("mri:nifti-detail", args=(self.test_nifti.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
