# Importing all needed libraries
from selenium import webdriver
import time
import pandas as pd

import json
from lxml import html
import re
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)

import ssl

import pandas as pd

WAIT_TIME = 10
WAIT_TIME_2 = 5
WAIT_TIME_3 = 3
WAIT_TIME_4 = 0.5
WAIT_TIME_5 = 1

chromedriver_path = 'C:/Users/user/Desktop/script_scraper/chromedriver'
ssl._create_default_https_context = ssl._create_unverified_context
PASSWORD = 'Francisco01'
USERNAME = 'yuwouddaummeukeu-1608@yopmail.com'


def load_instagram():
    """
    Function to initialize Instagram and launch it in a browser using Selenium
    """
    executable_path = chromedriver_path

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-notifications')
    options.add_argument("--disable-gpu")

    preferences = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.location": 2,
        # We don't need images, only the URLs.
        "profile.managed_default_content_settings.images": 2,
    }
    options.add_experimental_option("prefs", preferences)

    browser = webdriver.Chrome(
        executable_path=executable_path,
        # chrome_options=options,
    )
    browser.wait = WebDriverWait(browser, WAIT_TIME)

    # Opening the browser and getting the url

    url = "https://www.instagram.com/"
    browser.get(url)

    # wait 5 seconds to load
    time.sleep(WAIT_TIME_2)

    # Accept cookies

    return browser


def searchAndClick(keyword, browser):
    time.sleep(WAIT_TIME_2)
    searchbox1 = browser.find_element(
        "css selector", "svg[aria-label='Búsqueda']").click()
    time.sleep(WAIT_TIME_2)
    searchbox = browser.find_element(
        "css selector", "input[placeholder='Busca']")
    searchbox.send_keys(keyword)
    time.sleep(WAIT_TIME_3)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(WAIT_TIME_3)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(WAIT_TIME_3)

    scrolldown = browser.execute_script('window.scrollBy(0, 500);')
    time.sleep(WAIT_TIME_5)

    posts = []
    links = browser.find_elements("tag name", "a")
    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            posts.append(post)

    time.sleep(4)
    data_dict = {}
    # datetime_list = []
    # coments_list = []
    # usernames_list = []

    for post in posts:
        browser.get(post)
        time.sleep(10)

        usernames_list = []
        datetime_list = []
        coments_list = []

        # Div_user = browser.find_elements("class name", "_a9zr")
        divs = browser.find_elements(
            By.XPATH, '//div[contains(@class,"_a9zr")]')
        try:
            for div in divs:
                usernames = div.find_elements(By.XPATH, './/h3')
                usernames = [element.text for element in usernames]
                usernames_list.extend(usernames)
        except:
            print('No se encontraron usernames en este post')

        # Buscar datetime
        try:
            for div in divs:
                elements = div.find_elements(By.XPATH, './/time')
                elements = [element.get_attribute(
                    'datetime') for element in elements]
                datetime_list.extend(elements)
        except:
            print('No se encontraron datetimes en este post')

        # Buscar comentarios
        try:
            for div in divs:
                coments = div.find_elements(By.XPATH, './/span')
                coments = [element.text for element in coments]
                coments_list.extend(coments)
        except:
            print('No se encontraron comentarios en este post')

        for username, datetime, comment in zip(usernames_list, datetime_list, coments_list):
            if username not in data_dict:
                data_dict[username] = []

            data_dict[username].append(
                {'datetime': datetime, 'comment': comment, 'Origen': "instagran", "url": post})

    time.sleep(WAIT_TIME_5)
    return data_dict


def instagram_login(driver):
    time.sleep(WAIT_TIME_3)
    username = driver.find_element("css selector", "input[name='username']")
    password = driver.find_element("css selector", "input[name='password']")
    username.clear()
    password.clear()
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    login = driver.find_element(
        "css selector", "button[type='submit']").click()
    time.sleep(4)
    nothow = driver.find_element(
        "xpath", "//button[contains(text(), 'Ahora no')]").click()
    # turn on notif
    time.sleep(4)
    nothow2 = driver.find_element(
        "xpath", "//button[contains(text(), 'Ahora no')]").click()


p = load_instagram()
instagram_login(p)
valor = searchAndClick("somosgamave", p)
df = pd.DataFrame.from_dict(valor, orient='index')
# df = pd.DataFrame(valor)
# df.head()
