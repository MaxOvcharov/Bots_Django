# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.models import User, Group

from models import Test
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer, TestSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tests to be viewed or edited.
    """
    queryset = Test.objects.all()
    serializer_class = TestSerializer
