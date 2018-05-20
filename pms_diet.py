"""
pms_diet.py: Weekly Randomized PMS Meal Plan inspired by www.cyclediet.com

__author__ = 'Tariana Gomes Rodovalho'
__email__ = 'tariana.rodovalho@gmail.com'

"""

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

import random
import calendar
import pandas
import locale
import base64

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


class Waiter:
    def __init__(self):
        self.sender = 'tariana.rodovalho@gmail.com'
        self.subscribers = ['leo.olberg@gmail.com', 'tarianarodovalho@hotmail.com']
        self.api_url = 'https://www.googleapis.com/auth/gmail.send'
        
    def create_message(self, message_text):
        message = MIMEText(message_text, 'html')
        message['to'] = ', '.join(self.subscribers)
        message['from'] = self.sender
        message['subject'] = 'Plano Alimentar da Semana'
        raw = base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': raw.decode()}
    
    def send_plates(self, message):
        user_id = 'me'
        try:
            service = self.__setup_service()
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print ('Message Id: %s' % message['id'])
            return message
        except HttpError as error:
            print ('An error occurred: %s' % error)
    
    def __setup_service(self):
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', self.api_url)
            creds = tools.run_flow(flow, store)
        return build('gmail', 'v1', http=creds.authorize(Http()))
    


class Chef:
    def __init__(self):  
        self.meal_names = ['Café-da-manhã', 'Almoço', 'Lanche', 'Jantar']
        self.plates = [
                [
                "Um copo de leite desnatado com um copo de cereal sem glúten e um copo de morangos ou 1/4 de blueberry ou meia banana",
                "omelete com pimentão verde e tomate e uma fatia de pão integral ou sem glúten e uma laranja pequena",
                "Um copo de mingau de aveia com um copo de leite e 14 nozes e um copo de melão",
                "Sanduiche de muffim ingles: um ovo, uma colher de sopa de manteiga, um1 muffim inglês integral ou sem glúten, uma fatia de queijo branco, e 1 copo de leite",
                "2/3 (copo) de farelo ou cereal de arroz, um copo de leite desnatado, meio de berries ou meio banana",
                "Meio copo de iogurte com meio copo de berries, 14 nozes, 1/3 de cereal integral ou sem glúten e complete o copo com iogurte",
                "Omelete de 2 ovos, pimentão verde, brócolis e cebola, 1 fatia de torrada integral ou sem glúten, 100ml de suco de laranja ou uva",
                "Um copo de mingau de aveia, um copo de leite e meio copo de berries",
                "Um copo de vitamina de frutas com 10 amêndoas"
            ],
            [
                "Um copo de frango com vegetais e uma colher de sopa de amendoim, salada de espinafre, alface e pêras com molho de vinagrete",
                "Salada de espinafre com 100g peito de frango grelhado, tomate, pepino, salsão, cebola vermelha e ovo cozido e 2 colheres (sopa) de molho de vinagrete",
                "Um copo de sopa de frango, legumes e macarrao com 50g de peru com alface temperada com uma colher de sopa de mostarda",
                "Frango assado com um copo de vegetais cozidos e uma maçã",
                "Uma batata pequena assada com frango com molho de mostarda e salada de alface com tomate, cebola e pepino e uma maçã",
                "Iscas de peito de frango grelhado com pimentão verde e vermelho, cebola, alho e azeite de oliva, arroz castanho e uma laranja fatiada",
                "Sanduiche integral recheado com 2/3 copo de salada de atum (uma lata de atum com uma colher de sopa de maionese e meio aipo, 2 colheres (sopa) de cebola e 2 ovos cozidos) e pimentão, pepino e tomate",
                "Um copo de sopa de lentilhas com uma fatia de pão integral, uma colher de sopa de amendoim, salada de alface com espinafre ao molho de vinagrete e meio fruta",
                "Uma pizza de espinafre com tomates, cebolas e amêndoas, meio laranja",
                "Almôndegas com meio copo de arroz ou batata assada, um copo de vagem e meio maçã",
                "Um filé de peixe com meio copo de arroz integral com amêndoas, meio copo de vagem e uma fruta"
            ],
            [
                "Uma laranja pequena e 22 amêndoas",
                "20g mussarela com 3 tomates cereja",
                "Cinco cenourinhas com uma pêra",
                "Uma maçã com 1 colher (sopa) de amendoim",
                "Morangos com iogurte desnatado",
                "Uma colher (sopa) semente de girassol com 10 uvas",
                "Uma fatia de pão integral, 1 colher (sopa) de pasta de amendoim e meia banana",
                "Wrap de alface com pimentão verde e maionese",
                "Um copo de iogurte com 1/4 de cereal sem açucar"
            ],
            [
                "Salada de espinafre com tomate e cebola vermelha e amêndoas, meio copo de arroz, 100g de peixe grelhado temperado com azeite, alho, especiarias e limão",
                "Um copo e meio de chilli com salada de folhas",
                "Um copo e meio de espaguete com abóbora ao molho marinara, 100 g de peito de frango grelhado, meio copo de brócolis com ervilha e cogumelos, salada de espinafre e um pãozinho de trigo",
                "Meio copo de arroz, um copo de cenoura ralada, filé de frango grelhado com suco de laranja",
                "Wrap de vegetais grelhados",
                "100g de salmão grelhado, um copo de ervilhas sauté com cebolas e 10 amêndoas, salada de espinafre com molho de vinagrete e uma laranja pequena",
                "100g de filé de peixe com 1/2 copo de arroz integral com ervilhas, salada de espinafre com tomates, cebola vermelha e 10 amêndoas",
                "Burrito de feijão preto com arroz, milho verde, salada de espinafre com tomate e pepino",
                "Curry de vegetais com arroz basmati, salada de espinafre com fatias de pêra e pêssego",
                "Lasanha integral de espinafre com um copo de vegetais à escolha e uma fruta",
                "Pimentão recheado, meio copo de arroz, salada de espinafre e uma laranja"
            ]]  
        self.note = "OBS: Ingerir 1 colher de sopa de linhaça (ou 1 capsula de linhaça ou de óleo de peixe) 3x ao dia."

    def shorten_days_of_week(self):
        return dict(zip(calendar.day_abbr,range(7)))
        
    def __sort_menu_for_week(self):
        sorted_menu = []
        for plate in self.plates:
            sorted_menu.append(random.sample(plate, 7))
        return sorted_menu
    
    def create_menu(self):
        sorted_menu = self.__sort_menu_for_week()
        days_of_week_abbr = self.shorten_days_of_week().keys()
        pandas.set_option('display.max_colwidth',200)       
        menu_table = pandas.DataFrame(sorted_menu, self.meal_names, days_of_week_abbr)
        menu_table.style.set_properties(**{'text-align': 'center'})
        return menu_table.to_html() + self.note

waiter = Waiter()
chef = Chef()
menu = chef.create_menu()
message = waiter.create_message(menu)
waiter.send_plates(message)
