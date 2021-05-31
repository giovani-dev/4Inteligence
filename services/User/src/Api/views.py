from typing import List
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from Api.serializer import (
    ProfileSerializer, 
    ProfileDetailSerializer
)
from Api.permissions import (
    IsADM,
    IsUser
)
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
import django.core.exceptions as django_exceptions
from util import base_view
from Api.models import Profile
from util.cep import Cep


class UserCreateView(CreateAPIView):
    permission_classes: List[object] = [AllowAny]
    serializer_class: object = ProfileSerializer

    def post(self, request, *args, **kwargs):
        serial = ProfileSerializer(
            data=self.request.data,
            context={
                    'cep': Cep(self.request.data.get('cep', None)),
                    'request': self.request
                }
            )
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.data)


class UserListView(base_view.GenericListView):
    permission_classes: List[object] = [IsADM]
    serializer_class: object = ProfileDetailSerializer

    def get_queryset(self) -> object:
        self.queryset = Profile.objects.filter(login__is_active=True).order_by('-registration_date')
        return super(UserListView, self).get_queryset()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes: List[object] = [IsADM or IsUser]
    serializer_class: object = ProfileDetailSerializer

    def get_object(self) -> object:
        try:
            return Profile.objects.get(identifier=self.kwargs['identifier'])
        except (Profile.DoesNotExist, django_exceptions.ValidationError):
            raise NotFound(detail="This user does not exists.")


    def put(self, request, *args, **kwargs):
        serial = ProfileDetailSerializer(
            self.get_object(),
            data=self.request.data,
            context={
                    'cep': Cep(self.request.data.get('cep', None)),
                    'request': self.request
                }
            )
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance.login)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)