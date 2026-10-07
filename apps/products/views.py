from django.shortcuts import render
from django.http import HttpResponse

# Временная функция для проверки работы сайта
def home_page_view(request):
    return HttpResponse("<h1>Главная страница</h1>")