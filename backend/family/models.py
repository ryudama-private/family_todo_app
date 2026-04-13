from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    secret_question = models.CharField(max_length=255)
    secret_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "family"

    def __str__(self) -> str:
        return self.name