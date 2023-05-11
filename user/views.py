from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from jobs.models import Applications
from user.serializers import UserSerializer, UserApplicationsSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserApplicationsView(generics.ListAPIView):
    """Endpoint for listing user applications by provided user_id"""

    serializer_class = UserApplicationsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Applications.objects.select_related("user").filter(
            user_id=self.kwargs.get("pk")
        )

        return queryset
