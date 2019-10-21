from rest_framework import serializers

from TiAPI.models import UserModel, CodeModel


class RequestAddCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50, required=True)
    username = serializers.CharField(max_length=100, required=True)


class RequestAddUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    name = serializers.CharField(max_length=100, required=True)
    surname = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(max_length=100, required=True)


class RequestUserCodesSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeModel
        fields = "__all__"
