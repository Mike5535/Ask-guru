from django.shortcuts import render
# Create your views here.

QUESTIONS = [
    {
        "title": f"Title №{i}",
        "text": f"Text for questions №{i}",
    } for i in range(10)
]

def index(request):
    return render(request, "base.html", {"questions": QUESTIONS})

def ask(request):
    return render(request, "ask.html")    
