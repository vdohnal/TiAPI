from datetime import timedelta

import rest_framework_simplejwt.views as jwt_views
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status


class JWTCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(request.path)
        login_url = settings.LOGIN_URL
        redirect_url = request.path if request.path != login_url else settings.LOGIN_REDIRECT_URL
        factory = RequestFactory()

        self.copy_request_data(request)
        refresh = request.COOKIES.get('refresh_token')
        access = request.COOKIES.get('login_token')

        if not refresh:
            if request.path == login_url:
                return self.get_response(request)
            print('REDIRECT TO LOGIN URL')
            return redirect(f"{login_url}?next={redirect_url}")
        self.load_jwt_token(request, access)

        jwt_request = factory.post(reverse('token_validate'), data={'token': access},
                                   content_type='application/json')

        ver_response = jwt_views.TokenVerifyView.as_view()(jwt_request)
        # print(ver_response, ver_response.status_code, ver_response.data)
        if ver_response.status_code == status.HTTP_200_OK:
            print("ACCESS TOKEN OK")
            # print(request.GET)
            return self.get_response(request)

        print("ACCESS TOKEN NOT OK")

        jwt_request = factory.post(reverse('token_refresh'), data={'refresh': refresh},
                                   content_type='application/json')
        ref_response = jwt_views.TokenRefreshView.as_view()(jwt_request)
        # print(ref_response, ref_response.status_code, ref_response.data)
        if ref_response.status_code == status.HTTP_200_OK:
            access = ref_response.data['access']
            self.load_jwt_token(request, access)
            # print(request.GET)
            response = self.get_response(request)
            response.set_cookie('login_token',
                                access,
                                max_age=settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME',
                                                                timedelta(seconds=5)).total_seconds(),
                                # max_age=timedelta(seconds=5).total_seconds(),
                                httponly=True,
                                )
            return response
        return redirect(login_url)

    @staticmethod
    def copy_request_data(request):
        if request.method == 'GET':
            request.GET = request.GET.copy()
        else:
            request.POST = request.POST.copy()

    @staticmethod
    def load_jwt_token(request, access):
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {access}"

    # @staticmethod
    # def add_redirect_url(request, target):
    #     print(f'SET REDIRECT URL TO {target}')
    #     if request.method == 'GET':
    #         request.GET['next'] = target if request.GET.get('next') is None else request.GET['next']
    #     else:
    #         request.POST['next'] = target if request.POST.get('next') is None else request.POST['next']
