import socket
import threading

protocols_list = {22: "SSH", 53: "DNS", 80: "HTTP", 143: "IMAP", 443: "HTTPS", 21: "FTP", 23: "TELNET", 135: 'EPMAP', 139:'NETBIOS-SSN', 445:'MICROSOFT-DS',
                  465: "SMTP", 563: "NNTP", 990: "FTP"}


def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        sock.connect((ip, port))
        print('PORT :', port, 'OPEN, ', "TYPE -", protocols_list.get(port))
        sock.close()
    except:
        pass


ip = socket.gethostbyname(socket.gethostname())
print("\nIP:", ip)


for i in range(10000):
    protocol = threading.Thread(target=scan_port, args=(ip, i))
    protocol.start()

