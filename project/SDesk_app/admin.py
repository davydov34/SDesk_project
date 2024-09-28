from django.contrib import admin
from .models import (Task,
                     Profile,
                     Status,
                     Department,
                     StaffPosition,
                     PermissionLevel)


@admin.register(Department)
class DepartmentModelAdmin(admin.ModelAdmin):
    __module__ = Department

@admin.register(StaffPosition)
class DepartmentModelAdmin(admin.ModelAdmin):
    __module__ = StaffPosition

@admin.register(PermissionLevel)
class DepartmentModelAdmin(admin.ModelAdmin):
    __module__ = PermissionLevel

# Register your models here.
@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    __module__ = Task

@admin.register(Status)
class StatusModelAdmin(admin.ModelAdmin):
    __module__ = Status

@admin.register(Profile)
class StaffModelAdmin(admin.ModelAdmin):
    __module__ = Profile