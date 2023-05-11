from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jobs.models import Jobs
from jobs.serializers import JobRetrieveSerializer, JobWriteSerializer


class JobsViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    queryset = Jobs.objects.prefetch_related("headers")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return JobRetrieveSerializer
        return JobWriteSerializer

    @extend_schema(
        methods=["POST"],
        request=JobWriteSerializer,
        responses={201: JobRetrieveSerializer},
    )
    def create(self, request, *args, **kwargs):
        """Endpoint for creating job along with job headers"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        read_serializer = JobRetrieveSerializer(job)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        methods=["PUT"],
        request=JobWriteSerializer,
        responses={200: JobRetrieveSerializer},
    )
    def update(self, request, *args, **kwargs):
        """Endpoint for updating job along with its job headers"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        job.refresh_from_db()
        read_serializer = JobRetrieveSerializer(job)

        return Response(read_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        methods=["PATCH"],
        request=JobWriteSerializer,
        responses={200: JobRetrieveSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        """Endpoint for partial updating job along with its job headers"""
        return super().partial_update(request, *args, **kwargs)
