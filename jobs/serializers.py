from django.db import transaction
from rest_framework import serializers

from jobs.models import JobHeaders, Jobs


class JobHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHeaders
        fields = (
            "id",
            "rich_title_text",
            "rich_subtitle_text",
            "plain_title_text",
        )


class JobSerializer(serializers.ModelSerializer):
    headers = JobHeaderSerializer(read_only=False, many=False)

    class Meta:
        model = Jobs
        fields = ("id", "name", "type", "headers")

    def create(self, validated_data):
        with transaction.atomic():
            headers = validated_data.pop("headers")
            rich_title_text = headers["rich_title_text"]
            rich_subtitle_text = headers["rich_subtitle_text"]
            job = Jobs.objects.create(**validated_data)
            JobHeaders.objects.create(
                job=job,
                rich_title_text=rich_title_text,
                rich_subtitle_text=rich_subtitle_text,
            )

            return job

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.type = validated_data.get("type", instance.type)
        instance.save()

        headers = validated_data.pop("headers", None)

        job_headers = JobHeaders.objects.filter(job_id=instance.id)

        if headers:
            rich_title_text = headers.get("rich_title_text")
            rich_subtitle_text = headers.get("rich_subtitle_text")

            if rich_title_text:
                job_headers.update(rich_title_text=rich_title_text)

            if rich_subtitle_text:
                job_headers.update(rich_subtitle_text=rich_subtitle_text)

        return instance
