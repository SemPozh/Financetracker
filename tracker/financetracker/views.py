from django.contrib.auth import login, logout
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import *
from django.shortcuts import redirect
from django.http import JsonResponse
import datetime
from .models import Finance


def index(request):
    return render(request, 'financetracker/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистриции')
    else:
        form = UserRegisterForm()

    return render(request, 'financetracker/register.html', context={'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'financetracker/login.html', context={'form': form})


def review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                grade = form.cleaned_data['grade']
                user = request.user
                review = Review.objects.create(user_id=user.id, content=content, grade=grade)
                review.save()
                messages.success(request, 'Отзыв опубликован! Спасибо!')
                return redirect('reviews')
            else:
                messages.error(request, 'Ошибка отправки отзыва!')
        else:
            form = ReviewForm()
            reviews = Review.objects.all()[:5]
        return render(request, 'financetracker/reviews.html', context={'form': form, 'reviews': reviews})
    else:
        return redirect('register')


def ajax_reviews(request):
    if request.is_ajax():
        last_post_id = request.GET.get('lastPostId')
        more_reviews = Review.objects.filter(pk__gt=int(last_post_id))[:5]
        if not more_reviews:
            return JsonResponse({'data': False})
        data = []
        for review in more_reviews:
            obj = {
                'id': review.id,
                'date': review.date.strftime("%d %B %Yг. %H:%M"),
                'content': review.content,
                'user': review.user.username,
                'grade': review.grade
            }

            data.append(obj)
        data[-1]['last_post'] = True
        return JsonResponse({'data': data})


def my_finance(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form1 = AddFinanceForm(request.POST, prefix="form1")
            form2 = AddFinanceForm(request.POST, prefix="form2")
            form3 = AddFinanceForm(request.POST, prefix="form3")
            form4 = AddFinanceForm(request.POST, prefix="form4")
            if form1.is_valid() or form2.is_valid():
                try:
                    title = request.POST['form1-title']
                    form = 'form1'
                except:
                    form = 'form2'

                is_income = request.POST['is_income']
                title = request.POST[f'{form}-title']
                money = request.POST[f'{form}-money']
                date = request.POST[f'{form}-date']
                description = request.POST[f'{form}-description']
                finance = Finance.objects.create(title=title, money=money, date=date, user_id=user.id,
                                                 description=description, is_income=is_income)
                finance.save()
                if is_income == 'True':
                    messages.success(request, 'Доход добавлен')
                else:
                    messages.success(request, 'Расход добавлен')

                return redirect('my_finance')
            else:
                messages.error(request, 'Форма невалидна')
        else:
            form1 = AddFinanceForm(prefix="form1")
            form2 = AddFinanceForm(prefix="form2")
            form3 = AddFinanceForm(prefix="form3")
            form4 = AddFinanceForm(prefix="form4")
        incomes = Finance.objects.filter(user_id=user.id, is_income=True)
        expenses = Finance.objects.filter(user_id=user.id, is_income=False)
        context = {
            'incomes': incomes,
            'expenses': expenses,
            'form1': form1,
            'form2': form2,
            'form3': form3,
            'form4': form4,
        }
        return render(request, 'financetracker/my_finance.html', context=context)
    else:
        return redirect('register')


def delete_finance(request):
    if request.is_ajax():
        finance_id = int(request.POST.get('finance_id'))
        finance_obj = Finance.objects.get(pk=finance_id)
        finance_obj.delete()

        data = {
            'delete': True
        }
        return JsonResponse(data)


def redact_finance(request):
    if request.is_ajax():
        finance_red_id = request.POST.get('finance_red_id')
        redact_finance_obj = Finance.objects.get(pk=finance_red_id)

        print(request.POST)
        title = request.POST.get('redacted_title')
        money = request.POST.get('redacted_money')
        date = request.POST.get('redacted_date')
        description = request.POST.get('redacted_description')

        redact_finance_obj.title = title
        redact_finance_obj.money = money
        redact_finance_obj.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        redact_finance_obj.description = description

        redact_finance_obj.save()

        date = redact_finance_obj.date.strftime("%d %B %Y")
        data = {
            'id': redact_finance_obj.id,
            'title': redact_finance_obj.title,
            'money': redact_finance_obj.money,
            'date': date,
            'is_income': redact_finance_obj.is_income,
            'description': redact_finance_obj.description
        }

        print(data['date'])

        return JsonResponse(data)


def user_logout(request):
    logout(request)
    return redirect('index')