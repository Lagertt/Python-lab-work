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

                    


            elif (data.decode().find('retr') == 0) & (auth == True):    
                list_files = data.decode()[5:].split()
                client_sock.send("Введите путь до папки: ".encode())
                path = client_sock.recv(1024).decode()
                print(str(client_addr) + "^" + str(login) + ": file transfer request in " + path)
                begin_path = str(os.path.abspath(os.curdir))
                for file in list_files:
                    shutil.move(str(os.path.abspath(os.curdir)) + "\\" + str(file), path)
                client_sock.send("Файлы перемещены\n".encode())
                    

                

                
            
            elif (data.decode() == 'infofile') & (auth == True):
                client_sock.send("Введите путь до файла: ".encode())
                path = client_sock.recv(1024).decode()
                print(str(client_addr) + "^" + str(login) +": request for file information " + path)
                file_type, a = mimetypes.guess_type(path, strict=True)
                client_sock.send(("Информация о файле " + path + ":" + 
                                  "\n    размер: " + str(os.stat(path).st_size) + " байт"
                                  "\n    MIME тип: " + str(file_type) + 
                                  "\n    время создания: " + str(time.ctime(os.stat(path).st_ctime)) + "\n").encode())



            elif data.decode() == 'help':
                print(str(client_addr) + ": request help on commands")
                client_sock.send(("list: показать список файлов в каталоге запуска программы\n"
                                  "infofile: показать сведения о файле\n"
                                  "authuserpass: авторизация\n"
                                  "retr <file_1> <file_n>: передать файлы, указанные в строке\n"
                                  "exit: выход\n"
                                  "help: справка по командам\n").encode())
                


            elif (data.decode() == 'list') & (auth == True):
                print(str(client_addr) + "^" + str(login) +": requesting a list of files in a directory")
                res = os.listdir(path=".")
                client_sock.send(("Файлы в текущей папке:\n" + str(res) + "\n").encode())



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