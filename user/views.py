from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        email_or_username = self.request.data.get('email_or_username')
        password = self.request.data.get('password')
        try:
            user = User.objects.get(Q(username=email_or_username) | Q(email=email_or_username))
        except User.DoesNotExist:
            raise Http404
        if user.check_password(password):
            raise ValidationError({
                'password': ['password is incorrect']
            })
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': str(token)})


class UserApiView(CreateAPIView):
    serializer_class = UserSerializer
