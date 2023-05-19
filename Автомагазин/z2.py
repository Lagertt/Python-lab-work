
import json
import time
import random
import collections
from operator import itemgetter
import threading
import multiprocessing.dummy as multiprocessing

# самая продаваемая машина
def mostexpensive_car():
    AutoShop = loadJson()
    
    DictCar = {}
    for worker in AutoShop:
        for car in worker['sold cars']:
           DictCar[car['name']] = 0

    for worker in AutoShop:
        for car in worker['sold cars']:
           DictCar[car['name']] += 1

    c = collections.Counter(DictCar).most_common() 

    for elem in c[:1]:
        print("\nCамая продаваемая машина: " + elem[0])


# 5 самых дорогих запчастей
def top5_mostexpensive_part():
    AutoShop = loadJson()
    SortedDict = {}

    for worker in AutoShop:
        for part in worker['sold parts']:
           SortedDict[part['name']] = part['price']

    c = collections.Counter(SortedDict).most_common()  
    print("\n5 самых дорогих запчастей:")
    for elem in c[:5]:
        print('  *' + elem[0])

# самый эффективный сотрудник
def mosteffective_worker():
    AutoShop = loadJson()   
    
    performance = 0 # эффективность сотрудника (количество проданных запчастей и автомобилей)
        
    for worker in AutoShop:
        count_cars = 0 # кол-во проданных машин
        count_parts = 0 # кол-во проданных запчастей
        for i in range(len(worker['sold cars'])):
            count_cars += 1
        for i in range(len(worker['sold parts'])):
            count_parts += 1
        if 1.5 * count_cars + count_parts > performance:
            performance = 1.5 * count_cars + count_parts
            performance_worker = worker['name']
    print("\nСамый эффективный сотрудник: " + performance_worker)


# линейное решение 
def linearSolution():
    top5_mostexpensive_part()
    mostexpensive_car()
    mosteffective_worker()

timer = 5
# решение с помощью событий таймера
def TimerSolution():
    top5_mostexpensive_part()
    time.sleep(timer)

    mostexpensive_car()
    time.sleep(timer)

    mosteffective_worker()
    time.sleep(timer)
    

# генерация данных в файле
def generateJson():
    AutoShop = []

    print("Ща, я работаю, не мешайте...")
    list_cars = ["Mercedes E-class convertible", "Mercedes A-class sedan", "Mercedes GLB", "Mercedes GLE coupe", "Mercedes GLS Maybach", 
                 "Mercedes G-class", "Mercedes S-class coupe", "Mercedes EQC"]
    list_carsprice = [6.9, 2.8, 3.8, 8.7, 16.4, 13.7, 9.2, 7.3]

    list_parts = ["свечи", "диски", "двигатель", "тормозные колодки", "зимняя резина", "летняя резина", "амортизаторы", "воздушный фильтр"]
    list_partsprice = [2, 15, 300, 10, 15, 12, 8, 3]

    list_names = ["Ишеев Мефодий Юриевич", "Ахметов Платон Леонтиевич", "Талалихина Зоя Данииловна", "Аверин Агафон Никифорович", 
                  "Шелепина Ефросиния Юлиевна", "Соколова Роза Федотовна"]
    for i in range(6):
        name = list_names[i]
        sold_cars = []
        sold_parts = []
        for j in range(random.randint(0, 10)):
            rc = random.randint(0, 7)        
            new_car = {'name': list_cars[rc], 'price': list_carsprice[rc]}
            sold_cars.append(new_car)

        for j in range(random.randint(0, 10)):
            rp = random.randint(0, 7)
            new_part = {'name': list_parts[rp], 'price': list_partsprice[rp]}
            sold_parts.append(new_part)
            
        new_worker = {'name': name, 'sold cars': sold_cars, 'sold parts': sold_parts}
        AutoShop.append(new_worker)

    new_json = {"workers": AutoShop}
    with open("file.json", "w", encoding = 'utf-8') as write_file:
        json.dump(new_json, write_file, indent = 4, ensure_ascii=False)
            
    


# добавление записи 
def addRecord():
    AutoShop = loadJson()
    sold_cars = []
    sold_parts = []

    name = input('Введите ФИО: ')
    num_sold_cars = int(input('Введите количество проданных автомобилей: '))
    for i in range(num_sold_cars):
        name_car = input('Введите наименование автомобиля: ')
        price_car = float(input('Введите цену автомобиля в млн: '))
        new_car = {'name': name_car, 'price': price_car}
        sold_cars.append(new_car)

    num_sold_parts = int(input('Введите количество проданных запчастей: '))
    for i in range(num_sold_parts):
        name_part = input('Введите наименование запчасти: ')
        price_part = int(input('Введите цену запчасти в тыс: '))
        new_part = {'name': name_part, 'price': price_part}
        sold_parts.append(new_part)

    new_worker = {'name': name, 'sold cars': sold_cars, 'sold parts': sold_parts}
    AutoShop.append(new_worker)

    new_json = {"workers": AutoShop}
    with open("file.json", "w", encoding = 'utf-8') as write_file:
        json.dump(new_json, write_file, indent = 4, ensure_ascii=False)
    


def loadJson():
    with open("file.json", 'r', encoding = 'utf-8') as read_file:
        jDict = json.loads(read_file.read())
    return jDict.get('workers')  # возвращает список со словарями
   


m = input('Обновить данные  в json файле?\n1) Да\n2) Нет\nВведите номер команды: ')
if m == '1':
    generateJson()
    print('Файл сгенерирован')

n = input('\n1) Линейное решение\n2) Решение с таймером\n3) Добавить запись в '
          'json\n4) Выход\n\nВведите номер команды: ')

while n != '4':
    if n == '1':
        print('\n-----------------РЕЗУЛЬТАТЫ-----------------')
        linearSolution()
        print('\n--------------------------------------------')
    if n == '2':
        print('\n-----------------РЕЗУЛЬТАТЫ-----------------')
        TimerSolution()
        print('\n--------------------------------------------')
    if n == '3':
        addRecord()
    if n == '4':
        break
    n = input('\n1) Линейное решение\n2) Решение с таймером\n3) Добавить запись в '
          'json\n4) Выход\n\nВведите номер команды: ')


