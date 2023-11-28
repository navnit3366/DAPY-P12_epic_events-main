from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from epic_crm.models import User, Client, Contract, Event
from epic_crm.permissions import IsAdmin, IsSalesContact, IsSupportContact
from epic_crm.filters import ClientFilter, ContractFilter, EventFilter
from . import serializers


class MultipleSerializerMixin:
    """Mixin to distinguish list from detail serializer."""

    detail_serializer_class = None

    def get_serializer_class(self):
        detail_serializer_actions = ['retrieve', 'update', 'partial_update', 'create']
        if self.action in detail_serializer_actions and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.UserListSerializer
    detail_serializer_class = serializers.UserDetailSerializer
    permission_classes = (IsAdmin, )

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class ClientViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.ClientListSerializer
    detail_serializer_class = serializers.ClientDetailSerializer
    permission_classes = [IsAdmin|IsSalesContact|IsSupportContact]
    filterset_class = ClientFilter

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            if Group.objects.get(name='sales') in user.groups.all():
                queryset = Client.objects.filter(Q(sales_contact=user) | Q(sales_contact__isnull=True))
            elif Group.objects.get(name='support') in user.groups.all():
                queryset = Client.objects.filter(events__support_contact=user)
            else:
                raise APIException('You currently don\t belong to any authorized team, please contact an admin to be added to sales or support team.')
        else:
            queryset = Client.objects.all()

        return queryset


class ContractViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.ContractListSerializer
    detail_serializer_class = serializers.ContractDetailSerializer
    permission_classes = [IsAdmin|IsSalesContact, ]
    filterset_class = ContractFilter

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            queryset = Contract.objects.filter(sales_contact=self.request.user)
        else:
            queryset = Contract.objects.all()

        return queryset

    
    def create(self, request):        
        data = request.data.copy()
        data['sales_contact'] = request.user.id
        data['is_signed'] = 'false'

        serialized_data = self.detail_serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        client = get_object_or_404(Client, pk=serialized_data.data.get('client'))
        if client.sales_contact is None:
            client.sales_contact = request.user
            client.save()

        return Response(serialized_data.data)

    def partial_update(self, request, pk=None):
        contract = get_object_or_404(Contract, pk=pk)

        serialized_data = self.detail_serializer_class(contract, data=request.data, partial=True)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response(serialized_data.data)

    @action(detail=True, methods=['post'])
    def mark_as_signed(self, request, pk=None):
        contract = get_object_or_404(Contract, pk=pk)
        data = request.data.copy()
        data['client'] = contract.client.id

        if not contract.is_signed:            
            new_event = serializers.EventDetailSerializer(data=data)
            new_event.is_valid(raise_exception=True)
            new_event.save()

            contract.is_signed = True
            contract.save()            

            return Response(new_event.data, status=200)
        else:
            return Response(f"Contract {pk} already marked as signed.", status=400)


class EventViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.EventListSerializer
    detail_serializer_class = serializers.EventDetailSerializer
    permission_classes = [IsAdmin|IsSupportContact, ]
    filterset_class = EventFilter

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            queryset = Event.objects.filter(support_contact=user)
        else:
            queryset = Event.objects.all()        

        return queryset
