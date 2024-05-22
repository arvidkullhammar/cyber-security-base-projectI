from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("notes/<str:username>/", views.notes, name="notes"),
    path("create/", views.create_note),
    path("delete/", views.delete_note,name="delete"),
    path('login/', LoginView.as_view(template_name='pages/login.html')),
	path('logout/', LogoutView.as_view(next_page='/login')),
]