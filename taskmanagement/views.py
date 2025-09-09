from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Task, Comment
from .serializers import ListUserSerializer, TaskSerializer, CommentSerializer
from .security import IsAdmin, AssignedUser, IsUser, Admin_or_Assigned


class UserListView(ReadOnlyModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class TaskView(ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # show all tasks to admin, and specific tasks to related users
        if self.request.user.is_admin():
            return Task.objects.all()
        return Task.objects.filter(assigned_to = self.request.user)
    
    """
    check permision for which user role can create, destroy, update
    or retrieve
    """
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsUser, IsAdmin]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, AssignedUser | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
    def perform_create(self, serializer):
        serializer.save()

class CommentsView(ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin():
            return Comment.objects.all()
        return Comment.objects.filter(task__assigned_to=self.request.user)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated, IsUser, IsAdmin]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin | Admin_or_Assigned]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request)