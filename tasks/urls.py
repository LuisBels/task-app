from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home" ),
    path("signup/", views.signup, name="signup"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks_completed/", views.tasks_completed, name="tasks_completed"),
    path("logout/", views.sigout, name="sigout"),
    path("signin/", views.signin, name="signin"),
    path("tasks/create/", views.created_task, name="created_task"),
    path("tasks/<int:task_id>/", views.task_detail, name="detail"),
    path("tasks/<int:task_id>/complete", views.complete_task, name="complete"),
    path("tasks/<int:task_id>/edit/", views.edit_task, name="edit"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="delete")
]