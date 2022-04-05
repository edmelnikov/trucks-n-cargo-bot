# bs4, selenium, requests
import site_parser
import time

def main():
    # parser = site_parser.Ati_truck_parser()
    #
    # parser.make_new_query(city_from="Амстердам",
    #                       city_to="Москва",
    #                       weight_t=None,
    #                       volume_m3=None,
    #                       cargo_type=None
    #                       )
    # # parser.make_new_query()
    # time.sleep(1)
    # parser.load_next_page()
    # time.sleep(5)
    # del parser

    # Example of AtiCargoParser usage
    parser = site_parser.AtiCargoParser(delay_time=5)  # create an object
    num_listings = parser.make_new_query(city_from="Москва", city_to="Нижний Новгород", max_weight=10)  # make a query
    if num_listings > 0:  # if there are listings matching the query, get the data
        print(parser.get_listing_data())  # get data from current page
        if parser.load_next_page():  # load next page
            print(parser.get_listing_data())  # get data from the next page
        # and so on and so forth...
        if parser.load_next_page():
            print(parser.get_listing_data())
        if parser.load_next_page():
            print(parser.get_listing_data())
        # time.sleep(5)
    del parser


if __name__ == '__main__':
    main()



