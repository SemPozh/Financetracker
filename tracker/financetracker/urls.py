from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('reviews/', review, name='reviews'),
    path('load-more-reviews/', ajax_reviews, name='load-more-reviews'),
    path('my-finance/', my_finance, name='my_finance'),
    path('delete_finance/', csrf_exempt(delete_finance),  name='delete_finance'),
    path('redact_finance/', redact_finance, name='redact_finance'),
    path('logout/', user_logout, name='logout'),
    path('statistic/', statistic, name='statistic'),
    path('ajax_statistic/', ajax_statistic, name='ajax_statistic')
]