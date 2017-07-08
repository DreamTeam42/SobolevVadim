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

    myUrl = 'https://portal.rosreestr.ru/wps/portal/p/is/cc_informSections/ais_mrn/!ut/p/c4/04_SB8K8xLLM9MSSzPy8xBz9CP0os3gTZwNPL8tgY5MwIwM3A88AIwvv4FAPI3cjY_2CbEdFAO5-2_s!/'
    filterLine= {'region': '0100000000000',
             'raion': '',
             'city': '',
             'street': '',
             'startEncumbranceDate': '',
             'endEncumbranceDate': '',
             'dealType': '',
             'encumbranceType': '',
             'objectKind': '',
             'objectPurpose': '',
             'start': 0,
             'limit': 10000
             }
    headers = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
              'Chrome/58.0.3029.110 YaBrowser/17.6.1.749 Yowser/2.5 Safari/537.36'

    urlStart = 'https://portal.rosreestr.ru/wps/PA_AIS_MRN/rest/deal/'
    pagenumber = 1 #номер страницы
    urlEnd = '/table/data'
    qwe = 0
    session = requests.Session()
    session.headers.update({'User-Agent': headers})
    for i in range(0, ident): #В цикле по всем регионам и городам
        filterLine['region'] = fullList[i]
        print(filterLine['region'])

        while (pagenumber <= 10):#Здесь указывается  - сколько объектов необходимо * 10000 ( получается до 100000 )
            #format_url = '{}{:02d}{}'.format(urlStart + str(filterLine['region'][0:2]) , urlEnd)
            url = urlStart + filterLine['region'][0:2] + urlEnd # сделал так т.к. ваш пример выше не работал ( не силен в питоне )
            print(url)
            print('start = ', filterLine['start'])
            print('limit = ', filterLine['limit'])

            try:
                r = session.post(url, data=filterLine)
                res = r.json() #результат записывам в формат json
                with open('res'+filterLine['region']+'_'+str(pagenumber)+'.json', 'w', encoding='utf-8') as outfile: #запись в json файл с кирилицей и номерос стр.
                    json.dump(res, outfile, sort_keys=True, indent=4, ensure_ascii=False) #в файл записываются по 10000 объектов
                pagenumber += 1
                step = 10000
                filterLine['start'] += step
            except requests.expections.HTTPError as err:
                print('HTTP Error occured')
                print('Response is: {content}'.format(content=err.response.content))
        qwe += 1 # qwe - для цикла,чтобы можно было его остановить
        filterLine['start'] = 0 #сбрасываем параметры для след. региона
        pagenumber = 1
        if (qwe == 2):
            break

if __name__ == '__main__':
    fullList = {}
    region = {}
    i = 0
    regionNumber = 0
    regionStr = '00000000000' #У региональных объектов изменяются только первые 2 цифры, следовательно за ними только 00000000000 - так и буду их отличать в цикле
    ids = []
    with open('KLADR_KLADR.csv', "r", encoding='cp1251') as dbFile:
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
    parse(region, regionNumber)

#&quot;region&quot;:&quot;0100000000000&quot;,&quot;raion&quot;:&quot;0100300000000&quot;,&quot;city&quot;:&quot;&quot;,&quot;startEncumbranceDate&quot;:&quot;&quot;,&quot;endEncumbranceDate&quot;:&quot;&quot;,&quot;dealType&quot;:&quot;&quot;,&quot;encumbranceType&quot;:&quot;&quot;,&quot;objectKind&quot;:&quot;&quot;,&quot;objectPurpose&quot;:&quot;&quot;,&quot;dealSource&quot;:&quot;&quot;,&quot;agency&quot;:&quot;&quot;,&quot;startObjectsNumber&quot;:&quot;&quot;,&quot;endObjectsNumber&quot;:&quot;&quot;,&quot;startArea&quot;:&quot;&quot;,&quot;endArea&quot;:&quot;&quot;,&quot;startDealPrice&quot;:&quot;&quot;,&quot;endDealPrice&quot;:&quot;&quot;}