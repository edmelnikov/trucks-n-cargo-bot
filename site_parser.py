from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import re
from lxml import etree

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException


# ati.su listings parser (WIP) #
# Abstract parser class #
class AtiParser:
    delay_time = 5

    def __init__(self, url, delay_time):
        self.delay_time = delay_time
        self.driver = webdriver.Chrome()  # create Chrome browser driver
        self.driver.get(url)

    # Methods shared across all child classes #
    def authorize(self):  # authorization via login and password
        pass

    def fill_city_field(self, field_path, city, dropdown_path):  # enter city to specified text field
        # self.driver.find_element(By.XPATH, field_path).send_keys(city)
        # self.driver.find_element(By.XPATH, field_path).click()

        # wait and check if the fields are present
        try:
            presence_of_elem = EC.presence_of_element_located((By.XPATH, field_path))
            WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).send_keys(city)  # fill up departure city

            presence_of_elem = EC.presence_of_element_located((By.XPATH, field_path))
            WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).click()  # click to open up a dropdown list with suggested cities

        except TimeoutException:
            print("City input fields were not found!")

        # wait and check if the dropdown is present
        try:
            presence_of_elem = EC.presence_of_element_located((By.XPATH, dropdown_path))
            WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).click()  # click the first city in the dropdown
        except TimeoutException:
            print("City dropdown was not found!")

    def load_next(self, next_page_button_path):
        try:
            presence_of_elem = EC.presence_of_element_located((By.XPATH, next_page_button_path))
            WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).click()  # click "next page" button
            time.sleep(self.delay_time)  # a small delay to let the page update (temporary solution, has to be changed later)
            return True
        except TimeoutException:
            print("Next page button was not found!")
            return False
        except ElementNotInteractableException:  # last page and the next page button is not clickable
            return False

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
class AtiTruckParser(AtiParser):
    domain = 'https://trucks.ati.su/'

    search_button_path = '//*[@id="root"]/div/div[1]/main/div[4]/div[2]/div[2]/button'  # "search" button path
    from_input_path = '//*[@id="root"]/div/div[1]/main/div[3]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/div/label/div/input' # departure point field path
    to_input_path = '//*[@id="root"]/div/div[1]/main/div[3]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div/label/div/input'  # destinationn point field path
    weight_input_path = '//*[@id="root"]/div/div[1]/main/div[3]/div/div[1]/div[4]/div[2]/div/div[1]/label/input'  # lowest load capacity field path
    volume_input_path = '//*[@id="root"]/div/div[1]/main/div[3]/div/div[1]/div[5]/div[2]/div/div[1]/label/input'  # lowest volume field path
    next_page_button_path = '//*[@id="root"]/div/div[1]/main/div[5]/div/div[5]/div[1]/div/span[last()]'
    dropdown_from_first_path = '//*[@id="react-autowhatever-from--item-0"]'  # path of a first item in a dropdown list
    dropdown_to_first_path = '//*[@id="react-autowhatever-to--item-0"]'

    # Create Chrome driver open up the website #
    def __init__(self, delay_time=5):
        super().__init__(self.domain, delay_time=delay_time)  # start chrome driver and open the website

        # query parameters
        self.city_from = None  # departure city
        self.city_to = None  # destination city
        self.weight = None  # weight of cargo in tonnes
        self.volume = None  # volume of cargo in m3
        self.cargo_type = None  # cargo type? (WIP)

        # query results data
        self.total_listings_num = 0  # total number of listings found by a query

    # Make a new query satisfying the function parameters #
    # Also record the total number of found listings and number of avaliable pages with listings #
    # Returns a number of available listings obtained by the query #
    def make_new_query(self, city_from=None, city_to=None, weight=None, volume=None, cargo_type=None):

        self.city_from = city_from
        self.city_to = city_to
        self.weight = weight
        self.volume = volume
        self.cargo_type = cargo_type

        # set departure city
        if city_from is not None:
            self.fill_city_field(self.from_input_path, self.city_from, self.dropdown_from_first_path)

        # set destination city
        if city_to is not None:
            self.fill_city_field(self.to_input_path, self.city_to, self.dropdown_to_first_path)

        # set weight (I know that I violate the DRY principle here, but who cares)
        if self.weight is not None:
            try:
                presence_of_elem = EC.presence_of_element_located((By.XPATH, self.weight_input_path))
                WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).send_keys(self.weight)
            except TimeoutException:
                print("Weight fields were not found!")

        # set volume
        if self.volume is not None:
            try:
                presence_of_elem = EC.presence_of_element_located((By.XPATH, self.volume_input_path))
                WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).send_keys(self.volume)
            except TimeoutException:
                print("Volume fields were not found!")

        # click search button
        try:
            presence_of_elem = EC.presence_of_element_located((By.XPATH, self.search_button_path))
            WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).click()  # fill up departure city
        except TimeoutException:
            print("Search button was not found!")
            return 0  # we can't progress any further, return 0 meaning that no listings were found

        # wait until the listings load
        time.sleep(self.delay_time)
        try:
            presence_of_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/main/div[5]/div/div[4]'))
            WebDriverWait(self.driver, self.delay_time).until(presence_of_elem)
        except TimeoutException:
            print("Either no listings were found, or the page hasn't loaded")

        # parse the page with listings and find the total number of available listings
        soup = BeautifulSoup(self.driver.page_source, "html.parser")  # get page source with all listings
        total_listing_num_div = soup.find('div', {'data-qa': 'total-trucks-count'})  # div containing total number of listings
        if total_listing_num_div is None:  # if no trucks have been found
            self.total_listings_num = 0
            # self.total_pages_num = 0
        else:

            self.total_listings_num = re.findall(r'\d+', total_listing_num_div.getText().replace(" ", ""))
            self.total_listings_num = int(''.join(self.total_listings_num))  # in case there is a space between digits

        return self.total_listings_num

    # Get listing data in form of a dictionary from current page #
    def get_listing_data(self):
        # ISSUES:
        # \u characters

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        listing_divs = soup.find_all('div', {'class': 'sc-gIDmLj hbTsnE card'})  # find divs containing listings

        listing_datum = {
            'from_city': None,
            'to_city': None,
            'dates': None,
            'weight': None,
            'volume': None,
            'transport_type': None,
            'truck_info': None,
            'link': None,
        }

        listing_data = []
        if len(listing_divs) != 0:
            for listing_div in listing_divs:
                # Departure city
                try:
                    listing_datum['from_city'] = listing_div.find('p', {'data-qa': 'loading-city'}).getText(
                        separator=' ')
                except AttributeError:
                    print("Departure city name was not found")

                # dates
                try:
                    listing_datum['dates'] = listing_div.find('p', {'data-qa': 'loading-periodicity'}).getText(separator='').replace("\u2009", " ")
                except AttributeError:
                    print("Dates were not found")

                # destination city
                try:
                    listing_datum['to_city'] = listing_div.find('p', {'data-qa': 'main-unloading-point-name'}).getText(separator='').replace("\u2009", " ")
                except AttributeError:
                    print("Destination city name was not found")

                # weight
                try:
                    listing_datum['weight'] = listing_div.find('span', {'data-qa': 'truck-weight'}).getText(separator='').replace("\u2009", " ")
                except AttributeError:
                    print("Weight was not found")

                # volume
                try:
                    listing_datum['volume'] = listing_div.find('span', {'data-qa': 'truck-volume'}).getText(separator='').replace("\u2009", " ")
                except AttributeError:
                    print("Volume was not found")

                # general info
                try:
                    listing_datum['truck_info'] = listing_div.find('p', {'data-qa': 'truck-info'}).getText(separator='').replace("\u2009", " ")
                except AttributeError:
                    print("Truck info was not found")

                listing_data.append(listing_datum)
        return listing_data

    def load_next_page(self):
        return self.load_next(self.next_page_button_path)


