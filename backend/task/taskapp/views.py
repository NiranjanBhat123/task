from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Project, User
from .serializers import ProjectSerializer, UserRegistrationSerializer, UserSerializer
from .permissions import IsOwnerOrContributor
from rest_framework.exceptions import NotFound
from django.core.exceptions import MultipleObjectsReturned

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrContributor]
    queryset = Project.objects.none()

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user) | Project.objects.filter(contributors=user)

    def get_object(self):
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
        except Project.DoesNotExist:
            raise NotFound('A project with this ID does not exist.')
        except MultipleObjectsReturned:
            print(f"Multiple projects found with ID {filter_kwargs[self.lookup_field]}")
            obj = queryset.filter(**filter_kwargs).first()
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Remove duplicates based on project ID
        unique_projects = {str(project['id']): project for project in serializer.data}.values()
        return Response(list(unique_projects))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user).data,
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )
        
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
