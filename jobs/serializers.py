from django.db import transaction
from rest_framework import serializers

from jobs.models import JobHeaders, Jobs
from jobs.utils import send_job_created_mail, send_job_updated_mail


class JobHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHeaders
        fields = (
            "id",
            "rich_title_text",
            "rich_subtitle_text",
            "plain_title_text",
        )


class JobRetrieveSerializer(serializers.ModelSerializer):
    headers = JobHeaderSerializer(read_only=True, many=True)

    class Meta:
        model = Jobs
        fields = ("id", "name", "type", "headers")


class JobWriteSerializer(serializers.ModelSerializer):
    headers = JobHeaderSerializer(read_only=False, many=True)

    class Meta:
        model = Jobs
        fields = ("name", "type", "headers")

    def create(self, validated_data):
        with transaction.atomic():
            headers = validated_data.pop("headers")[0]
            rich_title_text = headers["rich_title_text"]
            rich_subtitle_text = headers["rich_subtitle_text"]
            job = Jobs.objects.create(**validated_data)
            JobHeaders.objects.create(
                job=job,
                rich_title_text=rich_title_text,
                rich_subtitle_text=rich_subtitle_text,
            )
            send_job_created_mail(job_id=job.id)
            return job

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.type = validated_data.get("type", instance.type)
        instance.save()

        headers = validated_data.pop("headers", None)

        job_headers = JobHeaders.objects.filter(job_id=instance.id)
        old_title_rich_text = job_headers.first().rich_title_text

        if headers:
            rich_title_text = headers[0].get("rich_title_text")
            rich_subtitle_text = headers[0].get("rich_subtitle_text")

            if rich_title_text:
                job_headers.update(rich_title_text=rich_title_text)
            else:
                rich_title_text = old_title_rich_text

            if rich_subtitle_text:
                job_headers.update(rich_subtitle_text=rich_subtitle_text)
        else:
            rich_title_text = old_title_rich_text

        send_job_updated_mail(
            job_id=instance.id,
            old_title_rich_text=old_title_rich_text,
            new_title_rich_text=rich_title_text,
        )

        return instance
