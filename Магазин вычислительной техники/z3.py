import pickle
import time
import random
import collections
from operator import itemgetter
from multiprocessing import Process

# самая продаваемая модель ноутбука
def mostexpensive_laptop():
    TechnoShop = loadPickle()
    
    DictLaptop = {}
    for worker in TechnoShop:
        for laptop in worker['sold laptops']:
           DictLaptop[laptop['name']] = 0

    for worker in TechnoShop:
        for laptop in worker['sold laptops']:
           DictLaptop[laptop['name']] += 1

    c = collections.Counter(DictLaptop).most_common() 

    for elem in c[:1]:
        print("\nCамая продаваемая модель ноутбука: " + elem[0])


# 5 самых дорогих видеокарт
def top5_mostexpensive_videocard():
    TechnoShop = loadPickle()
    SortedDict = {}

    for worker in TechnoShop:
        for card in worker['sold videocards']:
           SortedDict[card['name']] = card['price']

    c = collections.Counter(SortedDict).most_common()  
    print("\n5 самых дорогих видеокарт:")
    for elem in c[:5]:
        print('  *' + elem[0])

# самый эффективный сотрудник
def mosteffective_worker():
    TechnoShop = loadPickle()   
    
    performance = 0 # эффективность сотрудника (количество проданных ноутбуков и видеокарт)
        
    for worker in TechnoShop:
        сount_laptops = 0 # кол-во проданных ноутбуков
        count_videocards = 0 # кол-во проданных видеокарт
        for i in range(len(worker['sold laptops'])):
            сount_laptops += 1
        for i in range(len(worker['sold videocards'])):
            count_videocards += 1
        if сount_laptops + count_videocards > performance:
            performance = сount_laptops + count_videocards
            performance_worker = worker['name']
    print("\nСамый эффективный сотрудник: " + performance_worker)


# генерация данных в файле
def generatePickle():
    TechnoShop = []

    list_laptop = ["ASUS ZenBook", "HP EliteBook x360", "Microsoft Surface Book 2", "Dell XPS 15", "Apple MacBook Air 13", 
                 "Lenovo ThinkPad Edge", "Apple MacBook Pro", "Dell XPS 13", "Huawei MateBook X Pro", "Lenovo ThinkPad X1 Carbon"]
    list_laptop_price = [50, 110, 160, 130, 71, 50, 148, 69, 98, 95]

    list_videocard = ["NVIDIA GeForce RTX 3080 Ti", "NVIDIA GeForce RTX 3090", "NVIDIA RTX A4500", "AMD Radeon RX 6900 XT", "NVIDIA GeForce RTX",
                     "AMD Radeon RX 6800 XT", "NVIDIA GeForce RTX 3070 Ti", "NVIDIA RTX A5000", "NVIDIA GeForce RTX 3070", "NVIDIA GeForce RTX 2080 Ti"]
    list_videocard_price = [1848, 2632, 7214, 1731, 1680, 1382, 1059, 4512, 1012, 1268]

    list_names = ["Ишеев Мефодий Юриевич", "Ахметов Платон Леонтиевич", "Талалихина Зоя Данииловна", "Аверин Агафон Никифорович", 
                  "Шелепина Ефросиния Юлиевна", "Соколова Роза Федотовна"]
    for i in range(6):
        name = list_names[i]
        sold_laptops = []
        sold_videocards = []
        for j in range(random.randint(0, 10)):
            rl = random.randint(0, 9)        
            new_laptop = {'name': list_laptop[rl], 'price': list_laptop_price[rl]}
            sold_laptops.append(new_laptop)

        for j in range(random.randint(0, 10)):
            rv = random.randint(0, 9)
            new_videocard = {'name': list_videocard[rv], 'price': list_videocard_price[rv]}
            sold_videocards.append(new_videocard)
            
        new_worker = {'name': name, 'sold laptops': sold_laptops, 'sold videocards': sold_videocards}
        TechnoShop.append(new_worker)

    new_pickle = {"workers": TechnoShop}
    with open("file.pickle", "wb") as write_file:
        pickle.dump(new_pickle, write_file)
            
    


# добавление записи 
def addRecord():
    TechnoShop = loadPickle()
    sold_laptops = []
    sold_videocards = []

    name = input('Введите ФИО: ')
    num_sold_laptops = int(input('Введите количество проданных ноутбуков: '))
    for i in range(num_sold_laptops):
        name_laptop = input('Введите наименование ноутбука: ')
        price_laptop = float(input('Введите цену ноутбука в тыс: '))
        new_laptop = {'name': name_laptop, 'price': price_laptop}
        sold_laptops.append(new_laptop)

    num_sold_videocards = int(input('Введите количество проданных видеокарт: '))
    for i in range(num_sold_videocards):
        name_videocard = input('Введите наименование видеокарты: ')
        price_videocard = int(input('Введите цену видеокарты в USD: '))
        new_videocard = {'name': name_videocard, 'price': price_videocard}
        sold_videocards.append(new_videocard)

    new_worker = {'name': name, 'sold laptops': sold_laptops, 'sold videocards': sold_videocards}
    TechnoShop.append(new_worker)

    new_pickle = {"workers": TechnoShop}
    with open("file.pickle", "wb") as write_file:
        pickle.dump(new_pickle, write_file)
    


def loadPickle():
    with open("file.pickle", 'rb') as read_file:
        jDict = pickle.loads(read_file.read())
    return jDict.get('workers')  # возвращает список со словарями
   

m = input('Обновить данные  в pickle файле?\n1) Да\n2) Нет\nВведите номер команды: ')
if m == '1':
    generatePickle()
    print('Файл сгенерирован')

# линейное решение 
def linearSolution():
    top5_mostexpensive_videocard()
    mostexpensive_laptop()
    mosteffective_worker()

# решение с помощью процессов
def processSolution():    
        
        proc1 = Process(target = top5_mostexpensive_videocard())
        proc2 = Process(target = mostexpensive_laptop())
        proc3 = Process(target = mosteffective_worker())

        proc1.start()
        proc2.start()
        proc3.start()

        print("Processes are finished...")

if __name__ == '__main__':
    print('\n-----------------РЕЗУЛЬТАТЫ ЛИНЕЙНОГО РЕШЕНИЯ-----------------')
    linearSolution()
    print('\n--------------------------------------------')

    print('\n----------------РЕЗУЛЬТАТЫ РЕШЕНИЯ С ПРОЦЕССАМИ---------------')
    processSolution()
    print('\n--------------------------------------------')




