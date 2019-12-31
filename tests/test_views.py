from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .fixtures import SIEMENS_DWI_SERIES_PATH
from django_mri.data_import import LocalImport
from django_mri.models import Scan, NIfTI
from .models import Subject, Group
from django.contrib.auth import get_user_model


class LoggedOutScanViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Creates instances to be used in the tests.
        For more information see Django's :class:`~django.test.TestCase` documentation_.

        .. _documentation: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
        """
        cls.subject = Subject.objects.create()
        LocalImport(cls.subject, SIEMENS_DWI_SERIES_PATH).run()

    def setUp(self):
        self.test_instance = Scan.objects.last()

    def test_scan_list_unautherized(self):
        url = reverse("mri:scan-list")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_scan_detail_unautherized(self):
        url = reverse("mri:scan-detail", args=(self.test_instance.dicom.id,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LoggedInImageViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Creates instances to be used in the tests.
        For more information see Django's :class:`~django.test.TestCase` documentation_.

        .. _documentation: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#testcase
        """
        cls.group = Group()
        cls.subject = Subject.objects.create()
        LocalImport(cls.subject, SIEMENS_DWI_SERIES_PATH).run()

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("test", "pass", is_staff=True)
        self.client.login()
        self.test_instance = Scan.objects.last()

    def test_list_view(self):
        response = self.client.get(reverse("mri:scan-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_view(self):
        url = reverse("mri:scan-detail", args=(self.test_instance.dicom_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
