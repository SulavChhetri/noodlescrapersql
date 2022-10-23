from quantitytester.total import *
import os

def filedeleter(file_path): # return True if the file is deleted, else return False
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    else:
        return False

def tabledeleter(tablename,searchitem):
    nameprice = '../files/'+searchitem+ '.db'
    connection = sqlite3.connect(nameprice)
    c =connection.cursor()
    c.execute(f"DROP TABLE IF EXISTS {tablename}")

def tablechecker(tablename,searchitem):
    nameprice = '../files/'+searchitem+ '.db'
    connection = sqlite3.connect(nameprice)
    c =connection.cursor()
    tablelist = c.execute(f"SELECT * FROM sqlite_master WHERE type ='table'").fetchall()
    for item in tablelist:
        if tablename in item:
            return True

def test_quantitytester():
    # Pass case
    assert quantitygen(
        "Wai Wai Zing Hot & Spicy Instant Noodle, 5 Packs, Free BowlS") == 5
    assert quantitygen("Maggi Veg Atta Noodles Masala 290 gm") == None
    assert quantitygen(
        "Yashoda Foods Current Noodles Hot 'n' Spicy Chilli + Pepper 100gm Carton 20 Pieces") == 20
    assert quantitygen(
        "Samyang Single Spicy Hot Chicken Ramen- 140gm* 5 pcs") == 5
    assert quantitygen("Current 2X Spicy Noodles (Pack of 5 X 100 gm)") == 5

def test_remove_punctuation():
    assert remove_punctuation("What are you doing?") == "What are you doing"
    assert remove_punctuation(
        "Samyang Single Spicy Hot Chicken Ramen- 140gm* 5 pcs") == "Samyang Single Spicy Hot Chicken Ramen 140gm 5 pcs"

def test_stopwordremover():
    assert stopwordsremover(
        "CG Wai Wai Quick Masala Curry Instant Noodle 60gm Pack of 5") == "CG Wai Wai Quick Masala Curry Instant Noodle 60gm Pack 5"
    assert stopwordsremover(
        "Wai Wai Chicken Bhujia Curry 750g") == "Wai Wai Chicken Bhujia Curry 750g"

def test_weightgen():
    assert weightgen("Hot Pot Gourmet Spicy Vegetable Noodles 100G") == 100
    assert weightgen("Parle Monaco Classic Regular 150g") == 150
    assert weightgen("Mcvities Digestive -1Kg") == 1000

def test_ngramcreator():
    assert ngramcreator("Hot Pot Gourmet Spicy Vegetable Noodles 100G", 2) == [
        'Hot Pot', 'Pot Gourmet', 'Gourmet Spicy', 'Spicy Vegetable', 'Vegetable Noodles', 'Noodles 100G']
    assert ngramcreator("Samyang Buldak Jjajang Hot Chicken Flavor Ramen(Pack of 5)",2) == [
        'Samyang Buldak', 'Buldak Jjajang', 'Jjajang Hot', 'Hot Chicken', 'Chicken Flavor', 'Flavor RamenPack', 'RamenPack 5']
    assert ngramcreator("Spartan Egg Chowmein 360G",1) == ["Spartan","Egg","Chowmein","360G"]

def test_scrape(): 
    assert type(scrape("noodles")) == list
    assert len(scrape('sweet'))>0
  
    #Fail Case, no file is created because of a bad url
    assert scrape("randomthingentered")== "Bad Url"

def test_middlewareprice():
    assert type(middlewareprice('noodles')) == list
    assert len(middlewareprice('biscuits'))>0
    assert middlewareprice('thisisbadurl')== "Bad Url"

def test_sqlproductprice():
    tabledeleter('productprice','sweet')
    sqlproductprice('sweet')
    assert tablechecker('productprice','sweet') == True

def test_csvpricesearcher():
    filedeleter('../files/noodles.db')
    sqlproductprice('noodles')
    assert type(csvpricesearcher('noodles')) == list
    assert len(csvpricesearcher('noodles'))>0
    assert csvpricesearcher("thisisabadsearch") == None

def test_middlewarequantity():
    filedeleter('../files/noodles.db')
    sqlproductprice('noodles')
    assert type(middlewarequantity('noodles')) == list
    assert len(middlewarequantity('noodles'))>0
    assert middlewarequantity("thisisabadsearch") == None

def test_csvquantity():
    filedeleter('../files/noodles.db')
    sqlproductprice('noodles')
    tabledeleter('productquantity','noodles')
    csvquantity("noodles")
    assert tablechecker('productquantity','noodles') == True

def test_main():
    filedeleter('../files/noodles.db')
    main('noodles')
    assert tablechecker('productquantity','noodles') == True
    assert tablechecker('productprice','noodles') == True

if __name__ == "__main__":
    test_remove_punctuation()
    test_quantitytester()
    test_stopwordremover()
    test_ngramcreator()
    test_weightgen()
    test_scrape()
    test_middlewareprice()
    test_sqlproductprice()
    test_csvpricesearcher()
    test_middlewarequantity()
    test_csvquantity()
    test_main()

