from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Note
from django.contrib.auth.models import User
from django.db import connection
from django.core.exceptions import PermissionDenied
from django.http import Http404






def index(request):
    if not request.user.id:
        return redirect("/login")
    else:
        return render(request,"pages/index.html")

#Flaw 1 - Broken access control
#@login_required
def notes(request,username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist") 
    print(f"user {user.id}")
    print(f" request {request.user.id}")
#Flaw 1 - Broken access control
    #if  user.id != request.user.id:

    #Flaw 3 - Logging
        #print(f"Unauthorised access attempt - {request.user.username} tried to access {user.username}s notes")

        #raise PermissionDenied


    notes = Note.objects.filter(creator=request.user)


    context = {"notes":  notes if notes else [],"user":user}
    return render(request,"pages/notes.html",context)


@login_required
def create_note(request):    
    if request.method == 'POST':
        content = request.POST['content']
        try:
            new_note = Note(creator=request.user,content=content)
            new_note.save()
        except Exception as e:
            print("could not create note",e)
        return redirect("/")


def delete_note(request):
    #Flaw 5 - CSRF
    
    #--- replace faulty if statement below with this ---
    #if request.method == 'POST':
    #    note_id = request.POST['note_id']

    if request.method == 'GET':
        note_id = request.GET['note_id']

#Flaw 4 - Injection
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM app_note WHERE id = {note_id}")
        # Code below uses DJangos built in ORM
        #note = Note.objects.get(id=note_id)
        #note.delete()
        return redirect("/")



