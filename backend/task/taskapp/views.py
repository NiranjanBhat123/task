from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Project, User
from .serializers import ProjectSerializer, UserRegistrationSerializer,UserSerializer,TaskSerializer

class IsOwnerOrContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.contributors.all()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrContributor]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user) | Project.objects.filter(contributors=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserRegistrationView(viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer

    def create(self, request):
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