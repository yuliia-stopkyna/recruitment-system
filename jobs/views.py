from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jobs.models import Jobs
from jobs.serializers import JobSerializer
import jobs.signals


class JobsViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobSerializer
    queryset = Jobs.objects.prefetch_related("headers")

    @extend_schema(
        methods=["POST"],
        request=JobSerializer,
        responses={201: JobSerializer},
    )
    def create(self, request, *args, **kwargs):
        """Endpoint for creating job along with job headers"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        read_serializer = JobSerializer(job)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        methods=["PUT"],
        request=JobSerializer,
        responses={200: JobSerializer},
    )
    def update(self, request, *args, **kwargs):
        """Endpoint for updating job along with its job headers"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        old_job_title = instance.headers.rich_title_text
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        job.refresh_from_db()

        new_job_title = job.headers.rich_title_text
        read_serializer = JobSerializer(job)
        jobs.signals.job_updated.send(
            sender=self.__class__,
            job_id=job.id,
            old_job_title=old_job_title,
            new_job_title=new_job_title,
        )

        return Response(read_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        methods=["PATCH"],
        request=JobSerializer,
        responses={200: JobSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        """Endpoint for partial updating job along with its job headers"""
        return super().partial_update(request, *args, **kwargs)
