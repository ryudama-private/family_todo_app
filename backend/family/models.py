from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    secret_question = models.CharField(max_length=255)
    secret_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "family"

    def __str__(self) -> str:
        return self.name


# Taskモデル
class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="やること")
    creator = models.ForeignKey('Family', related_name='created_tasks', on_delete=models.CASCADE, verbose_name="作った人")
    assignee = models.ForeignKey('Family', related_name='assigned_tasks', on_delete=models.CASCADE, verbose_name="やる人")
    due_date = models.DateTimeField(verbose_name="期限")
    status = models.CharField(max_length=50, verbose_name="進行状況")
    alarm_minutes = models.IntegerField(verbose_name="アラーム", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table = "task"

    def __str__(self):
        return self.title