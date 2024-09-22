# taskapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Task

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description', 'owner__username')
    filter_horizontal = ('contributors',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'project__name', 'assigned_to__username')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project', 'assigned_to')