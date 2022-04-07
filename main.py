# bs4, selenium, requests
import site_parser
import time
from bot import *
from constants import *
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

def main() -> None:
    """Run the bot."""

    # Create the Updater and pass it your bot's token.
    updater = Updater("5271615777:AAGH0_TAUSpXvUV9f8SNBbb26CJwYJ3ipZU", workers = 1024)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        allow_reentry= True ,

        states={
            SELECTING_ACTION: [
                CallbackQueryHandler(car_restart_or_new, pattern='^' + str(FINDING_CAR) + '$'),
                CallbackQueryHandler(find_cargo, pattern='^' + str(FINDING_CARGO) + '$'),
            ], 
            CAR_ADD_FIRST_PARAMS:[
                MessageHandler(Filters.text & (~Filters.command), car_add_first_params), 
                CallbackQueryHandler(car_cancel_param, pattern='^' + str(CANCEL_PARAM) + '$')

            ], 

            FINDING_CAR: [
                CallbackQueryHandler(ask_update_text_param, pattern='^' + str(CAR_CITY_OUT) + '$'), 
                CallbackQueryHandler(ask_update_text_param, pattern='^' + str(CAR_CITY_IN) + '$'), 
                CallbackQueryHandler(ask_update_text_param, pattern='^' + str(CAR_DATE) + '$'),
                CallbackQueryHandler(ask_update_text_param, pattern='^' + str(CAR_WEIGHT) + '$'), 
                CallbackQueryHandler(ask_update_text_param, pattern='^' + str(CAR_VOLUME) + '$'), 
                CallbackQueryHandler(car_start_search, pattern='^' + str(CAR_SEARCH_RESULTS) + '$')

            ], 

            DISPLAY_RESULTS: [
                CallbackQueryHandler(display_next, pattern='^' + str(NEXT) + '$'),
                CallbackQueryHandler(display_prev, pattern='^' + str(PREV) + '$'),
                CallbackQueryHandler(find_car, pattern='^' + str(FINDING_CAR) + '$')

            ], 

            TYPING: [
                MessageHandler(Filters.text, save_text_param)
            ]
        },

        fallbacks=[
            CommandHandler('end', done),
            ],
        run_async= True
    )

    
    dispatcher.add_handler(conv_handler)
    #dispatcher.add_handler(CommandHandler('findcar', car_restart_or_new))
    #dispatcher.add_handler(CommandHandler('findcargo', find_cargo))
    #dispatcher.add_handler(CommandHandler('start', start))
    # Start the Bot
    updater.start_polling()

    updater.idle()

# for parser testing
# def main2():
#     parser = site_parser.AtiTruckParser(delay_time=5)
#     print(parser.make_new_query(city_from='Москва', city_to='Санкт-Петербург'))
#     if parser.load_next_page():
#         print(parser.get_listing_data())

if __name__ == '__main__':
    main()
    # main2()


'''
def main():

    # Example of AtiTruckParser usage
    parser = site_parser.AtiTruckParser(delay_time=3)
    #
    print(parser.make_new_query(city_from="Санкт-Петербург",
                                city_to="Москва",
                                weight=25,
                                volume=30,
                                cargo_type=None
                                ))
    if parser.load_next_page():
        print(parser.get_listing_data())

    if parser.load_next_page():
        print(parser.get_listing_data())

    if parser.load_next_page():
        print(parser.get_listing_data())

    # Example of AtiCargoParser usage
    # parser = site_parser.AtiCargoParser(delay_time=5)  # create an object
    # num_listings = parser.make_new_query(city_from="Омск", city_to="Нижний Новгород")  # make a query
    # print(num_listings)
    # if num_listings > 0:  # if there are listings matching the query, get the data
    #     print(parser.get_listing_data())  # get data from current page
    #     if parser.load_next_page():  # load next page
    #         print(parser.get_listing_data())  # get data from the next page
    #     # and so on and so forth...
    #     if parser.load_next_page():
    #         print(parser.get_listing_data())
    #     if parser.load_next_page():
    #         print(parser.get_listing_data())
    #     # time.sleep(5)
    
    del parser'''
