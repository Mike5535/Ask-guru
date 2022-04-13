from django.db import models
from django.contrib.auth.models import User
import itertools 



class TopQuestionsManager(models.Manager):
        def top_questions(self):
                quest = Question.objects.values()
                que = list(quest)
                likes = list()

                for i in range(len(que)):
                        likes.append([len(list(Like.objects.filter(question = que[i]['id']))),que[i]['id']])
                        
                likes.sort(reverse=True , key = lambda l:l[0])

                que_id_sort  = []

                for j in range(len(likes)):
                        que_id_sort.append(likes[j][1])

               

                otvet = Question.objects.filter(id__in = que_id_sort)

                return otvet

class Tag(models.Model):
        name = models.CharField(max_length=255)

        def __str__(self):
                return self.name

class Question(models.Model):
        name = models.CharField(max_length=255)
        text = models.TextField()
        author = models.ForeignKey(User, on_delete=models.PROTECT)
        tags = models.ManyToManyField(Tag)

        objects = TopQuestionsManager()

        def __str__(self):
                return self.name

class Answer(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        text = models.TextField()
        author = models.ForeignKey(User, on_delete=models.PROTECT)
        STATUSES=[
                ('r','Correct'),
                ('w','Wrong'),
        ]
        correct = models.CharField(max_length=1,choices=STATUSES,blank=True,null=True)  

        def __str__(self):
                return self.question.name

class Profile(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        avatar = models.ImageField(upload_to='images/')
        

        def __str__(self):
                return self.user.username

class Like(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        answer = models.ForeignKey(Answer, on_delete=models.CASCADE,blank=True,null=True)
        question = models.ForeignKey(Question, on_delete=models.CASCADE,blank=True,null=True)
        STATUS = [
                (1,'Like'),
                (0,'Unlike'),
                (-1,'Dislike'),
        ]
        status = models.SmallIntegerField(choices=STATUS,default=0)

        class Meta:
                unique_together = [['user','answer'],['user','question']]

        def __str__(self):
                return self.user.username
