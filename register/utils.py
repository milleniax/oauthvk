import json
import urllib
import urllib.request
import requests
import time
from config import CLIENT_ID, CLIENT_SECRET


def auth(code):
    """Функция получает значения code для получения ключа доступа. Затем при помощи
    значения code сервер приложения получает ключ доступа access_token для доступа к API ВКонтакте.
    Далее при помощи API ВКонтакте получает имя авторизованного пользователя и список из 5 его друзей,
    выбранных в произвольном порядке. Функция возвращает сообщение с именем авторизованного
    пользователя и списком из 5 его друзей"""
    request_link = 'https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&redirect_uri=marselabdullin.myjino.ru/final/&code={2}'
    request_link = request_link.format(CLIENT_ID, CLIENT_SECRET, code)

    try:
        r = requests.get(url=request_link)
    except Exception as e:
        error_report = "<h1 style='color:blue'>Сервер ВКонтакте временно недоступен. Повторите попытку позже. </h1>"
        return error_report

    data = r.json()
    access_token = data['access_token']  
    user_id = data['user_id'] 
    
    return access_token, user_id
    
def info(access_token, user_id):

    request_link = "https://api.vk.com/method/users.get?user_ids={0}&fields=bdate&access_token={1}&v=5.101".format(user_id, access_token)

    try:
        # через API запрос получаем словарь в формате JSON
        r = requests.get(url=request_link)
    except Exception as e:
        error_report = "<h1 style='color:blue'>Сервер ВКонтакте временно недоступен. Повторите попытку позже. </h1>"
        return error_report

    data = r.json()
    # получаем имя авторизованного пользователя
    first_name = data['response'][0]['first_name']
    # получаем фамилию авторизованного пользователя
    last_name = data['response'][0]['last_name']
    greeting_string = 'Здравствуйте, {0} {1}, вы авторизованы'\
                                                .format(first_name, last_name)


    # создаем запрос на 5 друзей, выбранных в случайном порядке
    request_link = "https://api.vk.com/method/friends.get?order=random&count=5&access_token={0}&v=5.101 ".format(access_token)
    try:
        # через API запрос получаем словарь в формате JSON
        r = requests.get(url=request_link)
    except Exception as e:
        error_report = "<h1 style='color:blue'>Сервер ВКонтакте временно недоступен. Повторите попытку позже. </h1>"
        return error_report
    
    data = r.json()
    # получаем массив ID друзей
    array_of_friends_ID = data['response']['items']
    amount_of_friends = len(array_of_friends_ID)
    friends = []
    if amount_of_friends == 0:
        friends_info = 'У вас нет друзей'
        return greeting_string, friends_info, None
    elif amount_of_friends < 5:
        friends_info = 'У вас меньше 5 друзей:'
        for i in range(amount_of_friends):  # создаем список друзей
            user_id = str(array_of_friends_ID[i])
            time.sleep(0.5)
            # создаем запрос на данные пользователя из "ВКонтакт" по его ID
            request_link = "https://api.vk.com/method/users.get?user_ids={0}\
                            &fields=bdate&access_token={1}&v=5.101".format(user_id, access_token)
            try:
                # через API запрос получаем словарь в формате JSON
                r = requests.get(url=request_link)
            except Exception as e:
                error_report = "<h1 style='color:blue'>Сервер ВКонтакте временно недоступен. Повторите попытку позже. </h1>"
                return error_report
            data = r.json()
            temp_first_name = data['response'][0]['first_name']
            temp_last_name = data['response'][0]['last_name']
            new_string = '{0} {1}'.format(temp_first_name, temp_last_name)
            friends += new_string
        return greeting_string, friends_info, friends
    else:
        friends_info = '5 друзей из вашего контакт листа, выбранных в случайном порядке:'
        for i in range(amount_of_friends):  # создаем список друзей
            user_id = str(array_of_friends_ID[i])
            time.sleep(0.5)
            # создаем запрос на данные пользователя из "В Контакт" по его ID
            request_link = "https://api.vk.com/method/users.get?user_ids={0}&fields=bdate&access_token={1}&v=5.101"
            request_link = request_link.format(user_id, access_token)
            try:
                # через API запрос получаем словарь в формате JSON
                r = requests.get(url=request_link)
            except Exception as e:
                error_report = "<h1 style='color:blue'>Сервер ВКонтакте временно недоступен. Повторите попытку позже. </h1>"
                return error_report
            data = r.json()
            temp_first_name = data['response'][0]['first_name']
            temp_last_name = data['response'][0]['last_name']
            new_string = '{0} {1}'.format(temp_first_name, temp_last_name)
            friends.append(new_string)
            print(friends)

        return greeting_string,friends_info,friends
