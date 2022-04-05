# bs4, selenium, requests
import site_parser
import time

HUI = 2

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
    
    del parser


if __name__ == '__main__':
    main()



