from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from jobs.models import Jobs, JobHeaders
from jobs.serializers import JobSerializer

JOB_CREATE_URL = reverse("jobs:jobs-list")
JOB_DETAIL_URL = reverse("jobs:jobs-detail", args=[1])


class UnauthenticatedJobTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        job = Jobs.objects.create(
            name="Backend Developer", type=Jobs.TypeChoices.FULL_TIME
        )
        JobHeaders.objects.create(
            job_id=job.id,
            rich_title_text="<b>Backend Developer</b>",
            rich_subtitle_text="<b>Full-time vacancy</b>",
        )

    def test_auth_required(self):
        self.client = APIClient()
        response = self.client.get(JOB_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedJobTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        job = Jobs.objects.create(
            name="Backend Developer", type=Jobs.TypeChoices.FULL_TIME
        )
        JobHeaders.objects.create(
            job_id=job.id,
            rich_title_text="<b>Backend Developer</b>",
            rich_subtitle_text="<b>Full-time vacancy</b>",
        )

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="user", password="test12345"
        )
        self.client.force_authenticate(self.user)

        self.job = Jobs.objects.get(id=1)

    def test_job_retrieve(self):
        response = self.client.get(JOB_DETAIL_URL)
        serializer = JobSerializer(self.job)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_job_create(self):
        job_data = {
            "name": "Frontend Developer",
            "type": "full-time",
            "headers": {
                "rich_title_text": "<b>Frontend Developer</b>",
                "rich_subtitle_text": "<b>Full-time</b>",
            },
        }
        response_post = self.client.post(JOB_CREATE_URL, data=job_data, format="json")
        new_job = Jobs.objects.get(name=job_data["name"])
        new_job_url = reverse("jobs:jobs-detail", args=[new_job.id])
        response_get = self.client.get(new_job_url)
        serializer = JobSerializer(new_job)

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response_get.data)

    def test_job_partial_update(self):
        update_data = {"headers": {"rich_title_text": "<p>Backend Developer</p>"}}
        response = self.client.patch(JOB_DETAIL_URL, data=update_data, format="json")
        serializer = JobSerializer(self.job)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.job.headers.rich_title_text, update_data["headers"]["rich_title_text"]
        )
        self.assertEqual(response.data, serializer.data)

    def test_job_update(self):
        update_data = {
            "name": "Frontend Developer",
            "type": "full-time",
            "headers": {
                "rich_title_text": "<b>Frontend Developer</b>",
                "rich_subtitle_text": "<b>Full-time</b>",
            },
        }
        response = self.client.put(JOB_DETAIL_URL, data=update_data, format="json")
        job = Jobs.objects.get(id=1)
        serializer = JobSerializer(job)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(job.name, update_data["name"])
        self.assertEqual(response.data, serializer.data)

    def test_job_delete(self):
        response = self.client.delete(JOB_DETAIL_URL)
        job = Jobs.objects.filter(id=1)
        job_headers = JobHeaders.objects.filter(job_id=1)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(job)
        self.assertFalse(job_headers)
