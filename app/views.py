from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from app import models
from django.shortcuts import get_object_or_404 
import json
from django.http import HttpResponse
# Create your views here.

QUESTIONS = [
    {
        "title": f"Title №{i}",
        "text": f"Text for questions №{i} orem ipsum dolor sit amet, consectetur adipiscing elit. Morbi euismod tincidunt velit, et facilisis eros fringilla eget. Maecenas et ornare augue. Nunc tempor leo quis augue volutpat ultricies. Vivamus ornare auctor neque vel rhoncus. Aenean risus tellus, viverra a semper at, tristique id quam. Donec et efficitur felis, vitae faucibus arcu. Vivamus ultricies, mauris vitae tincidunt pellentesque, quam ante placerat urna, nec tincidunt lacus erat vitae sapien. Proin ac rhoncus metus, eu maximus est. Nullam vel volutpat turpis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Mauris eu metus blandit, fringilla lacus vel, sodales justo. Etiam sollicitudin consequat diam in iaculis. Sed sed dolor odio. In feugiat lorem nibh, nec ultricies lorem bibendum in.",
        "number": i,
    } for i in range(10)
]

TAGS = [
    {
        "name": f"Tag №{i}",
    } for i in range(10)
]

BEST_MEMBERS = [
    {
        "name": f"Member №{i}",
        "ref": f"members.member{i}",
    } for i in range(10)
]

def paginate(objects_list, request, per_page=10):
    page = request.GET.get('page')
    paginator = Paginator(objects_list, per_page)
    try:  
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        # Если страница не является целым числом, поставим первую страницу  
        posts = paginator.page(1)  
    except EmptyPage:  
        # Если страница больше максимальной, доставить последнюю страницу результатов  
        posts = paginator.page(paginator.num_pages)  
    return   {'page': page, 'posts': posts}   
      
def index(request):
    paginate(QUESTIONS,request,20)
    return render(request, "index.html", paginate(models.Question.objects.all(),request,1) | {"tags": TAGS,"best_members": BEST_MEMBERS})

def ask(request):
    return render(request, "ask.html", {"tags": TAGS,"best_members": BEST_MEMBERS})    

def user(request):
    return render(request, "user.html", {"tags": TAGS,"best_members": BEST_MEMBERS})

def login(request):
    return render(request, "login.html", {"tags": TAGS,"best_members": BEST_MEMBERS})  

def register(request):
    return render(request, "register.html", {"tags": TAGS,"best_members": BEST_MEMBERS})

def tag_question(request, string: str):
    return render(request, "tag_questions.html", {"questions": QUESTIONS,"tag": string,"tags": TAGS,"best_members": BEST_MEMBERS})    

def question(request, i: int):
    return render(request, "page_question.html", paginate(models.Answer.objects.filter(question_id=i),request,3) | {"question": models.Question.objects.all()[i-1],"tags": TAGS,"best_members": BEST_MEMBERS})    

def like_button(request, i: int):
   if request.method =="POST":
       if request.POST.get("operation") == "like_submit" and request.is_ajax():
         content_id=request.POST.get("content_id",None)
         content=get_object_or_404(LikeButton,pk=content_id)
         if content.likes.filter(id=request.user.id): #already liked the content
            content.likes.remove(request.user) #remove user from likes 
            liked=False
         else:
             content.likes.add(request.user) 
             liked=True
         ctx={"likes_count":content.total_likes,"liked":liked,"content_id":content_id}
         return HttpResponse(json.dumps(ctx), content_type='application/json')

   contents=LikeButton.objects.all()
   already_liked=[]
   id=request.user.id
   for content in contents:
       if(content.likes.filter(id=id).exists()):
        already_liked.append(content.id)
   ctx={"contents":contents,"already_liked":already_liked}
   return render(request,"like.html",ctx)
