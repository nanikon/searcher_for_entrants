import requests
import hashlib
import datetime


class EntrantApplications:
    def __init__(self, fname):
        """Инициализация. Принимает в себя ФИО абитуриента в формате Фамилия Имя Отчество"""
        self.url = 'http://admlist.ru/fio/'
        self.fname = fname
        self.has = self.get_hash()
        self.apps = self.get_app()
        self.priority = self.get_priority()

    def get_hash(self):
        """Возвращает хэшированные ФИО"""
        hash_object = hashlib.md5(self.fname.encode())
        return hash_object.hexdigest()

    def get_url(self):
        """Возвращает URL через который можно получить json файл, одним из компонентов которого будет
        требуемый абитуриент"""
        first_date = datetime.datetime(1970, 1, 1)
        time_since = datetime.datetime.now() - first_date
        seconds = int(time_since.total_seconds() * 1000)
        return self.url + self.has[:2] + '.json?nocache=' + str(seconds)

    def get_app(self):
        """Возвращает список двухэлементных списков направлений абитуриента. Первый элемент внутреннего списка - код
        направления в БД сайта, второй элемент - человекоподобное название. Если абитуриента в системе нет,
        возвращает [['-', 'Абитуриент не найден']]"""
        result = requests.get(self.get_url()).json()
        try:
            return result[self.has]
        except KeyError:
            return [['-', 'Абитуриент не найден']]

    def get_priority(self):
        """Возвращает направление, на которое абитуриент подал заявление о согласии на зачисление, при этом
        удаляет его из списка направлений. Если такого нет, то возвращает 'Пока не подано'"""
        p = ['-', 'Пока не подано']
        for app in self.apps:
            if app[1].startswith('<b>'):
                p = self.apps.pop(self.apps.index(app))
                p[1] = p[1].replace('<b>', '').replace('</b>', '')
        return p