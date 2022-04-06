from tkinter.messagebox import NO
from constants import *


def car_pretty_ptint(dict):
    dict_with_nones = dict.copy()
    text = ''
    text += 'Город отправления: '
    if dict.get(CAR_CITY_OUT):
        text += dict[CAR_CITY_OUT]
    else:
        text += 'Не указано'
        dict_with_nones[CAR_CITY_OUT] = None

    text += '\nГород назначения: '
    if dict.get(CAR_CITY_IN):
        text += dict[CAR_CITY_IN]
    else:
        text += 'Не указано'
        dict_with_nones[CAR_CITY_IN] = None

    text += '\nДата назначения: '
    if dict.get(CAR_DATE):
        text += dict[CAR_DATE]
    else:
        text += 'Не указано'
        dict_with_nones[CAR_DATE] = None

    text += '\nВес: '
    if dict.get(CAR_WEIGHT):
        text += dict[CAR_WEIGHT]
    else:
        text += 'Не указано'
        dict_with_nones[CAR_WEIGHT] = None    

    text += '\nОбъем: '
    if dict.get(CAR_VOLUME):
        text += dict[CAR_VOLUME]
    else:
        text += 'Не указано'  
        dict_with_nones[CAR_VOLUME] = None  

    text += '\nТип кузова: '
    if dict.get(CAR_BODY):
        text += dict[CAR_BODY]
    else:
        text += 'Не указано'   
        dict_with_nones[CAR_BODY] = None    

    return text, dict_with_nones

def display_pretty_print(dict):

    text = f''

    for elem in dict.keys():
        text += f'{elem}: {dict[elem]} \n'

    return text