from rest_framework import serializers
from .models import User, Project, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    contributors = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'contributors', 'tasks']

    def create(self, validated_data):
        owner = self.context['request'].user
        contributors_data = self.context['request'].data.get('contributors', [])
        tasks_data = self.context['request'].data.get('tasks', [])

        project = Project.objects.create(owner=owner, **validated_data)

        for contributor_id in contributors_data:
            contributor = User.objects.get(id=contributor_id)
            project.contributors.add(contributor)

        for task_data in tasks_data:
            assigned_to_id = task_data.pop('assigned_to', None)
            assigned_to = User.objects.get(id=assigned_to_id) if assigned_to_id else None
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