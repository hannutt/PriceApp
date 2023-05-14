from django.db import models

# Create your models here.
#luokkamäärityksellä luodaan tietokannan taulut
class Todo(models.Model):
     task = models.CharField(max_length=200)
     timelimit = models.CharField(max_length=25)

class Quiz(models.Model):
     question = models.CharField(max_length=200,null=True)
     op1 = models.CharField(max_length=200,null=True)
     op2 = models.CharField(max_length=200,null=True)
     answer = models.CharField(max_length=200,null=True)

     def __str__(self):
          return self.question