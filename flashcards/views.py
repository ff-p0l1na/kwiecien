import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import FlashCard
from .forms import FlashCardAdder


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
    flashcards = FlashCard.objects.filter(author=request.user).order_by('?')[:5]
    return render(request, 'flashcards/quiz.html', {'flashcards': flashcards})


@login_required
def quiz_submit(request):
    flashcard_backs = request.POST.getlist('flashcard_backs[]')
    user_answers = request.POST.getlist('answers[]')
    flashcards = FlashCard.objects.filter(id__in=flashcard_backs)
    correct_answers = 0
    for flashcard, user_answer in zip(flashcards, user_answers):
        if str(user_answer.strip().lower()) == str(flashcard.back.strip().lower()):
            correct_answers += 1
        else:
            flashcard.correct_answer = str(flashcard.back)
        flashcard.user_answer = str(user_answer)
        flashcard.save()

    return redirect('quiz_results', correct_answers=correct_answers)


@login_required
def quiz_results(request, correct_answers):
    num_questions = 5
    score = correct_answers / num_questions * 100
    message = 'Odpowiedziano poprawnie na {} z {} pytań.'.format(correct_answers, num_questions)
    if score < 60:
        message = 'Odpowiedziano poprawnie na {} z {} pytań. Zalecam powtórkę słówek.'.format(correct_answers, num_questions)
    elif score < 80:
        message = 'Odpowiedziano poprawnie na {} z {} pytań. Nadal może być lepiej.'.format(correct_answers, num_questions)
    else:
        message = 'Odpowiedziano poprawnie na {} z {} pytań. Wszystko już umiesz.'.format(correct_answers, num_questions)
    return render(request, 'flashcards/quiz.html', {'message': message})
