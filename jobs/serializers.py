from django.db import transaction
from rest_framework import serializers

from jobs.models import JobHeaders, Jobs


class JobHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHeaders
        fields = (
            "id",
            "job",
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
    rich_title_text = serializers.CharField(max_length=255, read_only=False)
    rich_subtitle_text = serializers.CharField(max_length=255, read_only=False)

    class Meta:
        model = Jobs
        fields = ("name", "type", "rich_title_text", "rich_subtitle_text")

    def create(self, validated_data):
        with transaction.atomic():
            rich_title_text = validated_data.pop("rich_title_text")
            rich_subtitle_text = validated_data.pop("rich_subtitle_text")
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

        rich_title_text = validated_data.get("rich_title_text")
        rich_subtitle_text = validated_data.get("rich_subtitle_text")

        job_headers = JobHeaders.objects.filter(job_id=instance.id)

        if rich_title_text:
            job_headers.update(rich_title_text=rich_title_text)

        if rich_subtitle_text:
            job_headers.update(rich_subtitle_text=rich_subtitle_text)

        return instance
