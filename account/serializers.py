from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=32)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=32, required=True)
    last_name = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validated_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email is already taken <3')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('<><><><><><> dude passwords are not similar <><><><><><>')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('<><><><><><> dude user wasn\'t found :( <><><><><><>')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('<><><><><><> dude code is incorrect :( <><><><><><>')
        return attrs

    def activate(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('<><><><><><> dude user wasn\'t found <><><><><><>')
        return email

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(username=email, password=password, request=request)
            if not user:
                raise serializers.ValidationError('<><><><><><> dude password is not correct <><><><><><>')
        else:
            raise serializers.ValidationError('<><><><><><> dude type ur email or password <><><><><><>')
        attrs.update({'user': user})
        return attrs


class HomeSerializer(serializers.Serializer):

    def validated(self, attrs):
        token = attrs.get('token')
        if token:
            return attrs
        raise serializers.ValidationError('there must be token in data')

    def check(self, attrs):
        token = attrs.get('token')
        if Token.objects.filter(key=token).exists:
            return token
        raise serializers.ValidationError('token wasnt found and user is not authenticated')
