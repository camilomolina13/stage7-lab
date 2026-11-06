from django.urls import path

from .views import ProjectDetail, ProjectList, TaskDetail, TaskList

urlpatterns = [
    path("projects", ProjectList.as_view()),
    path("projects/<int:pk>", ProjectDetail.as_view()),
    path("tasks", TaskList.as_view()),
    path("tasks/<int:pk>", TaskDetail.as_view()),
]