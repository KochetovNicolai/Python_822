import vkapi
import requests

def get_weather_today(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=' + city
    data = requests.get(url, params={'lang': 'ru'}).json()

    result = ''

    if data['cod'] == '404':
        result = 'Город не найден.'
    else:
        weather = data['weather']
        result += weather[0]['description'].capitalize() + '\n'
        temp = data['main']
        result += 'Температура воздуха: ' + str(round(temp['temp']-273, 1)) + ' °С' + '\n'

    return result

def get_weather_not_today(body):
    city = body.split()[0][0:-1]
    day = body.split()[1].split('.')[0]
    month = body.split()[1].split('.')[1]
    url = 'http://api.openweathermap.org/data/2.5/forecast?appid=0c42f7f6b53b244c78a418f4f181282a&q=' + city
    data = requests.get(url, params={'lang': 'ru'}).json()
    result = ''

    for i in data['list']:
        date = i['dt_txt'].split()[0]
        i_day = date.split('-')[2]
        i_month = date.split('-')[1]

        if day==i_day and month==i_month:
            result += city.capitalize() + ' погода на ' + day + '.' + month + ':' + '\n'
            weather = i['weather']
            result += weather[0]['description'].capitalize() + '\n'
            temp = i['main']
            result += 'Температура воздуха: ' + str(round(temp['temp']-273, 1)) + ' °С' + '\n'
            break

        else:
            pass

    if data['cod'] == '404':
        return 'Город, не найден.'
    elif result == '':
        return 'Данные введены некорректно. Формат ввода: город, DD.MM. Прогноз погоды доступен только на 5 дней вперёд.'
    else:
        return result



def create_answer(data, token):
    user_id = data['user_id']

    if data['body'].split()[0][-1] != ',':
        message = get_weather_today(data['body'].lower())
    else:
        message = get_weather_not_today(data['body'].lower())

    vkapi.send_message(user_id, token, message)
