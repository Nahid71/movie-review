from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        read_only=False, required=True, validators=[validate_password],
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(
        read_only=False, required=True, style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] == attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        if username_or_email and password:
            user = None
            if '@' in username_or_email:
                # User provided email address
                user_obj = User.objects.filter(email=username_or_email).first()
                user = user_obj if user_obj and user_obj.check_password(password) else None
            else:
                # User provided username
                user = authenticate(username=username_or_email, password=password)
            if user:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Invalid username or password')
        else:
            raise serializers.ValidationError('Username/email and password required')

    def create(self, validated_data):
        user = validated_data['user']

        # Generate a new token for the user
        token, created = Token.objects.get_or_create(user=user)

        return {
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }