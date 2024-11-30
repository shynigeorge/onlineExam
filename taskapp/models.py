from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Question Model
class Question(models.Model):
    question_text = models.CharField(max_length=255)
    answer_a = models.CharField(max_length=100, default='Always')
    answer_b = models.CharField(max_length=100, default='Often')
    answer_c = models.CharField(max_length=100, default='Sometimes')
    answer_d = models.CharField(max_length=100, default='Never')

    # Score values for each answer
    score_a = models.IntegerField(default=10)
    score_b = models.IntegerField(default=7)
    score_c = models.IntegerField(default=4)
    score_d = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text


# UserResponse Model
class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1)  # Options: 'a', 'b', 'c', 'd'
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text} - {self.answer}"
