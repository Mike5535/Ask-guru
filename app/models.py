import datetime
from django.db import models
from django.contrib.auth.models import User

class ProfileQuery(models.QuerySet):
    def user(self, user):
        return self.filter(username=user.username)

    def get_usernames(self):
        return User.objects.values('username')

class QuestionQuery(models.QuerySet):
    def latest(self):
        return self.order_by("-publish_date")

    def popular(self):
        return self.order_by("-reputation")

class TagQuery(models.QuerySet):
    def popular(self):
        return self.annotate(num_questions=models.Count("questions")).order_by("-num_questions")

    def questions(self, question):
        return self.filter(questions=question)

    def get_by_title(self, title):
        tags = self.filter(title=title)
        if len(tags) > 0:
            return tags[0]
        else:
            return None



class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuery(self.model, using=self.db)

    def get_user(self, user):
        return self.get_queryset().user(user)
    
    def get_usernames(self):
        return self.get_queryset().get_usernames()
  
class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuery(self.model)

    def get_popular(self):
        return self.get_queryset().popular()

    def get_latest(self):
        return self.get_queryset().latest()

    def get_by_tag(self, tag=None):
        if tag is None:
            return self.get_queryset().latest()
        return self.get_queryset().filter(tag=tag)

class AnswerManager(models.Manager):
    def get_queryset(self, question_search=None):
        if question_search is None:
            return QuestionQuery(self.model, using=self.db)
        return QuestionQuery(self.model, using=self.db).filter(question__id=question_search.id)

    def get_popular(self, question_search=None):
        return self.get_queryset(question_search).popular()

    def get_latest(self, question_search=None):
        return self.get_queryset(question_search).latest()

class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuery(self.model, using=self.db)

    def get_popular(self):
        return self.get_queryset().popular()

    def get_questions(self, question):
        return self.get_queryset().questions(question)

    def get_tag_by_title(self, title):
        return self.get_queryset().get_by_title(title)





class Profile(User):
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True,
                                      default="profile_images/user_01.jpg")

    def __str__(self):
        return str(self.username)

    manager = ProfileManager()


class Like(models.Model):
    authors = models.ManyToManyField(Profile, blank=True)

    def __int__(self):
        return self.authors.all().count()


class Dislike(models.Model):
    authors = models.ManyToManyField(Profile, blank=True)

    def __int__(self):
        return self.authors.all().count()


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=8192)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    dislike = models.ForeignKey(Dislike, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publish_date = models.DateField(default=datetime.date.today)
    reputation = models.IntegerField()

    manager = QuestionManager()

    def get_tags(self):
        return Tag.manager.get_questions(self)

    def get_count_answers(self):
        return Answer.manager.get_queryset(self).count()

    def get_reputation(self):
        return self.manager.get_reputation()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=8192)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    dislike = models.ForeignKey(Dislike, on_delete=models.CASCADE)
    isCorrect = models.BooleanField(default=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publish_date = models.DateField(default=datetime.date.today)
    reputation = models.IntegerField()

    manager = AnswerManager()

    def get_reputation(self):
        return self.manager.get_reputation()

    def __str__(self):
        return str(self.author) + "/" + str(self.question.title)


class Tag(models.Model):
    title = models.CharField(max_length=32)
    questions = models.ManyToManyField(Question, blank=True)
    last_update = models.DateField(auto_now=True)

    manager = TagManager()

    def get_count_questions(self):
        return Question.manager.get_by_tag(self).count()

    def __str__(self):
        return self.title
