from datetime import timedelta

import rest_framework_simplejwt.views as jwt_views
from django.conf import settings
from django.contrib.auth import mixins
from django.http import HttpResponseRedirect
from django.urls import resolve, Resolver404
from django.views.generic import FormView, UpdateView, RedirectView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

import TiAPI.models as models
from TiAPI.forms import UserLoginForm
from .serializers import *


class TestLogin(APIView, mixins.LoginRequiredMixin):
    login_url = settings.LOGIN_URL

    @staticmethod
    def get():
        return Response(status=200)


class JWTLogoutView(RedirectView):
    permanent = False
    query_string = False
    url = settings.LOGOUT_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        response = super().get(request, args, kwargs)
        response.delete_cookie('login_token')
        response.delete_cookie('refresh_token')
        return response


class JWTLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'auth/login.html'
    success_url = None

    def form_valid(self, form):
        # print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        if not self.success_url:
            self.success_url = self.request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        try:
            resolve(self.get_success_url())
        except Resolver404:
            self.success_url = settings.LOGIN_REDIRECT_URL
        print('CURRENT LOGIN REDIRECT', self.get_success_url())
        login_response = jwt_views.TokenObtainPairView.as_view()(self.request, username=username, password=password)
        # print('DATA----------------------------------------------------------------')
        # print(login_response, login_response.data, login_response.status_code)
        if login_response.status_code != status.HTTP_200_OK:
            return super().form_invalid(form)
            # return Response("Invalid login credentials.", status=status.HTTP_401_UNAUTHORIZED)
        if self.get_success_url() == self.request.path:
            raise ValueError(
                "Redirection loop for authenticated user detected. Check that "
                "your LOGIN_REDIRECT_URL doesn't point to a login page."
            )
        mresponse = HttpResponseRedirect(self.get_success_url())
        # mresponse.set_cookie('login_token', login_response.data.get('access'), httponly=True,
        #                      max_age=timedelta(seconds=5).total_seconds(), )
        mresponse.set_cookie('login_token', login_response.data.get('access'), httponly=True,
                             max_age=settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME',
                                                             timedelta(seconds=5)).total_seconds(), )
        mresponse.set_cookie('refresh_token', login_response.data.get('refresh'), httponly=True,
                             max_age=settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME',
                                                             timedelta(days=1)).total_seconds(), )
        return mresponse


class CodeGroupViewSet(viewsets.ModelViewSet):
    queryset = models.CodeGroupModel.objects.all()
    serializer_class = CodeGroupSerializer


class CodeViewSet(viewsets.ModelViewSet):
    queryset = models.CodeModel.objects.all()
    serializer_class = CodeSerializer


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
