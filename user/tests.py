from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from jobs.models import Jobs, JobHeaders, Applications
from user.serializers import UserApplicationsSerializer


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="user", password="test12345"
        )
        self.client.force_authenticate(self.user)
        self.job1 = Jobs.objects.create(
            name="Backend Developer", type=Jobs.TypeChoices.FULL_TIME
        )
        JobHeaders.objects.create(
            job_id=self.job1.id,
            rich_title_text="<b>Backend Developer</b>",
            rich_subtitle_text="<b>Full-time vacancy</b>",
        )
        self.job2 = Jobs.objects.create(
            name="Python Developer", type=Jobs.TypeChoices.FULL_TIME
        )
        JobHeaders.objects.create(
            job_id=self.job2.id,
            rich_title_text="<b>Python Developer</b>",
            rich_subtitle_text="<b>Full-time vacancy</b>",
        )
        Applications.objects.create(job=self.job1, user=self.user)
        Applications.objects.create(job=self.job2, user=self.user)

    def test_user_applications_retrieve(self):
        response = self.client.get(
            reverse("user:user-applications", args=[self.user.id])
        )
        applications = Applications.objects.filter(user_id=self.user.id)
        serializer = UserApplicationsSerializer(applications, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
