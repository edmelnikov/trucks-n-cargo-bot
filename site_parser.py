from bs4 import BeautifulSoup
import requests
import urllib.request
from selenium import webdriver
import time
import re
from lxml import etree


# ati.su listings parser (WIP) #
# Abstract parser class #
class Ati_parser():

    def __init__(self, url):
        self.driver = webdriver.Chrome()  # create Chrome browser driver
        self.driver.get(url)

    # Methods shared across all child classes #
    def authorize(self):  # authorization via login and password
        pass

    def fill_city_field(self, field_path, city, dropdown_path):  # enter city to specified text field
        self.driver.find_element_by_xpath(field_path).send_keys(city)  # fill up departure city
        self.driver.find_element_by_xpath(field_path).click()  # click to open up a dropdown list with suggested cities
        time.sleep(1)  # wait for a dropdown list to load
        self.driver.find_element_by_xpath(dropdown_path).click()  # click the first city in the dropdown

    # Virtual methods #
    def make_new_query(self):
        pass

    def get_listing_data(self):
        pass

    def load_next_page(self):
        pass

    # Quit the driver once the object is deleted #
    def __del__(self):
        self.driver.quit()


# WIP, on hold #
class Ati_truck_parser(Ati_parser):
    domain = 'https://trucks.ati.su/'

    search_button_path = '//*[@id="root"]/div/div[1]/main/div[4]/div[2]/div[2]/button'  # "search" button path
    from_input_path = '//*[@id="root"]/div/div[1]/main/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/div/label/div/input' # departure point field path
    to_input_path = '//*[@id="root"]/div/div[1]/main/div[3]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div/label/div/input'  # destinationn point field path
    weight_input_path = '//*[@id="root"]/div/div[1]/main/div[3]/div/div[1]/div[4]/div[2]/div/div[1]/label/input'  # lowest load capacity field path
    volume_input_path = '//*[@id="root"]/div/div[1]/main/div[3]/div/div[1]/div[5]/div[2]/div/div[1]/label/input'  # lowest volume field path
    next_page_button_path = '//*[@id="root"]/div/div[1]/main/div[5]/div/div[5]/div[1]/div/span[last()]'
    dropdown_first_path = '//*[@id="react-autowhatever-from--item-0"]'  # path of a first item in a dropdown list



    # Create Chrome driver open up the website #
    def __init__(self, sleep_time=2):
        super().__init__(self.domain)  # start chrome driver and open the website

        self.sleep_time=sleep_time  # waiting time to let the site fully load (may be removed later)

        # query parameters
        self.city_from = None  # departure city
        self.city_to = None  # destination city
        self.weight_t = None  # weight of cargo in tonnes
        self.volume_m3 = None  # volume of cargo in m3
        self.cargo_type = None  # cargo type? (WIP)

        # query results data
        self.total_listings_num = 0  # total number of listings found by a query
        self.total_pages_num = 0  # total number of avaliable pages of listings
        self.curr_page_num = 0  # current page number (unused)

    # Make a new query satisfying the function parameters #
    # Also record the total number of found listings and number of avaliable pages with listings #
    # Returns a number avaliable listings obtained by the query #
    def make_new_query(self, city_from=None, city_to=None, weight_t=None, volume_m3=None, cargo_type=None):
        # TODO:
        # 1. Add some kind of wrong spelling handling
        # 2. Implement a smarter way to wait until a page loads
        # 3. Fix load_next_page() method

        self.city_from = city_from
        self.city_to = city_to
        self.weight_t = weight_t
        self.volume_m3 = volume_m3
        self.cargo_type = cargo_type

        self.curr_page_num = 0

        # set departure city
        if city_from is not None:
            self.fill_city_field(self.from_input_path, self.city_from, self.dropdown_first_path)

        # set destination city
        if city_to is not None:
            self.fill_city_field(self.to_input_path, self.city_to, self.dropdown_first_path)

        # set load capacity lower bound
        if self.weight_t is not None:
            self.driver.find_element_by_xpath(self.weight_input_path).send_keys(self.weight_t)

        # set volume lower bound
        if self.volume_m3 is not None:
            self.driver.find_element_by_xpath(self.volume_input_path).send_keys(self.volume_m3)

        # search for listings
        self.driver.find_element_by_xpath(self.search_button_path).click() # click "search" button
        time.sleep(self.sleep_time)  # sleep to let the page fully load

        # parse the page with listings and find the total number of available listings
        soup = BeautifulSoup(self.driver.page_source, "html.parser")  # get page source with all listings
        total_listing_num_div = soup.find('div', {'data-qa': 'total-trucks-count'})  # div containing total number of listings
        if total_listing_num_div is None:  # if no trucks have been found
            self.total_listings_num = 0
            # self.total_pages_num = 0
        else:
            self.total_listings_num = int(re.findall(r'\d+', total_listing_num_div.getText())[0])

        return self.total_listings_num


    # Get listing data in form of a dictionary from current page #
    def get_listing_data(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        listing_divs = soup.find_all('div', {'class': 'sc-gIDmLj hbTsnE card'})  # find divs containing listings
        print(listing_divs)


    # Load next page, if it exists #
    # (WIP, Element ... is not clickable at point ... error) #
    def load_next_page(self):
        print(self.driver.page_source)
        self.driver.find_element_by_xpath(self.next_page_button_path).click()


class Ati_cargo_parser(Ati_parser):
    domain='https://loads.ati.su/'

    search_button_path = '//*[@id="search-scroll-anchor"]/div[2]/div[2]/button'  # "search" button path
    from_input_path = '//*[@id="__next"]/div/main/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/div/div/div/label/div[1]/input'  # departure point field path
    to_input_path = '//*[@id="__next"]/div/main/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/label/div[1]/input'
    dropdown_first_path = '//*[@id="react-autowhatever-1--item-0"]'  # path of a first item in a dropdown list

    def __init__(self):
        super().__init__(self.domain)  # start chrome driver and open the website

        self.city_from = None  # departure city
        self.city_to = None  # destination city

        self.total_listings_num = 0

    def make_new_query(self, city_from=None, city_to=None, date_from=None, date_range=None,
                       max_weight_t=None, weight_range=None, volume_m3=None):

        self.city_from = city_from
        self.city_to = city_to
        #self.weight_t = weight_t
        #self.volume_m3 = volume_m3

        self.total_listings_num = 0

        # set departure city
        if city_from is not None:
            self.fill_city_field(self.from_input_path, self.city_from, self.dropdown_first_path)

        # set destination city
        if city_to is not None:
            self.fill_city_field(self.to_input_path, self.city_to, self.dropdown_first_path)

        # search for listings
        self.driver.find_element_by_xpath(self.search_button_path).click()  # click "search" button
        time.sleep(2)  # sleep to let the page fully load

        # parse the page with listings and find the total number of available listings
        soup = BeautifulSoup(self.driver.page_source, "html.parser")  # get page source with all listings

        total_listing_num_div = soup.find('div', {'class': 'SearchResults_searchStatus__n103h'})  # div containing total number of listings
        if total_listing_num_div is not None:
            listing_num_str = total_listing_num_div.find('h2', {'class': 'glz-h glz-is-size-2'}).getText()
            self.total_listings_num = int(re.findall(r'\d+', listing_num_str)[0])
        else:
            self.total_listings_num = 0
        return self.total_listings_num


    # Get listing data in form of a dictionary from current page #
    # this code ignores tenders! #
    def get_listing_data(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        listing_divs = soup.find_all('div', {'class': '_39xB9'})  # find divs containing listings

        listing_datum = {
            'from_city': None,
            'to_city': None,
            'dates': None,
            'weight': None,
            'volume': None,
            'transport_type': None,
            'link': None,
        }

        listing_data = []
        if len(listing_divs) != 0:
            for listing_div in listing_divs:
                departure_data_div = listing_div.find('div', {'class': '_3TPf3 huFkH'})  # div (column) containing departure city data
                listing_datum['from_city'] = departure_data_div.find('div', {'class': '_15Q0N HptCF'}).getText(separator=' ')
                listing_datum['dates'] = departure_data_div.find('span', {'class': '_35iFG _1V6yy'}).getText(separator=' ')

                destination_data_div = listing_div.find('div', {'class': '_3TPf3 _3tY-M'})  # div (column) containing destination city data
                listing_datum['to_city'] = destination_data_div.find('div', {'class': '_15Q0N HptCF'}).getText(separator=' ')

                cargo_data_div = listing_div.find('div', {'class': '_3TPf3 _2gLPf'})  # div (column) containing cargo data
                weight_volume = cargo_data_div.find('div', {'class': '_3lW-N'}).getText(separator=' ').split(" / ")
                listing_datum['weight'] = weight_volume[0]
                listing_datum['volume'] = weight_volume[1]

                transport_data_div = listing_div.find('div', {'class': '_3TPf3 _1EqYq'})  # div (column) transport data
                listing_datum['transport_type'] = transport_data_div.find('span', {'class': 'glz-tooltiptext'}).getText(separator=' ')

                listing_data.append(listing_datum)
        print(listing_data)
        return listing_data

    # Load next page, if it exists #
    # #
    def load_next_page(self):
        pass

# avito.ru listings parser #
# def search_by_query_avito(query, city, num_listings=10):
#     domain = "https://www.avito.ru"
#     soup = BeautifulSoup(requests.get(f"{domain}/{city}?q={query}", verify=False).text, "lxml")  # soup of a page with listings
#     listing_preview = soup.find_all("div", {"data-marker": "item"})  # previews of listings
#     data = []
#     for i in range(num_listings):
#         if i >= len(listing_preview):
#             break
#         else:
#             title = listing_preview[i].find("a", {"data-marker": "item-title"}).find("h3").getText(' ')  # title of a listing
#             price = listing_preview[i].find("span",
#                                             {"class": "price-text-_YGDY text-text-LurtD text-size-s-BxGpL"}).getText()
#             rel_link = listing_preview[i].find("a", {"data-marker": "item-title"})['href']  # relative link of a listing
#             abs_link = f"{domain}{rel_link}"
#             description = listing_preview[i].find("div", {"class": "iva-item-descriptionStep-C0ty1"}).getText(' ')
#             img_link = listing_preview[i].find("img", {"class": "photo-slider-image-YqMGj"})['src']
#             data.append({"title": title, "price": price, "link": abs_link, "description": description, "img_link": img_link})
#
#     return data

