import sqlite3
import requests
import json
import os
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
file_path = os.path.join(ROOT_DIR, 'files')

with open(os.path.join(file_path, 'stopwords.txt'), 'r')as file:
    lines = [line.rstrip('\n') for line in file]


def scrape(searchitem):
    try:
        darazurl = 'https://www.daraz.com.np/catalog/?_keyori=ss&from=input&page=1&q=' + searchitem
        r = requests.get(darazurl).text
        jsonresponse = json.loads(r.split("window.pageData=")[
                                  1].split('</script>')[0])
        mainlist = jsonresponse['mods']['listItems']
        return mainlist
    except:
        return None


def scrape_and_insert_products(searchitem):
    mainlist = scrape(searchitem)
    if mainlist:
        product_price_into_db(searchitem, mainlist)


def product_price_into_db(searchitem, mainlist):
    nameprice = file_path+'/'+searchitem + '.db'
    with sqlite3.connect(nameprice) as conn:
        c = conn.cursor()
        c.execute(
        '''CREATE TABLE IF NOT EXISTS productprice(Product name TEXT, Price TEXT)''')
        for item in mainlist:
            price = 'Rs.' + str(int(float(item['utLogMap']['current_price'])))
            c.execute('''INSERT INTO productprice VALUES(?,?)''',
                    (item['name'], price))

def stopwordsremover(sentence):
    nostopword_sentence = list()
    for item in sentence.split():
        if not item.lower() in lines:
            nostopword_sentence.append(item)
    return ' '.join(nostopword_sentence)


def remove_punctuation(sentence):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    finalsentence = ""
    for item in sentence:
        if item not in punc:
            finalsentence += item
    return finalsentence


def ngramcreator(strings, n_grams):
    finallist = []
    nostopword = stopwordsremover(strings)
    splitlist = remove_punctuation(nostopword).split()
    n_grams_range = len(splitlist)-n_grams+1
    if (len(splitlist) < n_grams):
        return [remove_punctuation(strings)]
    else:
        for x in range(n_grams_range):
            finalstring = ''
            for i in range(n_grams):
                finalstring = finalstring+' '+splitlist[x+i]
            finallist.append(finalstring.lstrip())
        return finallist


def quantity_generator(item):
    quantitylist = ['Packs', 'packs', 'Pack of',
                    'pcs', 'Pieces', 'Pack', 'RamenPack']
    n_gram = ngramcreator(item, 2)
    for items in n_gram:
        if not (''.join(items.split()).isalpha()):
            for ite in items.split():
                if ite in quantitylist:
                    for itee in items.split():
                        if itee.isnumeric():
                            return int(itee)


def weight_generator(item):
    items = item.split()
    a = ''.join(items).lower()
    weight = []
    for i in range(len(a)):
        if a[i].isnumeric():
            weight.append(a[i])
            if a[i+1] == 'g':
                return int(''.join(weight))
            elif a[i+1] == 'k' and a[i+2] == 'g':
                return int(''.join(weight))*1000
        else:
            weight = []


def extract_productprice_from_db(searchitem):
    nameprice = file_path+'/'+searchitem + '.db'
    try:
        with sqlite3.connect(nameprice) as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM productprice''')
            product_list = c.fetchall()
            return product_list
    except:
        return None


def extract_and_insert_product_quantity(searchitem):
    product_list = extract_productprice_from_db(searchitem)
    if product_list != None:
        return productquantity_into_db(searchitem, product_list)


def productquantity_into_db(searchitem, product_list):
    nameprice = file_path+'/'+searchitem + '.db'
    with sqlite3.connect(nameprice) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS productquantity(Product name TEXT, Price TEXT,Quantity INT, Weight INT, Unit of Weight TEXT)''')
        for item in product_list:
            quantity = quantity_generator(item[0])
            weight = weight_generator(item[0])
            c.execute('''INSERT INTO productquantity VALUES(?,?,?,?,?)''', (
                item[0], item[1], 1 if quantity == None else quantity, weight, None if weight == None else 'gm'))

def tablechecker(tablename,searchitem):
    nameprice = file_path+'/'+searchitem + '.db'
    with sqlite3.connect(nameprice) as conn:
        c = conn.cursor()
        tablelist = c.execute(f"SELECT * FROM sqlite_master WHERE type ='table'").fetchall()
        for item in tablelist:
            if tablename in item:
                return True
        return False

def main(searchitem):
    if not (tablechecker('productprice',searchitem)):
        scrape_and_insert_products(searchitem)
        extract_and_insert_product_quantity(searchitem)
    else:
        extract_and_insert_product_quantity(searchitem)


main('noodles')
# scrape_and_insert_products('noodles')