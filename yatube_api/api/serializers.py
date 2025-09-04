"""Сериализаторы для моделей Post, Group и Comment."""

from rest_framework import serializers
from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        """Метаданные сериализатора Post."""

        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        read_only_fields = ('author',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Метаданные сериализатора Group."""

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        """Метаданные сериализатора Comment."""

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')
