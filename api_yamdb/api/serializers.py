import datetime as dt
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import (Review, Comment, User, EmailAndCode,
                            Category, Genre, Title)


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'bio', 'email', 'role']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Данный никнейм'
                                              ' уже зарегистрирован')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Данный электронный'
                                              ' адрес уже зарегистрирован')
        return value


class GetTokenSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
    expire_date = serializers.DateTimeField(required=False)

    def validate(self, validated_data):
        username = validated_data['username']
        confirm_code = validated_data['confirmation_code']
        if not EmailAndCode.objects.filter(
                username=username, confirm_code=confirm_code).exists():
            raise serializers.ValidationError('Неверный код подтверждения')
        return validated_data

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise NotFound
        return value

    class Meta:
        model = EmailAndCode
        fields = ['username', 'confirmation_code', 'expire_date']


class ConfirmEmailSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    confirm_code = serializers.CharField(required=False)
    expire_date = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        email = validated_data.get('email')
        try:
            instance = EmailAndCode.objects.get(email=email)
            return self.update(instance, validated_data)
        except ObjectDoesNotExist:
            return EmailAndCode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.confirm_code = validated_data.get(
            'confirm_code')
        instance.expire_date = validated_data.get(
            'expire_date')
        instance.save()
        return instance

    def validate_username(self, value):
        if value == 'me' or User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Данный никнейм'
                                              ' уже зарегистрирован')
        return value

    def validate_email(self, value):
        if (EmailAndCode.objects.filter(email=value).exists()
                or User.objects.filter(email=value).exists()):
            raise serializers.ValidationError('Данный электронный адрес'
                                              ' уже зарегистрирован')
        return value

    class Meta:
        model = EmailAndCode
        fields = ['username', 'email', 'confirm_code', 'expire_date']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.CharField(required=True,
                                 validators=[UniqueValidator(
                                     queryset=Genre.objects.all())])

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class ReadTitleSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    genre = GenreSerializer(many=True, source='genres')
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('category', 'genres')


class WriteTitleSerializer(serializers.ModelSerializer):

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
        source='genres'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        current_year = dt.date.today().year
        if current_year < value < 0:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Вы не можете оставить больше'
                                              ' одного отзыва на произведение')


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
