import urllib.request
import urllib.parse
import urllib
import csv
import json
import requests

def get_html(url):
    response = urllib.request.urlopen(url)
    return  response.read()

def parse(fullList, ident):
    #parsing(get_html('https://portal.rosreestr.ru/wps/portal/p/is/cc_informSections/ais_mrn/!ut/p/c4/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gTZwNPL8tgY5MwIwM3A88AIwvv4FAPI3cjY_2CbEdFAO5-2_s!/'))
    ######Working with POST#####

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
             'limit': '100000'
             }
    headers = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
              'Chrome/58.0.3029.110 YaBrowser/17.6.1.749 Yowser/2.5 Safari/537.36'

    urlStart = 'https://portal.rosreestr.ru/wps/PA_AIS_MRN/rest/deal/'
    pagenumber = 1 #номер страницы
    urlEnd = '/table/data'
    qwe = 0
    for i in range(1,ident): #В цикле по всем регионам и городам
        value['region'] = fullList[i]
        print(value['region'])
        session = requests.Session()
        #т.к. в url страницы указываются с 0 до 10 , пришлось делать условие со страницей до 10 и после 10
        while (pagenumber <= 1):#Здесь указывается  - сколько страниц необходимо нам. (достать я их с сайта не смог, поэтому вручную приходится писать) для теста использовал 1
            if (pagenumber < 10):
                r = session.post(urlStart + '0' + str(pagenumber) + urlEnd, #для страницы < 10
                                 data=value)  # запрос таблицы с параметрами формы
            else:
                r = session.post(urlStart + str(pagenumber) + urlEnd,   #для страницы >= 10
                                 data=value)  # запрос таблицы с параметрами формы
            res = r.json() #результат записывам в формат json
            with open('result.json', 'w', encoding='utf-8') as outfile: #запись в json файл с кирилицей
                json.dump(res, outfile, sort_keys=True, indent=4, ensure_ascii=False)
            pagenumber += 1
        qwe += 1
        pagenumber = 1
        if (qwe == 4):
            break

if __name__ == '__main__':
    fullList = {}
    region = {}
    i = 0
    regionNumber = 0
    regionStr = '00000000000' #У региональных объектов изменяются только первые 2 цифры, следовательно за ними только 00000000000 - так и буду их отличать в цикле
    ids = []
    with open('KLADR_KLADR.csv', "r") as dbFile:
        reader = csv.reader(dbFile)
        for line in reader:
            if i != 39927: #На этом индексе ошибка из за форматирования файла,пришлось немного разобраться
                fullList[i] = str(line[2])
            else:   #Для того индекса в значении не список строк, а только 1 строка
                fullList[i] = line
                error = str(fullList[i]).split(',') #Разбиваем ее на разделители - запятую
                fullList[i] = str(error[2]) #Достааем нужную часть строки из предыдущей
            if ( str(fullList[i]).find(regionStr,2,) != -1): #если существует вхлждение с 00000000000
                region[regionNumber] = str(fullList[i])
                print('Region', region[regionNumber])
                regionNumber += 1
            #print ( '\n', 'i = ', i)
            #print('id города-обл: ', fullList[i])
            i+=1

        # print(idOfregions ,'\n')
        # nameOfGegions = soup.findAll('span',class_='red_span')
    #parse('https://portal.rosre estr.ru/wps/PA_AIS_MRN/rest/deal/01/table/data', fullList)
    parse(fullList,i)

#&quot;region&quot;:&quot;0100000000000&quot;,&quot;raion&quot;:&quot;0100300000000&quot;,&quot;city&quot;:&quot;&quot;,&quot;startEncumbranceDate&quot;:&quot;&quot;,&quot;endEncumbranceDate&quot;:&quot;&quot;,&quot;dealType&quot;:&quot;&quot;,&quot;encumbranceType&quot;:&quot;&quot;,&quot;objectKind&quot;:&quot;&quot;,&quot;objectPurpose&quot;:&quot;&quot;,&quot;dealSource&quot;:&quot;&quot;,&quot;agency&quot;:&quot;&quot;,&quot;startObjectsNumber&quot;:&quot;&quot;,&quot;endObjectsNumber&quot;:&quot;&quot;,&quot;startArea&quot;:&quot;&quot;,&quot;endArea&quot;:&quot;&quot;,&quot;startDealPrice&quot;:&quot;&quot;,&quot;endDealPrice&quot;:&quot;&quot;}