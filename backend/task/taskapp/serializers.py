from rest_framework import serializers
from .models import Project, Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    tasks = TaskSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'contributors', 'tasks', 'created_at', 'updated_at']

    def create(self, validated_data):
        contributors_data = validated_data.pop('contributors', [])
        tasks_data = validated_data.pop('tasks', [])

        project = Project.objects.create(**validated_data)

        for contributor in contributors_data:
            project.contributors.add(contributor)

        for task_data in tasks_data:
            assigned_to = task_data.pop('assigned_to', None)
            Task.objects.create(project=project, assigned_to=assigned_to, **task_data)

        return project
    

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user