from rest_framework import serializers
from .models import User
from .utils import get_today_total_age


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField()
    password = serializers.CharField(required=True, write_only=True)
    photo = serializers.ImageField(required=False)
    birthday_date = serializers.DateTimeField(required=True, input_formats=['%d.%m.%Y'])

    def validate_email(self, email):
        if email and User.objects.filter(email__exact=email).exists():
            raise serializers.ValidationError("user with such email already exists")
        return email

    def validate_birthday_date(self, birthday_date):
        age = get_today_total_age(birthday_date)

        if age < 18:
            raise serializers.ValidationError("user must be at least 18 years old")

        return birthday_date

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    name = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)
    birthday_date = serializers.DateTimeField(required=False, input_formats=['%d.%m.%Y'])
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'name', 'photo', 'birthday_date', 'age')

    def get_age(self, obj):
        return get_today_total_age(obj.birthday_date)
