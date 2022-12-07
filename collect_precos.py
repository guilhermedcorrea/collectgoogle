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
from functools import wraps
from config import get_engine
from sqlalchemy import text, insert
from tabela import MonitoramentoPrecos




def insert_precod_google_shopping(*args, **kwargs) -> None:
        engine = get_engine()
        with engine.connect() as conn:
            try:
                result = conn.execute(
                            insert(MonitoramentoPrecos),
                            [
                                {"paginaanuncio": kwargs.get('pagina'), "concorrente": kwargs.get('concorrente'),"precoconcorrente":float(kwargs.get('preco'))
                                ,"nomeproduto":kwargs.get('concorrente')
                                ,"ean":kwargs.get('ean'),"urlgoogle":kwargs.get('url'),"vendidoem":kwargs.get('canal')}
                                ]
                                )
            except:
                print("error")
          
          
                  
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"C:\\Users\\Guilherme\\Documents\\ecommercefllaskapp\\collectgoogle\\chromedriver\\chromedriver.exe")


class Google:
    def __init__(self):
        self.dict = {}
        self.lista_dicts = []

    def scroll(self) -> None:

        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True

    def get_urls(self) -> list:
        lista_dicts = []

        data = pd.read_csv(
            "C:\\Users\\Guilherme\\Documents\\ecommercefllaskapp\\collectgoogle\\excelfiles\\urls_base\\urls_sellers.csv",sep=";", encoding='latin-1')
        for i, row in data.iterrows():
            ean = row[2]
            url_google = row[0]
            nomeproduto = row[1]
           
            dict_items = {}
            dict_items['eanreferencia'] = ean
            dict_items['paginaprodutogoogle'] = url_google
            dict_items['nomeproduto'] = nomeproduto
            lista_dicts.append(dict_items)
        
        return lista_dicts

    def get_precos(self) -> None:
        lista_dicts = []
        dicts = self.get_urls()
        for dict in dicts:
            time.sleep(1)
            
            driver.get(dict['paginaprodutogoogle'])
            self.scroll()
            name_sellers = []
            urls = []
            items = []
            nomeproduto = []
            prices_sellers = []
            eanferencia = []
            perfil_url = []

            driver.implicitly_wait(7)

            try:
                names = driver.find_elements(By.XPATH,'//*[@id="sh-osd__online-sellers-cont"]/tr/td[1]/div[1]/a')
                for name in names:
                    nam = name.text.strip()
                    name_sellers.append(nam)
                    nomeproduto.append(dict['nomeproduto'])
                    urls.append(dict['paginaprodutogoogle'])
                    eanferencia.append(dict['eanreferencia'])
            except Exception as e:
                print("Error", e)
            
            try:
                prices = driver.find_elements(By.XPATH,'//*[@id="sh-osd__online-sellers-cont"]/tr/td[4]/div/div[1]')
                for pric in prices:
                    price = pric.text.replace("R$","").replace(".","").replace(",",".").strip()
                    prices_sellers.append(price)
            except:
                prices_sellers.append("preçonaoencontrado")

            try:
                perfil_seller = driver.find_elements(By.XPATH,'//*[@id="sh-osd__online-sellers-cont"]/tr/td[5]/div/a')
                for perfil in perfil_seller:
                    perfil = perfil.get_attribute('href')
                    perfil_url.append(perfil)
            except:
                perfil_url.append(dict['paginaprodutogoogle'])

            name_se = [i for i in name_sellers if i != '']

            for i, num in enumerate(name_se):
                desc={}
                try:
                    desc['Sellers']=name_se[i]
                except:
                    desc['Sellers'] = "error"

                try:
                    desc['Prices']=prices_sellers[i]
                except:
                    desc['Prices'] = "error"

                try:
                    desc['Urls']=urls[i]
                except:
                    desc['Urls'] = "error"

                try:
                    desc["EanReferencia"] = eanferencia[i]
                except:
                    desc["EanReferencia"] = "error"

                try:
                    desc['perfilseller']=perfil_url[i]
                except:
                    desc['perfilseller'] = "error"

                try: 
                    desc['nomeproduto'] = nomeproduto[i]
                except:
                    desc['nomeproduto'] = "error"

              
                lista_dicts.append(desc)
                
                try:
                    insert_precod_google_shopping(pagina=desc['perfilseller'],concorrente=desc['Sellers']
                                ,preco=desc['Prices'],ean=desc['EanReferencia'],url=desc['Urls']
                                ,canal='GoogleShopping')
                except:
                    print("error")
      
        
        datagoogle = pd.DataFrame(lista_dicts)
        datagoogle.to_csv(
            "C:\\Users\\Guilherme\\Documents\\ecommercefllaskapp\\collectgoogle\\excelfiles\\precos\\google_precos.csv",sep=";", encoding='latin-1')
  
google = Google()
google.get_precos()