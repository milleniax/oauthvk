from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import requests
from . import utils
from config import CLIENT_ID, CLIENT_SECRET

def index(request):
    if 'access_token' not in request.COOKIES:  # проверяем браузер пользователя на наличие куки от нашего приложения
        # если куки не обнаружено значит пользователь зашел к нам в первый раз и направляем его на кнопку авторизации
        return render(request, 'register/register.html', )
    else:
        # если куки обнаружено - сразу перенаправляем пользователя на приложение авторизации
        return HttpResponseRedirect("http://marselabdullin.myjino.ru/login/")


def login(request):
    try:
        link = "https://oauth.vk.com/authorize?client_id={0}&scope=friends,offline&redirect_uri=http://marselabdullin.myjino.ru/final/&response_type=code".format(CLIENT_ID)
        print(link)
        r = requests.get(url=link)
        return HttpResponseRedirect("https://oauth.vk.com/authorize?client_id={0}&scope=friends,offline&redirect_uri=http://marselabdullin.myjino.ru/final/&response_type=code".format(CLIENT_SECRET))
    except Exception as e:
        response = "<h1 style='color:blue'>Сервер ВКонтакте временно недоступен. Повторите попытку позже. </h1>"
        return HttpResponse(response)


def final(request):
    # записываем в переменную текущую ссылку
    current_url = request.build_absolute_uri()
    code = current_url[44:]  # получаем код из ссылк
    # функция vk_utility.auth на входе получает код. при помощи кода получает доступ к списку друзей пользователя
    if 'access_token' not in request.COOKIES:
        access_token, user_id = utils.auth(code)
        greeting, friends_info, friends = utils.info(access_token, user_id)
        response = render(request, 'register/profile.html', {'greeting': greeting, 'friends_info': friends_info, 'friends': friends})
        response.set_cookie('access_token', access_token)
        response.set_cookie('user_id', user_id)
        
    else:
        greeting, friends_info, friends = utils.info(request.COOKIES.get('access_token'), request.COOKIES.get('user_id'))
        response = render(request, 'register/profile.html',
                          {'greeting': greeting, 'friends_info': friends_info,
                           'friends': friends})
    
    # и возвращает список из 5 друзей пользователя
       
    return response
