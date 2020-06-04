from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .fixtures import (
    SIEMENS_DWI_SERIES_PATH,
    LONELY_FILES_PATH,
)
from django_mri.models import Scan
from django_dicom.models import Image
from django.db.models import signals
from .models import Subject
from django.contrib.auth import get_user_model
import sys
import os
import factory


# class LoggedOutScanViewTestCase(TestCase):
#     @classmethod
#     @factory.django.mute_signals(signals.post_save)
#     def setUpTestData(cls):
#         """
#         Creates instances to be used in the tests.
#         For more information see Django's :class:`~django.test.TestCase` documentation_.

#         .. _documentation: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
#         """
#         cls.subject = Subject.objects.create(title="TestSubject")
#         Image.objects.import_path(SIEMENS_DWI_SERIES_PATH)
#         scan, _ = Scan.objects.get_or_create(dicom=Image.objects.first().series)
#         # scan.suggest_subject(cls.subject)

#     def setUp(self):
#         self.test_instance = Scan.objects.last()

#     def test_scan_list_unautherized(self):
#         url = reverse("mri:scan-list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_scan_detail_unautherized(self):
#         url = reverse("mri:scan-detail", args=(self.test_instance.dicom.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        Subject.objects.create(title="TestSubject")
        Image.objects.import_path(SIEMENS_DWI_SERIES_PATH)
        scan, _ = Scan.objects.get_or_create(dicom=Image.objects.first().series)
        scan.subject = Subject.objects.last()
        scan.save()

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test", password="pass", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.test_scan = Scan.objects.last()

    # def test_list_view(self):
    #     response = self.client.get(reverse("mri:scan-list"))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_view(self):
        url = reverse("mri:scan-detail", args=(self.test_scan.id,))
        print(self.test_scan.subject.id)
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    # def test_scan_from_dicom_bad_request(self):
    #     url = reverse("mri:from_dicom", args=(sys.maxsize,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_scan_from_dicom_view(self):
    #     url = reverse("mri:from_dicom", args=(self.test_scan.dicom.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_scan_create(self):
    #     # # TODO figure out how to access the create function in
    #     # # the Scan_serializer and complete the test
    #     # url = "/mri/scan/"
    #     # study = Study.objects.create()
    #     # SIEMENS_DWI_SERIES_FOR_CREATE_SCAN["study_id"] = study.id
    #     # Series.objects.create(**SIEMENS_DWI_SERIES_FOR_CREATE_SCAN)
    #     # dicom = Series.objects.last()
    #     # response = self.client.post(url, data={"dicom": dicom})
    #     # self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     pass


# class LoggedOutNIfTIViewTestCase(TestCase):
#     @classmethod
#     @factory.django.mute_signals(signals.post_save)
#     def setUpTestData(cls):
#         """
#         Creates instances to be used in the tests.
#         For more information see Django's :class:`~django.test.TestCase` documentation_.

#         .. _documentation: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
#         """
#         cls.subject = Subject.objects.create(title="TestSubject")
#         Image.objects.import_path(SIEMENS_DWI_SERIES_PATH)
#         scan, _ = Scan.objects.get_or_create(dicom=Image.objects.first().series)

#     def setUp(self):
#         scan = Scan.objects.last()
#         self.test_nifti = scan.dicom_to_nifti()

#     def test_scan_list_unautherized(self):
#         url = reverse("mri:nifti-list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_scan_detail_unautherized(self):
#         url = reverse("mri:nifti-detail", args=(self.test_nifti.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class LoggedInNIfTIViewTestCase(APITestCase):
#     @classmethod
#     @factory.django.mute_signals(signals.post_save)
#     def setUpTestData(cls):
#         """
#         Creates instances to be used in the tests.
#         For more information see Django's :class:`~django.test.TestCase` documentation_.

#         .. _documentation: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
#         """
#         # cls.subject = Subject.objects.create(title="TestSubject")
#         Image.objects.import_path(SIEMENS_DWI_SERIES_PATH)
#         scan, _ = Scan.objects.get_or_create(dicom=Image.objects.first().series)
#         # scan.suggest_subject(cls.subject)

#     def setUp(self):
#         User = get_user_model()
#         self.user = User.objects.create_user(
#             username="test", password="pass", is_staff=True
#         )
#         self.client.force_authenticate(self.user)
#         scan = Scan.objects.last()
#         self.test_nifti = scan.dicom_to_nifti()

#     def test_list_view(self):
#         response = self.client.get(reverse("mri:nifti-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_detail_view(self):
#         url = reverse("mri:nifti-detail", args=(self.test_nifti.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
