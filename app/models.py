from django.db import models
from django.contrib.auth.models import User

class TagManager(models.Manager):
        def questions_tag(self,):
                return self.filter(tags)

class Tag(models.Model):
        name = models.CharField(max_length=255)

        def __str__(self):
                return self.name

class Question(models.Model):
        name = models.CharField(max_length=255)
        text = models.TextField()
        author = models.ForeignKey(User, on_delete=models.PROTECT)
        tags = models.ManyToManyField(Tag)

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

class LikeButton(models.Model):
    content=models.TextField(null=True)
    likes=models.ManyToManyField(User,blank=True, related_name='likes')
     
    @property
    def total_likes(self):
        return self.likes.count() 
