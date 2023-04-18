import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
import random
from .models import FlashCard
from .forms import FlashCardAdder, FlashCardForm


def add_flashcard(request):
    submitted = False
    if request.method == "POST":
        form = FlashCardAdder(request.POST)
        if form.is_valid():
            FlashCard = form.save(commit=False)
            FlashCard.author = request.user
            form.save()
            return HttpResponseRedirect('/dodaj_fiszke?submitted=True')
    else:
        form = FlashCardAdder
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'flashcards/add_flashcard.html', {'form': form, 'submitted': submitted,})


@login_required
def all_flashcards(request):
    fc_list = FlashCard.objects.filter(author=request.user)
    return render(request, 'flashcards/fc_list.html',
                  {'fc_list': fc_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    if request.user.is_authenticated:
        name = request.user.username
    else:
        name = "Nieznajomy"
    month = month.title()
    # miesiac na cyfre
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # kalendarz
    cal = HTMLCalendar().formatmonth(year, month_number)

    # obecny rok
    now = datetime.now()
    current_year = now.year

    # godzina
    time = now.strftime('%H:%M')

    return render(request,
                  'flashcards/home.html', {'name': name,
                                'year': year,
                                'month': month,
                                'month_number': month_number,
                                'cal': cal,
                                'current_year': current_year,
                                'time': time,
                                })


# @login_required()
# def quiz(request):
#     flashcard = random.choice(FlashCard.objects.all())
#     if request.method == 'POST':
#         form = FlashCardForm(request.POST)
#         if form.is_valid():
#             user_answer = form.cleaned_data['back']
#             if user_answer.lower() == flashcard.back.lower():
#                 message = f"Dobrze! Odpowiedź to: {user_answer}."
#             else:
#                 message = f"Źle, poprawna odpowiedź to: {flashcard.back}."
#         else:
#             message = "Proszę wprowadzić odpowiedź."
#         context = {
#             'flashcard': flashcard,
#             'message': message,
#             'form': form,
#         }
#     else:
#         form = FlashCardForm()
#         context = {
#             'flashcard': flashcard,
#             'form': form,
#         }
#     return render(request, 'flashcards/quiz.html', context)

@login_required()
def quiz(request):
    # Zapisanie poprzedniego id
    prev_flashcard_id = request.session.get('prev_flashcard_id')
    prev_user_answer = request.session.get('prev_user_answer')

    # Losowanie nowej karty bez duplikatu
    flashcard = random.choice(FlashCard.objects.exclude(id=prev_flashcard_id))

    if request.method == 'POST':
        form = FlashCardForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['back']
            if user_answer.lower() == flashcard.back.lower():
                message = f"Dobrze! Odpowiedź to: {user_answer}."
            else:
                message = f"Źle, poprawna odpowiedź to: {flashcard.back}."
            # Zapisanie odpowiedzi w sesji
            request.session['prev_flashcard_id'] = flashcard.id
            request.session['prev_user_answer'] = user_answer
        else:
            message = "Proszę wprowadzić odpowiedź."
        context = {
            'flashcard': flashcard,
            'message': message,
            'form': form,
            'prev_user_answer': prev_user_answer,
        }
    else:
        form = FlashCardForm()
        context = {
            'flashcard': flashcard,
            'form': form,
            'prev_user_answer': prev_user_answer,
        }
    return render(request, 'flashcards/quiz.html', context)

