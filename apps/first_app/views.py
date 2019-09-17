from django.shortcuts import render, redirect   
from django.contrib.messages import error
from .models import data, book
import bcrypt

def index(request):
    if request.session:
        del request.session

    return render(request, 'first_app/login.html')

def register(request):
    if request.method == "POST":
        errors = data.objects.validate_registration(request.POST)
        if errors:
            for err in errors:
                error(request, err)
            print(errors)
            return redirect('/')
        else:
            new_id = data.objects.register_user(request.POST)

          
            return redirect('/success')
    
def login(request):
     if request.method == "POST":
        users = data.objects.filter(email=request.POST["email"])

        user = users[0]

        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id']= user.id
            request.session['first_name']= user.first_name
            print(success)
            return redirect("/success")

        else:
        
            error(request, 'blah blah')
            return redirect("/")


def success(request):
    context={
        'user': data.objects.get(id=request.session["id"]),
        'all_books' : book.objects.all(),
    }
    return render (request, "first_app/base.html", context)



def add(request):
    if request.method == 'POST':
        title=request.POST["title"]
        description=request.POST["description"]
        book.objects.create(title=title,description=description)
        x = book.objects.last().id
    return redirect("/success")


def edit (request, show_id):
    context = {
        'user': data.objects.get(id=request.session["id"]),
        "show" : book.objects.get(id=show_id),
        "chosen_book" : book.objects.get(id=show_id),

    } 
    return render (request, "first_app/edit.html", context)



def delete(request, show_id):
    x = book.objects.get(id=show_id)
    x.delete()

    return redirect('/')