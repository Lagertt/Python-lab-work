import socket
import os

def SolveEquation(A, B, C):
    D = B*B - 4*A*C
    if D >= 0:
        x1 = (-B-D)/(2*A)
        x2 = (-B+D)/(2*A)
    else:
        x1 = False
        x2 = False               
    
    return x1, x2

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
        # Пока клиент не отключился, читаем передаваемые
        # им данные и отправляем их обратно
        data = client_sock.recv(1024)          
                                   


        if (data.decode().find('LOGIN') == 0):    
            auth = data.decode()[6:].split()
            loginBEGIN = auth[0]
            password = auth[1]

            login = ''
            for s in loginBEGIN:
                if not s == ',':
                    login += s
            
            dict_auth = {}
            file_auth = open("Auth.txt", "r")
            while True:
                line = file_auth.readline()
                if not line:
                    break
                pair = line.split()
                dict_auth[pair[0]] = pair[1]
            file_auth.close

            if dict_auth.get(login, False) == password:
                auth = True
                client_sock.send("0\n".encode())
                print(str(client_addr) + ": user authorization " + login + " successful")
        
            else:
                client_sock.send("Error: 1\n".encode())
                print(str(client_addr) + ": user authorization " + login + " failed")




        elif data.decode() == 'help':
            print(str(client_addr) + ": request help on commands")
            client_sock.send(("LOGIN name, pass: вход в систему\n"
                              "STORE A B C: запомнить коэффициенты\n"
                              "SOLVE: решить уравнение с известными коэффициентами\n"
                              "SOLVE A B C: решить уравнение с указанными коэффициентами\n"
                              "exit: выход\n"
                              "help: справка по командам\n\n"
                              "Коды ответов сервера:\n"
                              "  0: нет ошибки\n"
                              "  1: ошибка авторизации\n"
                              "  2: не указаны коэффициенты\n"
                              "  3: синтаксическая ошибка\n").encode())



        elif (data.decode().find('STORE') == 0) & (auth == True):    
            coeff = data.decode()[6:].split()
            try:
                A = int(coeff[0])
                B = int(coeff[1])
                C = int(coeff[2])
                                
                print(str(client_addr) + ": the coefficients are recorder")
                client_sock.send("0\n".encode())
            except:
                client_sock.send("2\n".encode())

                                 
            

        elif (data.decode() == 'SOLVE') & (auth == True):  
            try:
                x1, x2 = SolveEquation(A, B, C)
                print(str(client_addr) + ": the solution of the equation has been started")
                if (not x1 == False):
                    client_sock.send(("0\n"
                                      "Answer: x1 = " + str('%.3f' % x1) + "      x2 = " + str('%.3f' % x2) + "\n").encode())
                else:
                    client_sock.send("Уравнение не имеет решений\n".encode())
            except:
                client_sock.send("2\n".encode())
        

        elif (data.decode().find('SOLVE') == 0) & (auth == True):   
            coeff = data.decode()[6:].split()
            try:
                A = int(coeff[0])
                B = int(coeff[1])
                C = int(coeff[2])

                x1, x2 = SolveEquation(A, B, C)
                print(str(client_addr) + ": the solution of the equation has been started")            
                if (not x1 == False):
                    client_sock.send(("0\n"
                                      "Answer: x1 = " + str('%.3f' % x1) + "      x2 = " + str('%.3f' % x2) + "\n").encode())
                else:
                    client_sock.send("Уравнение не имеет решений\n".encode())
            except:
                client_sock.send("2\n".encode())



        elif data.decode() == 'exit':
            print('Unconnected by ', client_addr)
            client_sock.close()
            break



        else:
           if auth == True:
               client_sock.send("3\n".encode())
           else:                   
               client_sock.send("1\n".encode())



        if (not data) | (data.decode() == 'exit'):
            # Клиент отключился
            print('Unconnected by', client_addr)
            client_sock.close()
            break



  
serv_sock.close()