class AtiCargoParser(AtiParser):
    domain = 'https://loads.ati.su/'
    search_button_path = '//*[@id="search-scroll-anchor"]/div[2]/div[2]/button'  # "search" button path
    from_input_path = '//*[@id="__next"]/div/main/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/div/div/div/label/div[1]/input'  # departure point field path
    to_input_path = '//*[@id="__next"]/div/main/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/label/div[1]/input'
    dropdown_first_path = '//*[@id="react-autowhatever-1--item-0"]'  # path of a first item in a dropdown list
    min_weight_path = '//*[@id="__next"]/div/main/div[1]/div/div[3]/div[2]/div[3]/div/div/div[1]/label/input'
    max_weight_path = '//*[@id="__next"]/div/main/div[1]/div/div[3]/div[2]/div[3]/div/div/div[2]/label/input'
    max_volume_path = '//*[@id="__next"]/div/main/div[1]/div/div[3]/div[2]/div[4]/div/div/div[2]/label/input'
    next_page_button_path = '//*[@id="__next"]/div/main/div[1]/div/div[7]/div/span[last()]'

    def __init__(self, delay_time):
        super().__init__(self.domain, delay_time=5)  # start chrome driver and open the website

        self.city_from = None  # departure city
        self.city_to = None  # destination city
        self.date_from = None  # starting weight
        self.date_range = None
        self.max_weight = None  # max load capacity in tonnes
        self.weight_range = None  # load capacity range in tonnes
        self.volume = None  # body capacity in m3
        self.total_listings_num = 0

    # Form and make a new query #
    # Returns a number of matching listings #
    # Returns zero if either no listings have been found, or other problem has occurred #
    def make_new_query(self, city_from=None, city_to=None, date_from=None, date_range=None,
                       max_weight=None, weight_range=None, volume=None):

        self.city_from = city_from
        self.city_to = city_to
        self.date_from = date_from
        self.date_range = date_range
        self.max_weight = max_weight
        self.weight_range = weight_range
        self.volume = volume

        self.total_listings_num = 0

        # set departure city
        if city_from is not None:
            self.fill_city_field(self.from_input_path, self.city_from, self.dropdown_first_path)

        # set destination city
        if city_to is not None:
            self.fill_city_field(self.to_input_path, self.city_to, self.dropdown_first_path)

        # set dates
        pass

        # set weight (I know that I violate the DRY principle here, but who cares)
        if type(self.weight_range) is tuple and len(self.weight_range) == 2:
            try:
                presence_of_elem = EC.presence_of_element_located((By.XPATH, self.min_weight_path))
                WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).send_keys(self.weight_range[0])

                presence_of_elem = EC.presence_of_element_located((By.XPATH, self.max_weight_path))
                WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).send_keys(self.weight_range[1])
            except TimeoutException:
                print("Weight fields were not found!")
        elif self.max_weight is not None:
            try:
                presence_of_elem = EC.presence_of_element_located((By.XPATH, self.max_weight_path))
                WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).send_keys(self.max_weight)
            except TimeoutException:
                print("Weight fields were not found!")

        # set volume
        if self.volume is not None:
            try:
                presence_of_elem = EC.presence_of_element_located((By.XPATH, self.max_volume_path))
                WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).send_keys(self.volume)
            except TimeoutException:
                print("Volume fields were not found!")

        # click search button
        try:
            presence_of_elem = EC.presence_of_element_located((By.XPATH, self.search_button_path))
            WebDriverWait(self.driver, self.delay_time).until(presence_of_elem).click()  # fill up departure city
        except TimeoutException:
            print("Search button was not found!")
            return 0  # we can't progress any further, return 0 meaning that no listings were found

        time.sleep(5)  # let the page with the results load
        # parse the page with listings and find the total number of available listings
        soup = BeautifulSoup(self.driver.page_source, "html.parser")  # get page source with all listings
        total_listing_num_div = soup.find('div', {'class': 'SearchResults_searchStatus__n103h'})  # div containing total number of listings
        if total_listing_num_div is not None:
            listing_num_str = total_listing_num_div.find('h2', {'class': 'glz-h glz-is-size-2'}).getText()  # unsafe, may cause problems
            self.total_listings_num = int(re.findall(r'\d+', listing_num_str)[0])
        else:
            self.total_listings_num = 0
        return self.total_listings_num

    # Get listing data in form of a dictionary from current page #
    # This code ignores "tenders"! #
    # Returns a list of dictionaries for each listing on current page #
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
        return listing_data

    # Load next page, if it exists #
    # Returns True if the next page has been successfully loaded #
    # Returns False otherwise #
    def load_next_page(self):
        return self.load_next(self.next_page_button_path)


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

