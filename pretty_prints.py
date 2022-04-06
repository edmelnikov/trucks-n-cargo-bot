from constants import *


def car_pretty_ptint(dict):
    text = ''
    text += 'Город отправления: '
    if dict.get(CAR_CITY_OUT):
        text += dict[CAR_CITY_OUT]
    else:
        text += 'Не указано'

    text += '\nГород назначения: '
    if dict.get(CAR_CITY_IN):
        text += dict[CAR_CITY_IN]
    else:
        text += 'Не указано'

    text += '\nДата назначения: '
    if dict.get(CAR_DATE):
        text += dict[CAR_DATE]
    else:
        text += 'Не указано'

    text += '\nВес: '
    if dict.get(CAR_WEIGHT):
        text += dict[CAR_WEIGHT]
    else:
        text += 'Не указано'    

    text += '\nОбъем: '
    if dict.get(CAR_VOLUME):
        text += dict[CAR_VOLUME]
    else:
        text += 'Не указано'    

    text += '\nТип кузова: '
    if dict.get(CAR_BODY):
        text += dict[CAR_BODY]
    else:
        text += 'Не указано'       

    return text