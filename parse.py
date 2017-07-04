import urllib.request
import urllib.parse
import urllib
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

def get_html(url):
    response = urllib.request.urlopen(url)
    return  response.read()

def parse(url):
    #parsing(get_html('https://portal.rosreestr.ru/wps/portal/p/is/cc_informSections/ais_mrn/!ut/p/c4/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gTZwNPL8tgY5MwIwM3A88AIwvv4FAPI3cjY_2CbEdFAO5-2_s!/'))
    #################Working with POST###############
    myUrl = 'https://portal.rosreestr.ru/wps/portal/p/is/cc_informSections/ais_mrn/!ut/p/c4/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gTZwNPL8tgY5MwIwM3A88AIwvv4FAPI3cjY_2CbEdFAO5-2_s!/'
    value = {'region': '0100000000000',
             'raion': '0100300000000',
             'city': '',
             'startEncumbranceDate': '',
             'endEncumbranceDate': '',
             'dealType': '',
             'encumbranceType': '',
             'objectKind': '',
             'objectPurpose': '',
             'start': '0',
             'limit': '10000'
             }

    html = get_html('https://portal.rosreestr.ru/wps/portal/p/is/cc_informSections/ais_mrn/!ut/p/c4/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gTZwNPL8tgY5MwIwM3A88AIwvv4FAPI3cjY_2CbEdFAO5-2_s!/')
    #soup = BeautifulSoup(html,'html.parser')
    data = {'region': '0100000000000',
                'start': '0',
                'limit': '10000'
                }
    headers = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Chrome/58.0.3029.110 YaBrowser/17.6.1.749 Yowser/2.5 Safari/537.36'

    session = requests.Session()
    r = session.post(url, data=value)  # запрос таблицы с параметрами формы
    return r.json()

if __name__ == '__main__':
    urlStart = 'https://portal.rosreestr.ru/wps/PA_AIS_MRN/rest/deal/'
    pagenumber = 1
    urlEnd = '/table/data'
    #parse('https://portal.rosre estr.ru/wps/PA_AIS_MRN/rest/deal/01/table/data')
    while (pagenumber <= 2):
        if (pagenumber < 10):
            print('\n', '0', pagenumber,'\n')
            res = parse(urlStart+'0'+str(pagenumber)+urlEnd)
            with open('result.json', 'w',encoding='utf-8') as outfile:
                json.dump(res, outfile, sort_keys=True, indent=4,ensure_ascii=False)
        else:
            print('\n', pagenumber, '\n')
            res = parse(urlStart + str(pagenumber) + urlEnd)
            with open('result.json', 'w',encoding='utf-8') as outfile:
                json.dump(res, outfile, sort_keys=True, indent=4,ensure_ascii=False)
        pagenumber += 1

#&quot;region&quot;:&quot;0100000000000&quot;,&quot;raion&quot;:&quot;0100300000000&quot;,&quot;city&quot;:&quot;&quot;,&quot;startEncumbranceDate&quot;:&quot;&quot;,&quot;endEncumbranceDate&quot;:&quot;&quot;,&quot;dealType&quot;:&quot;&quot;,&quot;encumbranceType&quot;:&quot;&quot;,&quot;objectKind&quot;:&quot;&quot;,&quot;objectPurpose&quot;:&quot;&quot;,&quot;dealSource&quot;:&quot;&quot;,&quot;agency&quot;:&quot;&quot;,&quot;startObjectsNumber&quot;:&quot;&quot;,&quot;endObjectsNumber&quot;:&quot;&quot;,&quot;startArea&quot;:&quot;&quot;,&quot;endArea&quot;:&quot;&quot;,&quot;startDealPrice&quot;:&quot;&quot;,&quot;endDealPrice&quot;:&quot;&quot;}