from django.contrib import admin
from django.urls import path, include

from docs.views import Docs

app_name = 'docs'

urlpatterns = [
    path('documention/', Docs.as_view(), name='documention'),
]