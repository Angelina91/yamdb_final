from datetime import date

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import ReviewUser
from users.validators import validate_username_not_me


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message='Такой slug уже есть в базе данных',
            )
        ]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Genre.objects.all(),
                message='Такой slug уже есть в базе данных',
            )
        ]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class GetTitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )
        model = Title

    def get_rating(self, obj):
        return Review.objects.filter(title=obj.id).aggregate(
            Avg('score'))['score__avg']


class PostPatchTitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    genre = SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title

    def validate_year(self, value):
        this_year = date.today().year
        if value > this_year:
            raise serializers.ValidationError('Сверьте год выпуска')
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        GenreTitle.objects.bulk_create(
            [GenreTitle(genre=genre, title=title) for genre in genres]
        )
        return title

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializers = GetTitleSerializer(instance, context=context)
        return serializers.data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs['title_id']
            if Review.objects.filter(
                author=author, title_id=title_id
            ).exists():
                raise serializers.ValidationError('Вы уже осталяли отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Comment


class ReviewUserSerializer(serializers.ModelSerializer):
    """Получение данных пользователя"""
    class Meta:
        model = ReviewUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class CreateUserSerializer(serializers.ModelSerializer):
    """Создание нового пользователя"""
    class Meta:
        model = ReviewUser
        fields = ('username', 'email')


class CreateTokenSerializer(serializers.Serializer):
    """Создание токена"""
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username_not_me, ],
    )
