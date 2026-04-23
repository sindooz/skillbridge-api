from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "student"


class IsTrainer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "trainer"


class IsInstitution(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "institution"


class IsProgrammeManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "programme_manager"


class IsMonitoringOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "monitoring_officer"