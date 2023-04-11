import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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

@login_required
def quiz(request):
    flashcards = FlashCard.objects.all().order_by('?')[:5]
    form = FlashCardForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Handle the user's answers
            answers = form.cleaned_data['back']
            correct_answers = 0
            for i, flashcard in enumerate(flashcards):
                if i < len(answers):
                    # Compare the user's answer to the correct answer for this flashcard
                    if answers[i].lower() == flashcard.back.lower():
                        correct_answers += 1

            # Add the number of correct answers to the context
            context = {
                'flashcards': flashcards,
                'form': form,
                'correct_answers': correct_answers
            }

            # Redirect to a page showing the results
            return render(request, 'flashcards/quiz_res.html', context)

    context = {
        'flashcards': flashcards,
        'form': form,
    }
    return render(request, 'flashcards/quiz.html', context)


def results(request):
    return render(request, 'flashcards/quiz_res.html')
