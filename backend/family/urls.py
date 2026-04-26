from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("register/<int:family_id>/", views.delete_family_for_e2e),
    path("todos/", views.create_task),
]
