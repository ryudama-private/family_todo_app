from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("register/<int:family_id>/", views.delete_family_for_e2e),
    path("todos/", views.create_task, name="create_task"),
    path("todos/<int:task_id>/title/", views.update_task_title, name="update_task_title"),
    path("todos/<int:task_id>/assignee_id/", views.update_task_assignee, name="update_task_assignee"),
    path("todos/<int:task_id>/due_date/", views.update_task_due_date, name="update_task_due_date"),
    path("todos/<int:task_id>/alarm_minutes/", views.update_task_alarm_minutes, name="update_task_alarm_minutes"),
    path("todos/<int:task_id>/status/", views.update_task_status, name="update_task_status"),
]
