from django.urls import path

from . import views

urlpatterns = [
    path('', views.document_extraction, name='document_extraction'),
]
