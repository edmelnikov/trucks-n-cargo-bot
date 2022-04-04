# bs4, selenium, requests
import site_parser


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

    parser = site_parser.Ati_cargo_parser()
    parser.make_new_query(city_from="Москва", city_to="Нижний Новгород")

    parser.get_listing_data()
    # parser.get_listing_data()

    del parser


if __name__ == '__main__':
    main()



