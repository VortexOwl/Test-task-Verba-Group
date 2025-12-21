# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
import json
#from json import dump, load, loads
import random
#from random import randint
import time
#from time import sleep
from os.path import isfile

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.logs import log_info, log_debug, log_error
from src.utilities.utilities import creating_necessary_folders

# ----------------------------------------------------------------------------#
# External libraries                                                          #
# ----------------------------------------------------------------------------#
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(level=20)


def webdriver_create() -> None:
    global driver_browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("detach", True)
    options.add_argument("--headless")
    service = webdriver.ChromeService(executable_path="data/chromedriver/chromedriver.exe")
    driver_browser = webdriver.Chrome(options=options, service=service)

    stealth(driver_browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )


def timeout_web_request(beginning:int=10, end:int=30) -> None:
    time.sleep(random.randint(beginning, end))


def write_cookies() -> None:
    cookies = driver_browser.get_cookies()
    creating_necessary_folders(path='data')
    with open(file=f'data/cookies.json', mode='w') as file:
        json.dump(ocookies, file)


def read_cookies() -> None:
    creating_necessary_folders(path='data')
    if isfile(path='data/cookies.json'):
        with open(file='data/cookies.json', mode='r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                driver_browser.add_cookie(cookie_dict=cookie)
    else:
        write_cookies()
        read_cookies()


def wait_find_element(driver:webdriver, by:By, value:str, timeout:int=60) -> WebDriverWait:
    return WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_element_located((by, value)))
    

def wait_find_elements(driver:webdriver, by:By, value:str, timeout:int=60) -> WebDriverWait:
    return WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_all_elements_located((by, value)))


def get_json_products_page(text_request:str, number_page:str) -> dict:
    xhr_url = f'https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false' \
        "&ab_testing=false" \
        "&appType=1" \
        "&curr=rub" \
        "&dest=12358062" \
        "&hide_dtype=9;11" \
        "&hide_vflags=4294967296" \
        "&inheritFilters=false" \
        "&lang=ru" \
        f"&page={number_page}" \
        f"&query={text_request}" \
        "&resultset=catalog" \
        "&sort=popular" \
        "&spp=30" \
        "&suppressSpellcheck=false"
    log_debug(message=f'Product map page {number_page} XHR URL: {xhr_url}')
    driver_browser.get(url=xhr_url)
    timeout_web_request()
    str_response_json = wait_find_element(driver=driver_browser, by=By.XPATH, value=".//pre").get_attribute('textContent')
    response_json = json.loads(str_response_json)
    return response_json


def get_json_product_page(product_id:str) -> dict:
    random_number = random.randint(1, 4)
    xhr_url = f"https://rst-basket-cdn-0{random_number}bl.geobasket.ru/vol{product_id[:-5]}/part{product_id[:-3]}/{product_id}/info/ru/card.json" 
    log_debug(message=f'Page ID {product_id} XHR URL: {xhr_url}')
    driver_browser.get(url=xhr_url)
    timeout_web_request()
    str_response_json = wait_find_element(driver=driver_browser, by=By.XPATH, value=".//pre").get_attribute('textContent')
    response_json = json.loads(str_response_json)
    return response_json


def get_images(product_id:str) -> str:
    url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"
    log_debug(message=f'Page ID {product_id} URL: {url}')
    driver_browser.get(url=url)
    timeout_web_request()
    list_images = list()
    swipers = driver_browser.find_elements(by=By.XPATH, value=".//div[@class='swiper-wrapper']")
    for swiper in swipers:
        elements = swiper.find_elements(by=By.XPATH, value=".//img[starts-with(@alt, 'Product image')]")
        for element in elements:
            list_images.append(element.get_attribute('src'))
    str_images = ""
    count_images = len(list_images)
    for number in range(count_images):
        if number == count_images - 1:
            str_images += list_images[number]
        else:
            str_images += list_images[number] + ', '
    return str_images


def check_dict_is_key(check_dict:dict, check_key:str):
    if check_key in check_dict:
        return check_dict[check_key]
    return ""


