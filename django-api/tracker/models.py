from django.db import models
from django.db.models.functions import Now


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    # db_default: Django no envía este valor, lo pone PostgreSQL (DEFAULT NOW())
    created_at = models.DateTimeField(db_default=Now(), editable=False)

    class Meta:
        db_table = "projects"
        managed = False      # Django NUNCA crea ni modifica esta tabla


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    # Entero normal (sin ForeignKey): la FK y el ON DELETE CASCADE los maneja PostgreSQL
    project_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20)
    priority = models.CharField(max_length=10)
    due_date = models.DateField(null=True)
    created_at = models.DateTimeField(db_default=Now(), editable=False)
    # El trigger de PostgreSQL actualiza este campo en cada UPDATE
    updated_at = models.DateTimeField(db_default=Now(), editable=False)

    class Meta:
        db_table = "tasks"
        managed = False