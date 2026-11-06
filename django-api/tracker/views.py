from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import MAX_INT, get_json_body, get_or_404, save_changes
from .models import Project, Task
from .presenters import project_to_dict, task_to_dict
from .serializers import ProjectSerializer, TaskSerializer

PROJECT_NOT_FOUND = "Project not found."
TASK_NOT_FOUND = "Task not found."


def validated(serializer_class, request):
    """Lee el body y lo valida. Lanza ValidationError (400) si hay problemas."""
    serializer = serializer_class(data=get_json_body(request))
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


# ------------------------------ Projects ------------------------------

class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.order_by("id")
        return Response([project_to_dict(p) for p in projects], status=200)

    def post(self, request):
        data = validated(ProjectSerializer, request)
        project = Project.objects.create(**data)
        project.refresh_from_db()          # asegura created_at puesto por PostgreSQL
        return Response(project_to_dict(project), status=201)


class ProjectDetail(APIView):
    def get(self, request, pk):
        project = get_or_404(Project, pk, PROJECT_NOT_FOUND)
        return Response(project_to_dict(project), status=200)

    def put(self, request, pk):
        project = get_or_404(Project, pk, PROJECT_NOT_FOUND)   # 404 primero, luego el body
        data = validated(ProjectSerializer, request)
        save_changes(project, data)
        return Response(project_to_dict(project), status=200)

    def delete(self, request, pk):
        project = get_or_404(Project, pk, PROJECT_NOT_FOUND)
        project.delete()                   # las tareas se borran por el ON DELETE CASCADE
        return Response(status=204)


# -------------------------------- Tasks --------------------------------

class TaskList(APIView):
    def get(self, request):
        tasks = Task.objects.order_by("id")

        raw_project_id = request.query_params.get("project_id")
        if raw_project_id is not None:
            try:
                project_id = int(raw_project_id)
            except ValueError:
                raise ValidationError({"project_id": ["Not a valid integer."]})
            if project_id < 1 or project_id > MAX_INT:
                return Response([], status=200)      # no puede existir ese proyecto
            tasks = tasks.filter(project_id=project_id)

        return Response([task_to_dict(t) for t in tasks], status=200)

    def post(self, request):
        data = validated(TaskSerializer, request)
        task = Task.objects.create(**data)
        task.refresh_from_db()
        return Response(task_to_dict(task), status=201)


class TaskDetail(APIView):
    def get(self, request, pk):
        task = get_or_404(Task, pk, TASK_NOT_FOUND)
        return Response(task_to_dict(task), status=200)

    def put(self, request, pk):
        task = get_or_404(Task, pk, TASK_NOT_FOUND)
        data = validated(TaskSerializer, request)
        save_changes(task, data)
        return Response(task_to_dict(task), status=200)

    def delete(self, request, pk):
        task = get_or_404(Task, pk, TASK_NOT_FOUND)
        task.delete()
        return Response(status=204)