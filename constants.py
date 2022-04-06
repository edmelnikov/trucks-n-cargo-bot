(SELECTING_ACTION, FINDING_CARGO, FINDING_CAR) = ('SELECTED ACTION', 'поиск груза', 'поиск машины')
(
    CAR_CITY_OUT, 
    CAR_CITY_IN, 
    CAR_DATE, 
    CAR_WEIGHT, 
    CAR_VOLUME, 
    CAR_BODY, 
    CAR_BARGAIN, 
    CAR_SORT
) =  (
    'Город отправления',
    'Город назначения', 
    'Дата погрузки',
    'Вес груза',
    'Объем',
    'Тип кузова',
    'Возможность торга',
    'Тип сортировки'
)

(TYPING, CURRENT_CHOICE, CURRENT_CHANGE, RESTARTED_CAR, CAR_ADD_FIRST_PARAMS, CANCEL_PARAM) = (
    'typing', 
    'CURRENT_SEARCH_CHOICE', 
    'CURRENT_SEARCH_PARAM_CHANGE', 
    'RESTARTED_CAR', 
    'car_add_first_params', 
    'не указано'
)
CAR_PARAM_COUNTER = 'CAR_PARAM_COUNTER'
#CAR_SEARCH = 'CAR_SEARCH'
CAR_SEARCH_RESULTS = 'CAR_SEARCH_RESULTS'


DISPLAY_RESULTS = 'DISPLAY_RESULTS'
LISTING_COUNTER = 'LISTING_COUNTER'
NEXT = 'NEXT'
PREV = 'PREV'