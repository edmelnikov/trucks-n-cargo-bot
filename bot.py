#https://docs-python.ru/packages/biblioteka-python-telegram-bot-python/

from constants import *
from pretty_prints import *
import site_parser
from ast import Return
import logging
from pickle import TRUE
from tkinter import CURRENT
from typing import Tuple, Dict, Any

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> str:

    text = ("Выбери, что хочешь найти")
    buttons = [
        [
        InlineKeyboardButton(text='Найти машину', callback_data=str(FINDING_CAR)), 
        ], 
        [
        InlineKeyboardButton(text='Найти груз', callback_data=str(FINDING_CARGO))
        ]
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        "Привет! С помощью этого бота ты можешь найти груз или найти перевозчика."
    )
    update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_ACTION


def car_restart_or_new(update: Update, context: CallbackContext) -> str:

    context.user_data[CURRENT_CHOICE] = FINDING_CAR
    if context.user_data.get(RESTARTED_CAR):
        return find_car(update, context)
    
    else:
        text = f'Нужно ввести начальные параметры для поиска.'
        try:
            update.callback_query.answer()
            update.callback_query.message.reply_text(text=text)
        except AttributeError:
            update.message.reply_text(text)
        return car_add_first_params(update, context)


def car_add_first_params(update: Update, context: CallbackContext) -> str:

    if not context.user_data.get(CAR_PARAM_COUNTER):
        context.user_data[CAR_PARAM_COUNTER] = 1
        text = 'Введите город отправления'
        try:
            update.callback_query.answer()
            update.callback_query.message.reply_text(text=text)
        except AttributeError:
            update.message.reply_text(text)
        return CAR_ADD_FIRST_PARAMS

    if context.user_data.get(CAR_PARAM_COUNTER) == 1:
        
        context.user_data[RESTARTED_CAR] = TRUE
        context.user_data[FINDING_CAR] = {}
        context.user_data[FINDING_CAR][CAR_CITY_OUT] = update.message.text
        buttons = [
            [
            InlineKeyboardButton(text='Пропустить', callback_data=str(CANCEL_PARAM)), 
            ]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        text = 'Введите город назначения'
        update.message.reply_text(text=text, reply_markup=keyboard)
        context.user_data[CAR_PARAM_COUNTER] = 2

        return CAR_ADD_FIRST_PARAMS


    if context.user_data.get(CAR_PARAM_COUNTER) == 2: 

        context.user_data[FINDING_CAR][CAR_CITY_IN] = update.message.text
        text = f'Укажите дату погрузки или диапазон дат через тире'
        update.message.reply_text(text=text)
        context.user_data[CAR_PARAM_COUNTER] = 3

        return CAR_ADD_FIRST_PARAMS


    if context.user_data.get(CAR_PARAM_COUNTER) == 3: 

        context.user_data[FINDING_CAR][CAR_DATE] = update.message.text
        text = f'Укажите вес груза в тоннах'
        update.message.reply_text(text=text)
        context.user_data[CAR_PARAM_COUNTER] = 4

        return CAR_ADD_FIRST_PARAMS

    if context.user_data.get(CAR_PARAM_COUNTER) == 4: 

        context.user_data[FINDING_CAR][CAR_WEIGHT] = update.message.text
        text = f'Укажите объем груза в кубических метрах (m3)'
        buttons = [
            [
            InlineKeyboardButton(text='Пропустить', callback_data=str(CANCEL_PARAM)), 
            ]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text=text, reply_markup=keyboard)
        context.user_data[CAR_PARAM_COUNTER] = 5

        return CAR_ADD_FIRST_PARAMS
    
    if context.user_data.get(CAR_PARAM_COUNTER) == 5: 

        context.user_data[FINDING_CAR][CAR_DATE] = update.message.text
        text = f'Вы ввели все начальные параметры'
        del context.user_data[CAR_PARAM_COUNTER]
        update.message.reply_text(text)

        return find_car(update, context)    


def car_cancel_param(update: Update, context: CallbackContext) -> str:

    if context.user_data.get(CAR_PARAM_COUNTER) == 2:

        text = f'Укажите дату погрузки или диапазон дат через тире'
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text)
        context.user_data[CAR_PARAM_COUNTER] = 3
        
        return CAR_ADD_FIRST_PARAMS

    if context.user_data.get(CAR_PARAM_COUNTER) == 5:

        text = f'Вы ввели все начальные параметры'
        del context.user_data[CAR_PARAM_COUNTER]
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text)
        #update.callback_query.message.reply_text('...')

        return find_car(update, context)


