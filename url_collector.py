from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
from typing import Literal, List, Generator
from itertools import chain
from tabela import UrlsBase
from config import get_engine
from sqlalchemy import insert



def insert_urls_google(*args, **kwargs):
    engine = get_engine()
    with engine.connect() as conn:
        try:
            result = conn.execute(
                insert(UrlsBase),
                [
                    {"loja": kwargs.get('loja'),
                     "urlanuncio": str(kwargs.get('urlanuncio'))
                        , "referencia":str(kwargs.get('referencia'))
                        }
                ]
            )
        except Exception as e:
            print("error", e)


options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"C:\\Users\\Guilherme\\Documents\\ecommercefllaskapp\\collectgoogle\\chromedriver\\chromedriver.exe")

def search_products() -> None:
    lista_dicts: list = []
    driver.implicitly_wait(3)
    data = pd.read_csv(r"C:\\Users\\Guilherme\\Documents\\ecommercefllaskapp\\collectgoogle\\excelfiles\\eans\\eans_base.csv",sep=";",encoding='latin-1')
    data['EAN'] = data['EAN'].astype(str)
    data['EAN'] = data['EAN'].apply(lambda k: str(k).split(".0")[0])
    dicts = data.to_dict('records')
    for dic in dicts:
        time.sleep(3)
        driver.get(r'https://shopping.google.com.br')

        time.sleep(3)
        try:
            search = driver.find_element(By.XPATH,'//*[@id="REsRA"]')
            search.clear()
            search.send_keys(str(dic['EAN']))
        except:
            print("erro busca ean")
        try:
            busca = driver.find_element(By.XPATH,'//*[@id="kO001e"]/div/div/c-wiz/form/div[2]/div[1]/button/div/span').click()
        except:
            print("erro busca")
        time.sleep(1)
        try:
            google_url = driver.find_elements(By.XPATH,'//*[@id="rso"]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div/a')
            urlgoogle = [url.get_dom_attribute('href') for url in google_url]
            if len(urlgoogle) <= 10:
                google_url = driver.find_elements(By.XPATH, '//*[@id="rso"]/div/div[2]/div/div/div[1]/div[2]/span/a')
                urlgoogle = [url.get_dom_attribute('href') for url in google_url]
        except:
            print("valor invalido")

        if next(map(lambda k: k if len(k) >=200 else(k if type(k) == str else 'valorinvalido'),urlgoogle),None):

            dict_item: dict = {}
            if urlgoogle !='valorinvalido' or urlgoogle != None:
                dict_item['URLGOOGLE'] = str('https://www.google.com/') + str(next(chain(urlgoogle)))
                dict_item['EAN'] = str(dic['EAN'])
                dict_item['NOMEPRODUTO'] = str(dic['NomeProduto'])
                dict_item['Marca'] = dic['Marca']
                dict_item['SKU'] = str(dic['SKU'])
                lista_dicts.append(dict_item)
                print(dict_item)

                insert_urls_google(referencia = dict_item['EAN'], loja = 'www.google.com.br'
                                   , urlanuncio = str(dict_item['URLGOOGLE']))
               
    df = pd.DataFrame(lista_dicts)
    df.to_csv(
        'C:\\Users\\Guilherme\\Documents\\ecommercefllaskapp\\collectgoogle\\excelfiles\\urls_base\\urls_base.csv')
    


search_products()