"""ViewSets для моделей Post, Group и Comment."""

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для создания, редактирования и удаления постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Сохраняет пост с текущим пользователем как автором."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Разрешает редактирование только автору поста."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Разрешает удаление только автору поста."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено')
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для чтения информации о группах."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для управления комментариями к постам."""

    serializer_class = CommentSerializer

    def get_queryset(self):
        """Возвращает комментарии, относящиеся к конкретному посту."""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """Создаёт комментарий от текущего пользователя к посту."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """Разрешает редактирование только автору комментария."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого комментария запрещено')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Разрешает удаление только автору комментария."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого комментария запрещено')
        super().perform_destroy(instance)