def get_products_page(json_products_page:dict, list_products: list) -> list:
    if json_products_page:
        for response_product in json_products_page['products']:
            dict_product = dict()
            dict_product['link'] = f"https://www.wildberries.ru/catalog/{response_product['id']}/detail.aspx"
            dict_product['article'] = str(response_product['id'])
            dict_product['name'] = response_product['name']
            dict_product['fullPrice'] = response_product['sizes'][0]['price']['basic']
            dict_product['discountedPrice'] = response_product['sizes'][0]['price']['product']
            dict_product['nameSeller'] = response_product['supplier']
            dict_product['linkSeller'] = f"https://www.wildberries.ru/seller/{response_product['supplierId']}"
            list_product_sizes = list()
            for response_product_size in response_product['sizes']:
                dict_product_size = dict()
                dict_product_size['name'] = response_product_size['name']
                dict_product_size['fullPrice'] = response_product_size['price']['basic']
                dict_product_size['discountedPrice'] = response_product_size['price']['product']
                list_product_sizes.append(dict_product_size)
            dict_product['productSizes'] = list_product_sizes
            dict_product['productBalances'] = response_product['totalQuantity']
            dict_product['reviewRating'] = response_product['reviewRating']
            if response_product['feedbacks'] == None:
                dict_product['quantityFeedbacks'] = 0
            else:
                dict_product['quantityFeedbacks'] = int(response_product['feedbacks'])
            json_product_page = get_json_product_page(product_id=dict_product['article'])
            dict_product['description'] = check_dict_is_key(check_dict=json_product_page, check_key='description')
            dict_product['images'] = get_images(product_id=dict_product['article'])
            list_product_characteristics = list()
            response_product_options = check_dict_is_key(check_dict=json_product_page, check_key='options')
            for json_product_page_option in response_product_options:
                dict_product_characteristic = dict()
                dict_product_characteristic[json_product_page_option['name']] = json_product_page_option['value']
                list_product_characteristics.append(dict_product_characteristic)
            dict_product['characteristics'] = list_product_characteristics
            list_products.append(dict_product)
    return list_products


def is_go_next_page() -> bool:
    try:
        wait_find_element(driver=driver_browser, by=By.XPATH, value="//div[starts-with(@class, 'not-found')]", timeout=20)
        is_next_page = False
    except Exception as e:
        log_debug(f"Тип ошибки WebDriverWait: {type(e)}")
        is_next_page = True
    finally:
        return is_next_page


def go_product_card_page(text_request:str, number_page:str='1') -> bool:
    if number_page == '1':
        url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={text_request}"
    else:
        url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={text_request}&page={number_page}"    
    log_debug(message=f'Product map page {number_page} URL: {url}')
    driver_browser.get(url=url)
    read_cookies()
    timeout_web_request()
    is_next_page = is_go_next_page()
    return is_next_page


def page_filter_no_text(number_page:str) -> dict:
    price_start = 1
    price_finish = 10000
    flag_rating = 'frating=1'
    code_RF = 'f14177451=15000203'
    xhr_url = "https://www.wildberries.ru/__internal/u-recom/personal/ru/common/v8/search?ab_pers_testid=fn_ex" \
        "&ab_rec_testid=fn_ex" \
        "&ab_rel_testid=fn_ex" \
        "&ab_testing=false" \
        "&ab_vis_testid=fn_ex" \
        "&curr=rub&dest=12358062" \
        f"&lang=ru&page={number_page}" \
        "&query=0&resultset=catalog" \
        "&suppressSpellcheck=false" \
        f"&{flag_rating}" \
        f"&priceU={price_start}00%3B{price_finish}00" \
        f"&{code_RF}"
    driver_browser.get(url=xhr_url)
    timeout_web_request()
    str_response_json = wait_find_element(driver=driver_browser, by=By.XPATH, value=".//pre").get_attribute('textContent')
    response_json = json.loads(str_response_json)
    return response_json


def start_web_quest_1(text_request:str='пальто из натуральной шерсти') -> list:
    log_info(message='Запуск вебдрайвера.')
    webdriver_create()
    number_page = 1
    list_products = list()
    is_next_page = go_product_card_page(text_request=text_request, number_page=number_page)
    while is_next_page:
        json_products_page = get_json_products_page(text_request=text_request, number_page=str(number_page))
        list_products = get_products_page(json_products_page=json_products_page, list_products=list_products)
        if number_page == 3:
            break
        number_page += 1
        is_next_page = go_product_card_page(text_request=text_request, number_page=str(number_page))
    log_info(message='Выключение вебдрайвера.')
    driver_browser.quit()
    return list_products


def start_web_quest_2() -> list:
    log_info(message='Запуск вебдрайвера.')
    webdriver_create()
    number_page = 1
    list_products = list()
    while True:
        json_products_page = page_filter_no_text(number_page=str(number_page))
        if not json_products_page:
            break
        if not 'products' in json_products_page:
            break
        if not json_products_page['products']:
            break
        list_products = get_products_page(json_products_page=json_products_page, list_products=list_products)
        if number_page == 3:
            break
        number_page += 1
    log_info(message='Выключение вебдрайвера.')
    driver_browser.quit()
    return list_products
    

def start_web(quest_number:int=1, text_request:str='пальто из натуральной шерсти') -> list:
    if quest_number == 1:
        list_products = start_web_quest_1(text_request=text_request)
    elif quest_number == 2:
        list_products = start_web_quest_2()
    return list_products
