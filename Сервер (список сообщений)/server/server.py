import socket
import os
import mimetypes
import time
import shutil



serv_sock = socket.socket()
serv_sock.bind(('', 9090))
serv_sock.listen(10)

print('Waiting for connection...')

while True:

    # Бесконечно обрабатываем входящие подключения
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)
    auth = False

    while True:
        try:
            # Пока клиент не отключился, читаем передаваемые
            # им данные и отправляем их обратно
            data = client_sock.recv(1024)            

            if data.decode() == 'authuserpass' :
                dict_auth = {}
                file_auth = open("Auth.txt", "r")
                while True:
                    line = file_auth.readline()
                    if not line:
                        break
                    pair = line.split()
                    dict_auth[pair[0]] = pair[1]
                file_auth.close
                
                client_sock.send("Логин: ".encode())
                login = client_sock.recv(1024).decode()
                client_sock.send("Пароль: ".encode())
                password = client_sock.recv(1024).decode()
                    
                if dict_auth.get(login, False) == password:
                    auth = True
                    client_sock.send("Авторизация успешна\n".encode())
                    print(str(client_addr) + ": user authorization " + login + " successful")

                else:
                    client_sock.send("Ошибка: неверный логин или пароль\n".encode())
                    print(str(client_addr) + ": user authorization " + login + " failed")

                    


            elif (data.decode().find('read') == 0) & (auth == True):    
                num = comand[5:]
                print(str(client_addr) + ": request to read the message " + str(num))
                msgs = os.listdir(mess + "\\messag\\" + usr)
                bl = False
                for i in msgs:
                    if bl == True:
                        break
                    pp = i.find(" ")
                    if i[:pp] == num:
                       file_msg = open((mess + "\\messag\\" + usr + "\\" + i), 'r')
                       elem = file_msg.read()
                       client_sock.send(str(elem).encode())
                       bl = True
                       file_msg.close()
                if bl == False:
                    client_sock.send("Ошибка: нет такого сообщения\n".encode())


                                                     

                
            
            elif (data.decode().find('send') == 0) & (auth == True):
                user = comand[5:]
                print(str(client_addr) + ": request to send a message to the " + str(user))
                mesus = os.listdir(os.getcwd() + "\\masseg\\" + user)
                if len(mesus) != 0:
                    lm = sorted(mesus,reverse=True)
                    pp1 = lm[0].find(" ")
                    lsms = lm[0][:pp1]
                    pp2 = int(lsms)+1
                else:
                    pp2 = 1
                client_sock.send("Введите тему:\n".encode())
                theme = client_sock.recv(1024).decode()
                mf = str(pp2) + " " + theme + ".txt"
                file = open(mf,'w')
                client_sock.send("Введите сообщение:\n".encode())
                text = client_sock.recv(1024).decode()
                file.write(text)
                file.close()
                path = os.getcwd() + "\\" + mf
                moveto = os.getcwd() + "\\masseg\\" + user + "\\" + mf
                shutil.move(path,moveto)




            elif data.decode() == 'help':
                print(str(client_addr) + ": request help on commands")
                client_sock.send(("list: показать список сообщений\n"
                                  "read <msg>: вывести сообщение под номером <msg>\n"
                                  "send <user>: ввод сообщения для пользователя <user>\n"
                                  "authuserpass: авторизация\n"
                                  "exit: выход\n"
                                  "help: справка по командам\n").encode())
                


            elif (data.decode() == 'list') & (auth == True):
                print(str(client_addr) + ": request list of messages")
                ms = os.listdir(mess+"\\messag\\"+usr)
                for i in ms:
                    m = i[:i.rfind(".")]
                    client_sock.send(str(m).encode())



            elif data.decode() == 'exit':
                print('Unconnected by ', client_addr)
                client_sock.close()
                break



            else:
               if auth == True:
                   client_sock.send("Я вас не понимаю :(\n".encode())
               else:                   
                   client_sock.send("Ошибка, вы не авторизированы\n".encode())



            if (not data) | (data.decode() == 'exit'):
                # Клиент отключился
                print('Unconnected by', client_addr)
                client_sock.close()
                break


        except:
            client_sock.send("Ой, ошибка, повторите попытку :(".encode())

  
serv_sock.close()



#import subprocess
#import sys
#import os,shutil
#import os.path,time
#
#chek_user=False
#chek_exit=False
#
#def auth(user, chek_user):#проверка авторизации
#    fpas=open('pass.txt','r')
#    for line in fpas:# поиск пользователя в фыйле с паролями
#        if user==line.rstrip():
#             chek_user=True
#             print("Вы авторизировались")
#             return True
#    if chek_user==False:
#            print("Неверный логин или пароль")
#            return False
#    fpas.close()
#
#
#
#while chek_exit==False:# главный цикл
#    comand=input("введите команду: ")
#    if comand[:4]=="auth":
#        if comand[:4]=="auth":
#         comand1=comand[5:]
#         chek_user=auth(comand1, chek_user)
#         ss=comand1.find(" ")
#         usr=comand1[:ss]
#         mess=(os.getcwd())
#    else:
#        if chek_user==True:
#            if comand=="list":
#                ms=os.listdir(mess+"\\masseg\\"+usr)
#                for i in ms:
#                    m=i[:i.rfind(".")]
#                    print(m)
#            else:
#                if comand[:4]=="read":
#                    num=comand[5:]
#                    msgs=os.listdir(mess+"\\masseg\\"+usr)
#                    bl=False
#                    for i in msgs:
#                        if bl==True:
#                            break
#                        pp=i.find(" ")
#                        if i[:pp]==num:
#                           f=open((mess+"\\masseg\\"+usr+"\\"+i), 'r')
#                           e=f.read()
#                           print(e)
#                           bl=True
#                           f.close()
#                    if bl==False:
#                        print ("Нет сообщения с таким номером")
#                else:
#                    if comand[:4]=="send":
#                        user=comand[5:]
#                        mesus=os.listdir(os.getcwd()+"\\masseg\\"+user)
#                        if len(mesus)!=0:
#                            lm=sorted(mesus,reverse=True)
#                            pp1=lm[0].find(" ")
#                            lsms=lm[0][:pp1]
#                            pp2=int(lsms)+1
#                        else:
#                            pp2=1
#                        print ("Введите тему")
#                        theme=input()
#                        mf=str(pp2)+" "+theme+".txt"
#                        f1=open(mf,'w')
#                        print ("Введите сообщение")
#                        text=input()
#                        f1.write(text)
#                        f1.close()
#                        path = os.getcwd()+"\\"+mf
#                        moveto = os.getcwd()+"\\masseg\\"+user+"\\"+mf
#                        shutil.move(path,moveto)
#                    else:
#                        if comand == "help":
#                            print("list — показать список сообщений")
#                            print("read msg — вывести сообщение под номером msg")
#                            print("send user — ввод сообщения для пользователя")
#                            print("exit — выход")
#                            print("help — справка по командам")
#                        else:
#                            if comand == "exit":
#                                chek_exit=True
#                            else:
#                                print("нет такой команды!")
#        else:
#            print("вы не авторизованы!")

