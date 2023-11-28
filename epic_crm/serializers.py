from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework.serializers import ModelSerializer, ValidationError, CharField, ChoiceField
from .models import Client, Contract, Event, User


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'groups']
        extra_kwargs = {'password': {'write_only': True}}


class UserDetailSerializer(ModelSerializer):

    # TODO find a way to input group names instead of ids

    class Meta:
        model = User
        fields = ['id', 'username', "password", "first_name", "last_name", "email", "is_superuser", "is_active", "date_joined", "last_login", "groups"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        """Hashes password."""
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters')
        return make_password(value)


class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'full_name', 'email', 'sales_contact']


class ClientDetailSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


    # TODO élaborer pour qu'on voit les détails du sales_contact


class ContractListSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = ["id", "client", "sales_contact", "is_signed"]


class ContractDetailSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['is_signed']

    def validate(self, data):

        if data.get('client'):
            client = data['client']
            user = data['sales_contact']
            if client.sales_contact not in [user, None]:
                raise ValidationError("Cannot create a contract for a client linked to another salesperson.")            

        return data


class EventListSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'event_status', 'client', 'support_contact']


class EventDetailSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        # read_only_fields = ['client', 'support_contact']

    # TODO make sure event date is in the future ?
