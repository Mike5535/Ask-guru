from django.shortcuts import render
# Create your views here.

QUESTIONS = [
    {
        "title": f"Title №{i}",
        "text": f"Text for questions №{i}",
        "number": i,
    } for i in range(10)
]

TAGS = [
    {
        "name": f"Tag №{i}",
        "ref": f"questions.tag{i}",
    } for i in range(10)
]

BEST_MEMBERS = [
    {
        "name": f"Member №{i}",
        "ref": f"members.member{i}",
    } for i in range(10)
]

def index(request):
    return render(request, "index.html", {"questions": QUESTIONS,"tags": TAGS,"best_members": BEST_MEMBERS})

def ask(request):
    return render(request, "ask.html", {"tags": TAGS,"best_members": BEST_MEMBERS})    

def question(request, i: int):
    return render(request, "page_question.html", {"question": QUESTIONS[i],"tags": TAGS,"best_members": BEST_MEMBERS})    
