from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from django.contrib.auth.models import User
from django.db import connection




def index(request):
    if not request.user.id:
        return redirect("/login")
    else:
        return render(request,"pages/index.html")

#@login_required
def notes(request,username):
    user = User.objects.get(username=username)
    #if  user.username != request.user.username:
    # print("Unauthorised access attempt")
    #   raise PermissionDenied

    notes = Note.objects.raw(f"SELECT * FROM app_note WHERE creator_id = {user.id}")
    #notes = Note.objects.filter(creator=request.user)


    context = {"notes":  notes if notes else [],"user":user}
    return render(request,"pages/notes.html",context)


#@login_required
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
    if request.method == 'GET':
        note_id = request.GET['note_id']
        #note = Note.objects.get(id=note_id)
        #note.delete()
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM app_note WHERE id = {note_id}")
        return redirect("/")



