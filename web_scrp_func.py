
# Import Modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import random
import os

# User agents
def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]
 
    return random.choice(uastrings)

def DICT_INFO_SUPERMARKET(supermarket):

    if supermarket == "ahorramas":
        dict_info = {
                'pollo':"https://www.ahorramas.com/frescos/carniceria/pollo/?pmin=0.01&start=0&sz=200",
                'conejo_pavo_otrasaves':"https://www.ahorramas.com/frescos/carniceria/conejo-pavo-y-otras-aves/?pmin=0.01&start=0&sz=200",
                'jamon':"https://www.ahorramas.com/frescos/charcuteria/jamones-y-paletillas-curadas/?pmin=0.01&start=0&sz=200",
                'huevo':"https://www.ahorramas.com/frescos/huevos/huevos-de-suelo/?pmin=0.01&start=0&sz=200",
                'queso':"https://www.ahorramas.com/frescos/quesos/quesos-en-barra-y-frescos/?pmin=0.01&start=0&sz=200",
                'leche':"https://www.ahorramas.com/lacteos/leche-y-bebidas-vegetales/leche-semidesnatada/?pmin=0.01&start=0&sz=200",
                'yogurt_griego':"https://www.ahorramas.com/lacteos/yogures-kefir-y-postres/yogures-griegos/?pmin=0.01&start=0&sz=200",
                'cafe':"https://www.ahorramas.com/alimentacion/cacao-cafes-e-infusiones/cafe-molido/?pmin=0.01&start=0&sz=200",
                'pan_de_molde':"https://www.ahorramas.com/alimentacion/panaderia/pan-de-molde/?pmin=0.01&start=0&sz=200",
                'ensaladas':"https://www.ahorramas.com/frescos/verduras-y-hortalizas/lechugas-y-ensaladas/?pmin=0.01&start=0&sz=200",
                'atun':"https://www.ahorramas.com/alimentacion/conservas-de-pescado/atun/",
                'limon_naranja':"https://www.ahorramas.com/frescos/frutas/naranja-limon-y-citricos/",
                'platano_uva':"https://www.ahorramas.com/frescos/frutas/platanos-y-uvas/",
                'piña_kiwi_aguacate_tropicales':"https://www.ahorramas.com/frescos/frutas/pinas-kiwis-aguacates-y-tropicales/?pmin=0.01&start=0&sz=200"
                }

    elif supermarket == "dia":
        dict_info = {
             'Platos preparados':"https://www.dia.es/compra-online/platos-preparados/cf",
             'Ofertas':"https://www.dia.es/compra-online/ofertas-DIA-online",
             'Frescos':"https://www.dia.es/compra-online/frescos/cf",
             'Despensa':"https://www.dia.es/compra-online/despensa/cf",
             'Bebidas':"https://www.dia.es/compra-online/bebidas/cf",
             'Bodega':"https://www.dia.es/compra-online/bodega/cf",
             'Congelados':"https://www.dia.es/compra-online/congelados/cf",
             'Cuidado personal':"https://www.dia.es/compra-online/cuidado-personal/cf",
             'Bebe':"https://www.dia.es/compra-online/bebe/cf",
             'Cuidado del hogar':"https://www.dia.es/compra-online/cuidado-del-hogar/cf",
             'Mascotas':"https://www.dia.es/compra-online/mascotas/cf"
             }
    else:
        print("error")
    return(dict_info)

def GET_URL_INFO(url_text,headers):    
    source = requests.get(url_text, headers = headers).text
    soup =  BeautifulSoup(source, 'html.parser')
    return(soup)

def CLEAN_DATA_AHORRAMAS(soup,keyword):
    product_name = [i.text for i in soup.find_all(attrs={"class":"link product-name-gtm"})]
    product_price = [i.text.replace("\n","") for i in soup.select("div[class='price'] > div > span > span[class='value']")]
    product_link = ['https://www.ahorramas.com' + i.get("href") for i in soup.select("div[class='image-container'] > a")]    
    df = pd.DataFrame({'Name':[i.lower().strip() for i in product_name],
                       'Price':[i.lower().strip().replace("€","").replace(",",".") for i in product_price],
                       'URL':product_link,
                       'Keyword':keyword})
    df['Price'] = df['Price'].astype(float)
    return(df)


def CLEAN_DATA_DIA(url_text,soup,keyword,headers):
    n_pages = int([i.text.replace("\n","")  for i in soup.find_all(attrs={"class":"pagination-list-and-total"})][0].split("de")[1].replace(" ",""))
    df_all_pages = pd.DataFrame()    
    for i_page in range(n_pages):
        try:
            url_text_pages = url_text + "?page=" + str(i_page)            
            source = requests.get(url_text_pages, headers = headers).text
            soup =  BeautifulSoup(source, 'html.parser')    
            product_name = [i.text.replace("\n","").replace("\r","").replace("\t","") for i in soup.find_all(attrs={"class":"details"})]
            filtered_product_name = [i for i in product_name if i != "" ]
            product_price = [i.text.replace("\n","").replace("\r","").replace("\t","").replace("\xa0"," ").split("€")[0].replace(",",".").replace(" ","")  for i in soup.find_all(attrs={"class":"price"})]
            product_price = [float(i) if i != "" else 0 for i in product_price]
            filtered_product_price = [i for i in product_price if (i > 0 )]
            product_link = ['https://www.dia.es' + i.get("href")  for  i in soup.find_all(attrs={"class":"productMainLink"})]
            df = pd.DataFrame({'Name':[i.lower().strip() for i in filtered_product_name],
                                'Price':filtered_product_price,
                               'URL':product_link,
                               'Keyword':keyword,
                               'N page':i_page})            
            df['Price'] = df['Price'].astype(float)        
            df_all_pages = df_all_pages.append(df)
            print("done")
        except:
            print("error")   
    return(df_all_pages)

