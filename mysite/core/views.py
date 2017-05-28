from distutils.command import register
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect



from mysite.core.form import *


@login_required
def home(request):
    incomes = Finance.objects.filter(user=request.user, category__name="dochody")
    outcomes = Finance.objects.filter(user=request.user).exclude(category__name="dochody")

    incomesValue = 0.0
    outcomesValue = 0.0


    for income in incomes:
        incomesValue += income.value

    for outcome in outcomes:
        outcomesValue -= outcome.value



    return render(request, 'myhome.html', {'incomes': incomes, 'outcomes': outcomes,
                                           'outcomesValue': outcomesValue, 'incomesValue': incomesValue})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def add(request):
    if request.method == 'POST':
        form = FinanceForm(request.user, request.POST)
        if form.is_valid():
            finance = form.save(commit=False)
            finance.user = request.user
            finance.save()
            return redirect('home')
    else:
        form = FinanceForm(request.user)
    return render(request, 'outcome.html', {'form': form})


@login_required
def addCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid:
            category = form.save(commit=False)
            category.user_id = request.user.id
            category.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, "category.html", {'form': form})