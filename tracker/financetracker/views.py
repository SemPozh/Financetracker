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
import re
import calendar
from django.middleware.csrf import get_token



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

                if 'my-finance' in request.get_full_path():
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


def statistic(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = StatisticPeriodForm(request.POST, prefix="form")
            form1 = AddFinanceForm(request.POST, prefix="form1")
            form2 = AddFinanceForm(request.POST, prefix="form2")
            form3 = AddFinanceForm(request.POST, prefix="form3")
            form4 = AddFinanceForm(request.POST, prefix="form4")
            start_day = datetime.datetime.strptime(request.POST['form-date1'], '%Y-%m-%d')
            end_day = datetime.datetime.strptime(request.POST['form-date2'], '%Y-%m-%d')
            period_name = 'период'

        else:
            months = {
                '01': 'январь',
                '02': 'февраль',
                '03': 'март',
                '04': 'апрель',
                '05': 'май',
                '06': 'июнь',
                '07': 'июль',
                '08': 'август',
                '09': 'сентябрь',
                '10': 'октябрт',
                '11': 'ноябрь',
                '12': 'декабрь',
            }

            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year
            count_of_days = str(calendar.monthrange(current_year, current_month)[1])
            if len(str(current_month)) == 1:
                current_month = '0' + str(current_month)
            start_day = datetime.datetime.strptime(str(current_year) + '-' + current_month + '-01', '%Y-%m-%d')
            end_day = datetime.datetime.strptime(str(current_year) + '-' + str(current_month) + '-' + count_of_days,
                                                 '%Y-%m-%d')
            period_name = months[current_month]

            form = StatisticPeriodForm(prefix="form")
            form1 = AddFinanceForm(prefix="form1")
            form2 = AddFinanceForm(prefix="form2")
            form3 = AddFinanceForm(prefix="form3")
            form4 = AddFinanceForm(prefix="form4")

        days_count = int(re.search(r'\d+', str(end_day - start_day)).group(0)) + 1
        all_expenses = Finance.objects.filter(date__gte=start_day, date__lte=end_day, is_income=False)
        all_incomes = Finance.objects.filter(date__gte=start_day, date__lte=end_day, is_income=True)

        expenses_money = 0
        incomes_money = 0

        for expense in all_expenses:
            expenses_money += expense.money

        for income in all_incomes:
            incomes_money += income.money

        average_day_expenses = round(int(expenses_money) / days_count, 2)
        average_day_incomes = round(int(incomes_money) / days_count, 2)

        finance_diff = incomes_money - expenses_money

        context = {
            'form': form,
            'form1': form1,
            'form2': form2,
            'form3': form3,
            'form4': form4,
            'days_count': days_count,
            'all_expenses': all_expenses,
            'all_incomes': all_incomes,
            'expenses_money': expenses_money,
            'incomes_money': incomes_money,
            'average_day_expenses': average_day_expenses,
            'average_day_incomes': average_day_incomes,
            'finance_diff': finance_diff,
            'period_name': period_name
        }

        return render(request, 'financetracker/statistic.html', context=context)
    else:
        return redirect('register')


def ajax_statistic(request):
    if request.is_ajax():
        start_day = datetime.datetime.strptime(request.POST['date1'], '%Y-%m-%d')
        end_day = datetime.datetime.strptime(request.POST['date2'], '%Y-%m-%d')

        days_count = int(re.search(r'\d+', str(end_day - start_day)).group(0)) + 1
        all_expenses_list = list(Finance.objects.filter(date__gte=start_day, date__lte=end_day, is_income=False))
        all_incomes_list = list(Finance.objects.filter(date__gte=start_day, date__lte=end_day, is_income=True))

        all_expenses = []
        for item in all_expenses_list:
            finance_data = {
                'id': item.id,
                'title': item.title,
                'money': item.money,
                'date': item.date,
                'description': item.description
            }

            all_expenses.append(finance_data)

        all_incomes = []
        for item in all_incomes_list:
            finance_data = {
                'id': item.id,
                'title': item.title,
                'money': item.money,
                'date': item.date,
                'description': item.description
            }

            all_incomes.append(finance_data)

        expenses_money = 0
        incomes_money = 0

        for expense in all_expenses_list:
            expenses_money += expense.money

        for income in all_incomes_list:
            incomes_money += income.money

        average_day_expenses = round(int(expenses_money) / days_count, 2)
        average_day_incomes = round(int(incomes_money) / days_count, 2)

        finance_diff = incomes_money - expenses_money

        token = get_token(request)
        csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" />'.format(token)

        data = {
            'csrf_token_html': csrf_token_html,
            'days_count': days_count,
            'all_expenses': all_expenses,
            'all_incomes': all_incomes,
            'expenses_money': expenses_money,
            'incomes_money': incomes_money,
            'average_day_expenses': average_day_expenses,
            'average_day_incomes': average_day_incomes,
            'finance_diff': finance_diff,
        }

        return JsonResponse(data)
