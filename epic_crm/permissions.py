from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException

from epic_crm.models import User, Client, Contract, Event


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True


class IsSalesContact(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        kwargs = view.kwargs

        if user.groups.filter(name="sales").exists():            
            if view.action in ["list", "create", "mark_as_signed"]:
                return True
            elif view.action == "destroy":
                return False
            elif kwargs.get('pk'): 
                if "clients" in request.path_info:
                    client = get_object_or_404(Client, pk=kwargs.get('pk'))
                    if client.sales_contact in [request.user, None]:
                        return True
                if "contracts" in request.path_info:
                    contract = get_object_or_404(Contract, pk=kwargs.get('pk'))
                    if contract.sales_contact in [request.user, None]:
                        return True


    def has_object_permission(self, request, view, obj):

        if obj.sales_contact in [request.user, None]:
            return True


class IsSupportContact(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if Group.objects.get(name='support') in user.groups.all():
            if view.action == "list":
                return True
            elif view.kwargs.get('pk'):
                event = get_object_or_404(Event, pk=view.kwargs['pk'])
                if event.support_contact == user:
                    return True

    def has_object_permission(self, request, view, obj):

        support_team_allowed_actions = ['update']
        if "events" in request.path_info and view.action in support_team_allowed_actions:
            if obj.support_contact == request.user:
                return True
