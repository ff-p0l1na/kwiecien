import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import FlashCard
from .forms import FlashCardAdder


def add_flashcard(request):
    submitted = False
    if request.method == "POST":
        form = FlashCardAdder(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dodaj_fiszke?submitted=True')
    else:
        form = FlashCardAdder
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'flashcards/add_flashcard.html', {'form': form, 'submitted': submitted,})

def all_flashcards(request):
    fc_list = FlashCard.objects.all()
    return render(request, 'flashcards/fc_list.html',
                  {'fc_list': fc_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Paulina"
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
