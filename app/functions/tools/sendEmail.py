from PyQt5.QtWidgets import QWidget
import random
import yagmail

def send_code(email):
    USER = 'validador38@gmail.com'
    PASSWORD = 'svgcdnaiglujawdy '
    yag = yagmail.SMTP(USER,PASSWORD)
    CODE = random.randint(1000,9999)
    receiver = email
    topic = 'Código de sistema PROCURA'
    message = f'Sea bienvenid@ al sistema! \n\nSu código de un solo uso es: {CODE}'
    yag.send(to=receiver, subject=topic, contents=message)
    print(f'Mensaje enviado a {email}')
    return CODE