def find_car(update: Update, context: CallbackContext) -> str:

    text = f'Параметры поиска машины:  \n\n'
    text_,_ = car_pretty_ptint(context.user_data[FINDING_CAR])
    text += text_
    buttons = [
        [
        InlineKeyboardButton(text='Город отправления', callback_data=str(CAR_CITY_OUT)), 
        InlineKeyboardButton(text='Город назначения', callback_data=str(CAR_CITY_IN))
        ], 
        [
        InlineKeyboardButton(text='Дата погрузки', callback_data=str(CAR_DATE)), 
        InlineKeyboardButton(text='Вес груза', callback_data=str(CAR_WEIGHT))
        ],
        [
        InlineKeyboardButton(text='Объем', callback_data=str(CAR_VOLUME)), 
        InlineKeyboardButton(text='Тип кузова', callback_data=str(CAR_BODY))
        ], 
        [
        InlineKeyboardButton(text='Запустить поиск', callback_data=str(CAR_SEARCH_RESULTS)), 
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    try:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    except AttributeError:
        update.message.reply_text(text=text, reply_markup=keyboard)

    return FINDING_CAR


def ask_update_text_param(update: Update, context: CallbackContext) -> str:

    context.user_data[CURRENT_CHANGE] = update.callback_query.data 

    text = f'Вы хотите поменять {context.user_data[CURRENT_CHANGE].lower()}. Пожалуйста, введите:'
    update.callback_query.edit_message_text(text=text)

    return TYPING 


def save_text_param(update: Update, context: CallbackContext) -> str:

    type_of_choice = context.user_data[CURRENT_CHOICE] 
    type_of_param = context.user_data[CURRENT_CHANGE] 
    if not context.user_data.get(type_of_choice):
        context.user_data[type_of_choice] = {}
    context.user_data[type_of_choice][type_of_param] = update.message.text
    del context.user_data[CURRENT_CHANGE] 

    if type_of_choice == FINDING_CAR:
        return find_car(update, context)

    elif type_of_choice == FINDING_CARGO:
        return find_cargo(update, context)


def car_start_search(update: Update, context: CallbackContext) -> str:
    
    _, temp_dict_ = car_pretty_ptint(context.user_data[FINDING_CAR])
    text = f'Поиск запущен ...'
    update.callback_query.answer()
    update.callback_query.message.reply_text(text=text)
    
    parser = site_parser.AtiTruckParser(delay_time=3)
    size_query = parser.make_new_query(city_from = temp_dict_[CAR_CITY_OUT],
                            city_to = temp_dict_[CAR_CITY_IN],
                            weight = temp_dict_[CAR_WEIGHT],
                            volume = temp_dict_[CAR_BODY],
                            cargo_type = temp_dict_[CAR_BODY]
                            )
    
    query = parser.get_listing_data()

    context.user_data[CAR_SEARCH_RESULTS] = [query]
    context.user_data[LISTING_COUNTER] = 0

    return display_results(update, context)


def display_prev(update: Update, context: CallbackContext) -> str:
    context.user_data[LISTING_COUNTER] -= 1
    return display_results(update, context)

def display_next(update: Update, context: CallbackContext) -> str:
    context.user_data[LISTING_COUNTER] += 1
    return display_results(update, context)


def display_results(update: Update, context: CallbackContext) -> str:

    choice = context.user_data[CURRENT_CHOICE]
    if choice == FINDING_CAR:

        if context.user_data[LISTING_COUNTER] == 0:
            list_num = context.user_data[LISTING_COUNTER]

            buttons = [
                [
                InlineKeyboardButton(text='Вперед', callback_data=str(NEXT)), 
                ], 
                [
                InlineKeyboardButton(text='Вернуться к меню поиска', callback_data=str(FINDING_CAR)), 
                ], 
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            text = f'Результаты поиска \n\n'
            text_ = display_pretty_print(context.user_data[CAR_SEARCH_RESULTS][0][list_num])
            text += text_
            text += f'\nстраница {list_num + 1}'
            update.callback_query.message.reply_text(text=text, reply_markup=keyboard)

            return DISPLAY_RESULTS

        elif context.user_data[LISTING_COUNTER] !=0 and context.user_data[LISTING_COUNTER] != len(context.user_data[CAR_SEARCH_RESULTS][0]) - 1:
            
            list_num = context.user_data[LISTING_COUNTER]

            buttons = [
                [
                InlineKeyboardButton(text='Назад', callback_data=str(PREV)), 
                InlineKeyboardButton(text='Вперед', callback_data=str(NEXT))
                ], 
                [
                InlineKeyboardButton(text='Вернуться к меню поиска', callback_data=str(FINDING_CAR)), 
                ], 
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            text = f'Результаты поиска \n\n'
            text_ = display_pretty_print(context.user_data[CAR_SEARCH_RESULTS][0][list_num])
            text += text_
            text += f'\nстраница {list_num + 1}'
            update.callback_query.message.reply_text(text=text, reply_markup=keyboard)

            return DISPLAY_RESULTS

        else:      
            list_num = context.user_data[LISTING_COUNTER]

            buttons = [
                [
                InlineKeyboardButton(text='Назад', callback_data=str(PREV)), 
                ], 
                [
                InlineKeyboardButton(text='Вернуться к меню поиска', callback_data=str(FINDING_CAR)), 
                ], 
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            text = f'Результаты поиска \n\n'
            text_ = display_pretty_print(context.user_data[CAR_SEARCH_RESULTS][0][list_num])
            text += text_
            text += f'\nстраница {list_num + 1}'
            update.callback_query.message.reply_text(text=text, reply_markup=keyboard)

            return DISPLAY_RESULTS



def find_cargo(update: Update, context: CallbackContext) -> str:

    print(update.callback_query.data)
    text = 'Эта ветка в разработке :(. Нажми /start'

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return SELECTING_ACTION

def done(update: Update, context: CallbackContext) -> str:

    del context.user_data[CURRENT_CHOICE]
    #del context.user_data[CURRENT_CHANGE]

    update.message.reply_text('Спасибо что воспользовались. Пока!')
    return ConversationHandler.END

def restart(update: Update, context: CallbackContext) -> str:
    del context.user_data[CURRENT_CHOICE]


