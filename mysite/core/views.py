from distutils.command import register
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import Http404
from django.shortcuts import render, redirect
from fusioncharts import FusionCharts
from django.db.models import Sum

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

            category = Category(user=user, name='dochody')
            category.save()

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
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid:
            category = form.save(commit=False)
            category.user_id = request.user.id
            category.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, "category.html", {'form': form, 'categories': categories})

@login_required
def filterByCategoryName(request, category_name):
    try:
        finances = Finance.objects.filter(user=request.user, category__name=category_name)
        summary = 0.0
        for finance in finances:
            summary += finance.value

    except Category.DoesNotExist:
        raise Http404('Category does not exist')

    return render(request, 'filter_category.html', {'finances': finances, 'summary': summary})


@login_required
def chart(request):
    dataSource = {}
    dataSource['chart'] = {
        "caption": "Total value in category",
        "subCaption": request.user.username,
        "xAxisName": "Categories",
        "yAxisName": "Value (In PLN)",
        "numberPrefix": "PLN",
        "paletteColors": "#0075c2",
        "bgColor": "#ffffff",
        "borderAlpha": "0",
        "canvasBorderAlpha": "0",
        "usePlotGradientColor": "0",
        "plotBorderAlpha": "10",
        "placevaluesInside": "1",
        "rotatevalues": "1",
        "valueFontColor": "#ffffff",
        "showXAxisLine": "1",
        "xAxisLineColor": "#999999",
        "divlineColor": "#999999",
        "divLineIsDashed": "1",
        "showAlternateHGridColor": "0",
        "subcaptionFontBold": "0",
        "subcaptionFontSize": "14"
    }

    dataSource['data'] = []

    #TODO?
    total_value_in_category = Finance.objects\
        .values('category__name').annotate(category_value=Sum('value')).filter(user=request.user).order_by('-category_value')

    for key in total_value_in_category:
        data = {}
        data['label'] = key.get('category__name')
        data['value'] = key.get('category_value')
        dataSource['data'].append(data)

    column2D = FusionCharts("column2D", "ex1", "600", "350", "chart-1", "json", dataSource)
    return render(request, 'chart.html', {'output': column2D.render()})