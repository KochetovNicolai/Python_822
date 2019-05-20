import requests
import bs4


class Functions:

    def get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        try:
            kek = bs.findAll("title")
        except:
            return 'Unknown name'
        return kek[0].text.split()[0]

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        return result

    @staticmethod
    def get_weather(town):

        city = str(town).lower()
        request = requests.get("https://sinoptik.com.ru/погода-" + city)
        print("Request status code: ", request.status_code)
        if request.status_code == 404:
            return "Я не знаю такого города"
        b = bs4.BeautifulSoup(request.text, "html.parser")
        try:
            temperature = []
            for i in range(3, 7):
                k = b.select('.temperature .p{}'.format(i))
                temperature.append(k[0].getText())

            result = ''
            result = result + ('Утром :' + temperature[0] + ' ' + temperature[1]) + '\n'
            result = result + ('Днём :' + temperature[2] + ' ' + temperature[3]) + '\n'
            description = b.select('.rSide .description')
            weather = description[0].getText()
            result = result + weather.strip()
        except:
            return 'Unknown weather'
        return result

    @staticmethod
    def get_time():
        try:
            request = requests.get("https://my-calend.ru/date-and-time-today")
            b = bs4.BeautifulSoup(request.text, "html.parser")
            all_info_from_page = b.select(".page")[0]  # возвращает всю информацию со страницы
            find_time = all_info_from_page.findAll("h2")[1]  # возвращает не распаршенную информацию о времени
            # (она идет во втором блоке h2)
        except:
            return 'Unknown time'
        return find_time.text

    # аналогичная ситуация с датой

    @staticmethod
    def get_date():
        try:
            request = requests.get("https://my-calend.ru/date-and-time-today")
            b = bs4.BeautifulSoup(request.text, "html.parser")
            all_info_from_page = b.select(".page")[0]
            find_date = all_info_from_page.findAll("h2")[0]
            time = find_date.text
        except:
            return 'Unknown date'
        return time

