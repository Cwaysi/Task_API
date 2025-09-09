from rest_framework.serializers import ModelSerializer, ReadOnlyField, CharField
from .models import CustomUser, Task, Comment

class ListUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "role", "date_joined", "is_active"]
        read_only_fields = ["email", "full_name", "role", "date_joined", "is_active"]


"""
Using the normal create was not hashing the password, when I used
curl, it made it empty, this is an override, to create password
"""
class UserRegister(ModelSerializer):
    password = CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "role", "password"]
        extra_kwargs = {'role': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

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
        fields = ['id', 'title', 'description', 'status', 'assigned_to', 'assigned_to_name', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['assigned_to', 'created_at', 'updated_at']

class TaskStatusUpdate(ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']