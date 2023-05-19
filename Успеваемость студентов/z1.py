
import json
import random
import collections
from operator import itemgetter
from threading import Thread
import multiprocessing.dummy as multiprocessing

# топ-10 предметов по сложности
def top10most_difficult():
    studentsArray = loadJson()
    SortedDict = {}
    dictSubjectAndCount = collections.Counter()  
    dictSubjectAndMark = collections.Counter()
    dictSubjectAndLeave = collections.Counter()
    for d in studentsArray:
        dictSubjectAndCount[d['subject']] += 1 # предмет и кол-во оценок по нему
        dictSubjectAndMark[d['subject']] += (d['mark']) #предмет с суммой оценок по нему
        dictSubjectAndLeave[d['subject']] += (d['leave']) #предмет с суммой пропусков по нему

    for names in (dictSubjectAndCount.keys()):
        SortedDict[names] = dictSubjectAndMark[names] / dictSubjectAndCount[names] + 0.2 * dictSubjectAndLeave[names]

    c = collections.Counter(SortedDict).most_common()  
    c.reverse()
    print('\n10 самых трудных предметов:')
    for elem in c[:10]:
        print(elem[0])

# топ-10 по успеваемости
def top10performance():
    studentsArray = loadJson()
    # сумма баллов по предметам
    marks = collections.Counter()
    # кол-во предметов
    counts = collections.Counter()
    performance = {}
    for people in studentsArray:
        marks[people['name']] += people['mark']
        counts[people['name']] += 1
    for names in list(marks.keys()):
        performance[names] = marks[names] / counts[names]
    print("\nТоп 10 студентов по успеваемости:")
    for student in sorted(performance.items(), key=itemgetter(1), reverse=True)[:10]:
        print(student)

# топ-10 по прогулам
def top10_leave():
    studentsArray = loadJson()
    # кол-во прогулов
    counts = collections.Counter()
    for people in studentsArray:
        counts[people['name']] += people['leave']
    print("\nТоп 10 студентов по прогулам:")
    for student in counts.most_common()[:10]:
        print(student)

# линейное решение 
def linearSolution():
    top10most_difficult()
    top10performance()
    top10_leave()

# решение с помощью потоков
def threadingSolution():
    thread1 = Thread(target=top10most_difficult)
    thread2 = Thread(target=top10performance)
    thread3 = Thread(target=top10_leave)
    thread1.start()
    thread2.start()
    thread3.start()


# генерация данных в файле
def generateJson():
    studentsArray = []
    print("Ща, я работаю, не мешайте...")
    list_subjects = ["Матанализ", "АиП", "АиС", "Философия", "СППО", "Алгем", "Диффуры", "ЯП", "ВС", "История", "ТерВер", "Английский", "Дискретка", "Матлогика", "ОС"]
    list_names = ["Ишеев Мефодий Юриевич", "Ахметов Платон Леонтиевич", "Талалихина Зоя Данииловна", "Аверин Агафон Никифорович", 
              "Шелепина Ефросиния Юлиевна", "Соколова Роза Федотовна", "Артамонов Василий Сократович", "Игошин Андрей Владиславович",
              "Костина Ульяна Яновна", "Кабальнов Эрнст Наумови", "Осминин Владимир Маркович", "Садовничий Эвелина Мефодиевна", "Ялчевский Фома Михеевич",
              "Юнкин Кирилл Трофимович", "Кахадзе Доминика Семеновна"]
    for i in range(15):
        name = list_names[i]
        for j in range(15):
            subject = list_subjects[j]
            mark = random.randint(2, 5)
            leave = random.randint(0, 5)

            new_student = {'name': name, 'subject': subject, 'mark': mark, 'leave': leave}

            studentsArray.append(new_student)
    new_json = {"students": studentsArray}
    with open("file.json", "w", encoding = 'utf-8') as write_file:
        json.dump(new_json, write_file, indent = 4, ensure_ascii=False)
            
    


# добавление записи
def addRecord():
    studentsArray = loadJson()
    name = input('Введите ФИО: ')
    subject = input('Введите предмет: ')
    mark = float(input('Введите средний балл по предмету: '))
    leave = int(input('Введите кол-во прогулов по предмету: '))

    new_student = {'name': name, 'subject': subject, 'mark': mark, 'leave': leave}

    studentsArray.append(new_student)

    new_json = {"students": studentsArray}

    with open("file.json", "w", encoding = 'utf-8') as write_file:
        json.dump(new_json, write_file, indent = 4, ensure_ascii=False)
    


def loadJson():
    with open("file.json", 'r', encoding = 'utf-8') as read_file:
        jDict = json.loads(read_file.read())
    return jDict.get('students')  # возвращает список со словарями
   


m = input('Обновить данные  в json файле?\n1) Да\n2) Нет\nВведите номер команды: ')
if m == '1':
    generateJson()
    print('Файл сгенерирован')

n = input('\n1) Линейное решение\n2) Решение с потоками\n3) Добавить запись в '
          'json\n4) Выход\n\nВведите номер команды: ')

while n != '4':
    if n == '1':
        linearSolution()
    if n == '2':
        threadingSolution()
    if n == '3':
        addRecord()
    if n == '4':
        break
    n = input('\n1) Линейное решение\n2) Решение с потоками\n3) Добавить запись в '
          'json\n4) Выход\n\nВведите номер команды: ')

