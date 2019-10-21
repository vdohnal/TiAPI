from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *


class GetUserCodes(ListAPIView):

    serializer_class = CodeSerializer

    def get_queryset(self):
        return CodeModel.objects.filter(user__username=self.kwargs.get('username')).all()

    @swagger_auto_schema(
        operation_description="Lists all codes for the user from the database.",
        query_serializer=RequestUserCodesSerializer,
        responses={
            status.HTTP_200_OK: serializer_class(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error.",
            status.HTTP_422_UNPROCESSABLE_ENTITY: "Invalid input arguments."
        }
    )
    def get(self, request, *args, **kwargs):

        serializer = RequestUserCodesSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=422)

        try:
            self.kwargs['username'] = request.query_params.get('username')
            serializer = self.get_serializer(self.get_queryset(), many=True)
        except Exception:
            return Response(status=500)

        return Response(serializer.data, status=200)


class GetUsers(ListAPIView):
    serializer_class = None
    queryset = UserModel.objects.all()

    @swagger_auto_schema(
        operation_description="Lists all users from the database.",
        query_serializer=None,
        responses={
            status.HTTP_200_OK: CodeSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error."
        }
    )
    def get(self, request, *args, **kwargs):

        try:
            serializer = UserSerializer(self.get_queryset(), many=True)
        except Exception:
            return Response(status=500)

        return Response(serializer.data, status=200)


class GetCodes(ListAPIView):
    serializer_class = None

    def get_queryset(self):
        return CodeModel.objects.all()

    @swagger_auto_schema(
        operation_description="Lists all codes from the database.",
        query_serializer=None,
        responses={
            status.HTTP_200_OK: CodeSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error."
        }
    )
    def get(self, request, *args, **kwargs):

        try:
            serializer = CodeSerializer(self.get_queryset(), many=True)
        except Exception:
            return Response(status=500)

        return Response(serializer.data, status=200)


class AddCode(APIView):

    @swagger_auto_schema(
        operation_description="Adds a code to the database.",
        query_serializer=RequestAddCodeSerializer,
        responses={
            status.HTTP_201_CREATED: "Code added to database.",
            status.HTTP_422_UNPROCESSABLE_ENTITY: "Invalid input arguments.",
        }
    )
    def post(self, request, *args, **kwargs):
        query = request.data
        query_serializer = RequestAddCodeSerializer(data=query)

        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=422)

        try:
            user_obj = list(UserModel.objects.filter(username=query_serializer.data.get('username')).all())
            if len(user_obj) != 1:
                return Response(status=422)
            code = CodeModel(code=query_serializer.data.get('code'), user=user_obj[0])
            code.save()

        except Exception as e:
            print(str(e))
            return Response(status=422)

        return Response(status=201)


class AddUser(APIView):

    @swagger_auto_schema(
        operation_description="Adds a user to the database.",
        query_serializer=RequestAddUserSerializer,
        responses={
            status.HTTP_201_CREATED: "User added to database.",
            status.HTTP_422_UNPROCESSABLE_ENTITY: "Invalid input arguments.",
        }
    )
    def post(self, request, *args, **kwargs):
        query = request.data
        query_serializer = RequestAddUserSerializer(data=query)

        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=422)

        try:
            user = UserModel(username=query_serializer.data.get('username'), name=query_serializer.data.get('name'),
                             surname=query_serializer.data.get('surname'),
                             email=query_serializer.data.get('email'))
            user.save()
        except Exception as e:
            print(str(e))
            return Response(status=422)

        return Response(status=201)
