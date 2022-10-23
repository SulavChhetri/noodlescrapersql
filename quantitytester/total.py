import sqlite3
import requests
import json
import sys
sys.path.append("..")


with open('../files/stopwords.txt', 'r')as file:
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
        product_price_into_db(searchitem,mainlist)


def product_price_into_db(searchitem,mainlist):
    nameprice = '../files/'+searchitem + '.db'
    connection = sqlite3.connect(nameprice)
    c = connection.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS productprice(Product name TEXT, Price TEXT)''')
    for item in mainlist:
        price = 'Rs.' + str(int(float(item['utLogMap']['current_price'])))
        c.execute('''INSERT INTO Productprice VALUES(?,?)''',
                    (item['name'], price))
    connection.commit()


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
    nameprice = '../files/'+searchitem + '.db'
    try:
        connection = sqlite3.connect(nameprice)
        c = connection.cursor()
        c.execute('''SELECT * FROM productprice''')
        product_list = c.fetchall()
        return product_list
    except:
        return None


def extract_and_insert_product_quantity(searchitem):
    product_list = extract_productprice_from_db(searchitem)
    if product_list != None:
        return productquantity_into_db(searchitem,product_list)


def productquantity_into_db(searchitem,product_list):
    nameprice = '../files/'+searchitem + '.db'
    connection = sqlite3.connect(nameprice)
    c = connection.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productquantity(Product name TEXT, Price TEXT,Quantity INT, Weight INT, Unit of Weight TEXT)''')
    for item in product_list:
        quantity = quantity_generator(item[0])
        weight = weight_generator(item[0])
        c.execute('''INSERT INTO productquantity VALUES(?,?,?,?,?)''', (
            item[0], item[1], 1 if quantity == None else quantity, weight, None if weight == None else 'gm'))
        connection.commit()


def main(searchitem):
    nameprice = '../files/'+searchitem + '.db'
    connection = sqlite3.connect(nameprice)
    c = connection.cursor()
    tablelist = c.execute(
        '''SELECT * FROM sqlite_master WHERE type ='table';''').fetchall()
    if not ('productprice' in tablelist):
        scrape_and_insert_products(searchitem)
        extract_and_insert_product_quantity(searchitem)
    else:
        extract_and_insert_product_quantity(searchitem)

# main('noodles')
