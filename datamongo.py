'''
# Домашнее задание к лекции 2.4 «Database. Mongo. ORM»

1. Вы реализуете приложение для поиска билетов на концерт. 
Заполните коллекцию в Монго данными о предстоящих концертах и 
реализуйте следующие функции:

- `read_data`: импорт данных из csv [файла](https://github.com/netology-code/py-homework-advanced/blob/master/2.4.DB.Mongo.ORM/artists.csv);
- `find_cheapest`: отсортировать билеты из базы по возрастанию цены;
- `find_by_name`: найти билеты по исполнителю, где имя исполнителя 
может быть задано не полностью, и вернуть их по возрастанию цены.


## Дополнительное задание

- Реализовать сортировку по дате мероприятия. Для этого вам потребуется 
строку с датой в csv-файле приводить к объекту datetime (можете считать,
 что все они текущего года) и сохранять его.

Пример поиска: найти все мероприятия с 1 по 30 июля.


python
'''

import csv
import re
import bson

from pymongo import MongoClient


def mk_mongodb(dbname, collname):
    client = MongoClient('localhost')
    db = client.dbname
    db.collname
    return db

def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    result = []
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        for row in reader:
            db.art_collection.insert(row)
    return db.name

def find_cheapest(db, collname):
    """
    Отсортировать билеты из базы по возрастанию цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """
    result = mydb.collname.find().sort('Price', 1)
    return result


def find_by_name(db, collname):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """
    search_name = input('Введите регулярное выражение для поиска: ')
    prep_regexp = re.sub('[^A-Za-zА-Яа-я0-9- ]+', '', search_name)
    regex = bson.regex.Regex(prep_regexp)
    result = db.collname.find({'Исполнитель' : regex}).sort('Price', 1)
    return result


def clear_db(dbname, collname):
    client = MongoClient('localhost')
    db = client[dbname]
    mycol = db[collname]
    mycol.drop()


if __name__ == '__main__':
    mydb = mk_mongodb()
    mydb_name = read_data('artists.csv', mydb)
    for k in mydb.art_collection.find():
        print('ispolnitel:', k['Исполнитель'],'cena',k['Price'])
    searched_names = find_by_name(mydb)
    print(searched_names)
    clear_db(mydb_name)


