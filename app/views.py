from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from app.models import Profile, Like, Dislike, Question, Answer, Tag
from django.http import Http404
from .forms import LoginForm, RegistrationForm, AnswerForm, QuestionForm, SettingsForm



def get_last_posts(request, array):
    page_number = request.GET.get('page')
    paginator = Paginator(array, 5)
    posts = paginator.page(paginator.num_pages)
    return posts, page_number

def get_profile(user):
    profile = Profile.manager.get_user(user)
    if len(profile) < 1:
        return user
    return profile[0]


def save_question(user, title, text, tags):
    dislike = Dislike()
    dislike.save()
    like = Like()
    like.save()
    reputation = 0
    question = Question(title=title, text=text, like=like, dislike=dislike, author=user, reputation=reputation)
    question.save()

    tags = tags.split(' ')
    for title in tags:
        tag = Tag.manager.get_tag_by_title(title)
        if tag is not None:
            tag.questions.add(question)
            continue
        tag = Tag(title=title)
        tag.save()
        tag.questions.add(question)

    return question
    
def get_popular_tags(number=10):
    tags = Tag.manager.get_popular()
    if len(tags) <= number:
        return tags
    return tags[:number]

def save_answer(text, user, question):
    like = Like()
    like.save()
    dislike = Dislike()
    dislike.save()
    reputation = 0
    answer = Answer(text=text, question=question, like=like, dislike=dislike, author=user,
                    reputation=reputation)
    answer.save()

def get_posts(request, array):
    page_number = request.GET.get('page')
    paginator = Paginator(array, 5)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts, page_number

def update_settings(user, username, email, password, first_name, last_name, profile_image):
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if profile_image:
        user.profile_image = profile_image
    user.save()





def index(request, tag: str = '', sort: str = ''):
    header = "popular questions"
    popular_tags = get_popular_tags()
    questions = Question.manager.get_popular()
    user = request.user
    if sort == "latest":
        header = "latest questions"
        questions = Question.manager.get_latest()
    if tag != '':
        tag = Tag.manager.get_tag_by_title(tag)
        questions = Question.manager.get_by_tag(tag)
        if len(questions) <= 0:
            raise Http404("Tag does not exist")
    posts, page_number = get_posts(request, questions)
    users = list(Profile.manager.get_usernames())

    user = get_profile(user)
    return render(request, "index.html",
                  {"questions": questions, "tag": tag, "page": page_number,
                   "posts": posts, "tags": popular_tags, "header": header, "user": user, "best_members":users})


@login_required
def ask(request):
    popular_tags = get_popular_tags()
    user = request.user
    user = get_profile(user)
    if request.method == "POST":
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = save_question(user, form.clean_title(), form.clean_text(), form.clean_tags())
            redirect_url = '/questionAnswer/' + str(question.id)
            return redirect(redirect_url)
    else:
        form = QuestionForm()
    return render(request, "ask.html", {"user": user, "tags": popular_tags, "form": form})


def logout(request):
    auth.logout(request)
    return redirect('/')


def login(request):
    popular_tags = get_popular_tags()
    user = request.user

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect('/')
            else:
                form.add_error("password", "Invalid username or password")
    else:
        form = LoginForm()

    user = get_profile(user)
    return render(request, "login.html", {"tags": popular_tags, "form": form, "user": user})


def registration(request):
    popular_tags = get_popular_tags()

    if request.method == "POST":
        form = RegistrationForm(data=request.POST, files=request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            auth.authenticate(username=username, password=raw_password)
            return redirect('/login/')

    else:
        form = RegistrationForm()
    return render(request, "registration.html", {"tags": popular_tags, "form": form})


@login_required
def settings(request):
    popular_tags = get_popular_tags()
    user = request.user
    user = get_profile(user)

    if request.method == "POST":
        form = SettingsForm(initial=request.POST, files=request.FILES)
        if form.is_valid():
            update_settings(user, form.clean_username(), form.clean_email(), form.clean_password(),
                            form.clean_first_name(), form.clean_last_name(), form.clean_profile_image())
    else:
        initial_data = model_to_dict(user)
        initial_data["profile_image"] = user.profile_image
        form = SettingsForm(initial=initial_data)

    return render(request, "settings.html", {"user": user, "tags": popular_tags, "form": form})


def answer(request, id_question: int):
    popular_tags = get_popular_tags()
    user = request.user

    question = Question.manager.all().filter(id=id_question)
    if len(question) <= 0:
        raise Http404("Question does not exist")
    question = question[0]
    answers = Answer.manager.get_popular(question)
    posts, page_number = get_posts(request, answers)

    user = get_profile(user)

    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            save_answer(form.clean_text(), user, question)
            answers = Answer.manager.get_popular(question)
            posts, page_number = get_last_posts(request, answers)
    else:
        form = AnswerForm()

    users = list(Profile.manager.get_usernames())

    return render(request, "page_question.html",
                  {"question": question, "answers": answers, "page": page_number, "posts": posts,
                   "tags": popular_tags, "user": user,"best_members":users, "form": form})


@login_required
@require_POST
def vote(request):
    print(request.GET)
    question_id = request.POST['question_id']
    print(question_id)
    return JsonResponse({'result_code': 0})
