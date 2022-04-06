from django.shortcuts import render
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

def user(request):
    return render(request, "user.html", {"tags": TAGS,"best_members": BEST_MEMBERS})

def login(request):
    return render(request, "login.html", {"tags": TAGS,"best_members": BEST_MEMBERS})  

def register(request):
    return render(request, "register.html", {"tags": TAGS,"best_members": BEST_MEMBERS})  

def question(request, i: int):
    return render(request, "page_question.html", {"question": QUESTIONS[i],"tags": TAGS,"best_members": BEST_MEMBERS})    
