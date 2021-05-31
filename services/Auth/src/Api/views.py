from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from Api.serializer import AuthUserSerializer
from typing import List


class AuthUserView(APIView):
    # TODO: esquema para autenticar os serviços que iram utilizar a autenticação
    permission_classes: List[object] = [AllowAny]

    def post(self, request, *args, **kwargs):
        auth = AuthUserSerializer(data=self.request.data)
        auth.is_valid(raise_exception=False)
        return Response({"detail": "you have permission."})