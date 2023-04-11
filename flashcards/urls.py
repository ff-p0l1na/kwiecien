from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('fiszki/', views.all_flashcards, name='list-flashcards'),
    path('dodaj_fiszke/', views.add_flashcard, name='add-flashcard'),
    path('quiz/', views.quiz, name='quiz'),
    path('wynik/', views.results, name='wynik')
]



