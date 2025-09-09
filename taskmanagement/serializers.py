from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import CustomUser, Task, Comment

class ListUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "role", "date_joined", "is_active"]


class CommentSerializer(ModelSerializer):
    author_full_name = ReadOnlyField(source='author.full_name') #want to get the name instead of the Id

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'author_full_name', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']


class TaskSerializer(ModelSerializer):
    assigned_to_name = ReadOnlyField(source='assigned_to.full_name')
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to', 'assigned_to_full_name', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['assigned_to', 'created_at', 'updated_at']