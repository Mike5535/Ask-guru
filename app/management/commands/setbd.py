from io import open

from django.core.management.base import BaseCommand
from app.models import Profile, Like, Dislike, Question, Answer, Tag
from django.core.files.base import ContentFile
from django.core.files import File

USERS_COUNT = 5 
QUESTION_COUNT = 100  
ANSWERS_COUNT = 1000 
TAGS_COUNT = 10  
REPUTATION_COUNT = 2000 


def clearDB():
    Tag.manager.all().delete()
    Answer.manager.all().delete()
    Like.objects.all().delete()
    Dislike.objects.all().delete()
    Question.manager.all().delete()
    Profile.objects.all().exclude(username="admin").delete()


def addUsers():
    for i in range(USERS_COUNT):
        username = "User_" + str(i)
        password = "password" + str(i)
        email = "email" + str(i) + "@mail.ru"
        image_path = "profile_images/duck.png"
        profile = Profile(username=username, password=password, email=email)
        profile.set_password(password)

        profile.profile_image = image_path
        profile.save()


def addTags():
    for i in range(TAGS_COUNT):
        title = "Tag_" + str(i)
        tag = Tag(title=title)
        tag.save()
        for j in range(QUESTION_COUNT // 10):
            question = Question.manager.all()[(i * j) % QUESTION_COUNT]
            tag.questions.add(question)


def addAnswers():
    objects = []
    for i in range(ANSWERS_COUNT):
        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et ' \
               'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ' \
               'ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu ' \
               'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt ' \
               'mollit anim id est laborum. ' + str(i)
        question = Question.manager.all()[i % QUESTION_COUNT]
        like = Like.objects.all()[i % REPUTATION_COUNT]
        dislike = Dislike.objects.all()[i % REPUTATION_COUNT]
        author = Profile.objects.all()[i % USERS_COUNT]
        reputation = int(like) - int(dislike)
        objects.append(
            Answer(text=text, question=question, like=like, dislike=dislike, reputation=reputation, author=author))
    Answer.manager.bulk_create(objects)


def addQuestions():
    objects = []
    for i in range(QUESTION_COUNT):
        title = "Question Title#" + str(i)
        text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the " \
               "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and " \
               "scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap " \
               "into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the " \
               "release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing " \
               "software like Aldus PageMaker including versions of Lorem Ipsum. Why do we use it?It is a long " \
               "established fact that a reader will be distracted by the readable content of a page when looking at its " \
               "layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, " \
               "as opposed to using 'Content here, content here', making it look like readable English. Many desktop " \
               "publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search " \
               "for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over " \
               "the years, sometimes by accident, sometimes on purpose (injected humour and the like). #" + str(i)
        like = Like.objects.all()[i % REPUTATION_COUNT]
        dislike = Dislike.objects.all()[i % REPUTATION_COUNT]
        author = Profile.objects.all()[i % USERS_COUNT]
        reputation = int(like) - int(dislike)
        objects.append(
            Question(title=title, text=text, like=like, dislike=dislike, reputation=reputation, author=author))
    Question.manager.bulk_create(objects)


def addReputations():
    for i in range(REPUTATION_COUNT):
        like = Like()
        dislike = Dislike()
        like.save()
        dislike.save()
        for j in range(1, i % USERS_COUNT):
            author = Profile.objects.all()[j]
            like.authors.add(author)
        author = Profile.objects.all()[0]
        dislike.authors.add(author)


def addAllTables():
    addUsers()
    addReputations()
    addQuestions()
    addAnswers()
    addTags()


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        clearDB()
        addAllTables()
