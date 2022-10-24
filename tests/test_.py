from quantitycreator.total import *
import os
from files import file_path

def filedeleter(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    else:
        return False

def tabledeleter(tablename,searchitem):
    nameprice = file_path+'/'+searchitem + '.db'
    connection = sqlite3.connect(nameprice)
    c =connection.cursor()
    c.execute(f"DROP TABLE IF EXISTS {tablename}")

def tablechecker(tablename,searchitem):
    nameprice = file_path+'/'+searchitem + '.db'
    connection = sqlite3.connect(nameprice)
    c =connection.cursor()
    tablelist = c.execute(f"SELECT * FROM sqlite_master WHERE type ='table'").fetchall()
    for item in tablelist:
        if tablename in item:
            return True

def test_quantity_generator():
    # Pass case
    assert quantity_generator(
        "Wai Wai Zing Hot & Spicy Instant Noodle, 5 Packs, Free BowlS") == 5
    assert quantity_generator("Maggi Veg Atta Noodles Masala 290 gm") == None
    assert quantity_generator(
        "Yashoda Foods Current Noodles Hot 'n' Spicy Chilli + Pepper 100gm Carton 20 Pieces") == 20
    assert quantity_generator(
        "Samyang Single Spicy Hot Chicken Ramen- 140gm* 5 pcs") == 5
    assert quantity_generator("Current 2X Spicy Noodles (Pack of 5 X 100 gm)") == 5

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
    assert weight_generator("Hot Pot Gourmet Spicy Vegetable Noodles 100G") == 100
    assert weight_generator("Parle Monaco Classic Regular 150g") == 150
    assert weight_generator("Mcvities Digestive -1Kg") == 1000

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
    assert scrape("randomthingentered")== None

def test_scrape_and_insertproducts():
    filedeleter(file_path+'/noodles.db')
    scrape_and_insert_products('noodles')
    assert tablechecker('productprice','noodles') == True
    assert scrape_and_insert_products('thisisbadurl')== None

def test_productprice_into_db():
    filedeleter(file_path+'/noodles.db')
    mainlist = scrape('noodles')
    product_price_into_db('noodles',mainlist)
    assert tablechecker('productprice','noodles') == True

def test_extract_productprice_from_db():
    filedeleter(file_path+'/noodles.db')
    mainlist = scrape('noodles')
    product_price_into_db('noodles',mainlist)
    assert type(extract_productprice_from_db('noodles')) == list
    assert len(extract_productprice_from_db('noodles'))>0
    assert extract_productprice_from_db("thisisabadsearch") == None

def test_extract_and_insert_productquantity():
    filedeleter(file_path+'/noodles.db')
    mainlist = scrape('noodles')
    product_price_into_db('noodles',mainlist)

    extract_and_insert_product_quantity('noodles')
    assert tablechecker('productquantity','noodles') == True

def test_productquantity_into_db():
    filedeleter(file_path+'/noodles.db')
    mainlist = scrape('noodles')
    product_price_into_db('noodles',mainlist)

    tabledeleter('productquantity','noodles')
    product_list = extract_productprice_from_db('noodles')
    productquantity_into_db("noodles",product_list)
    assert tablechecker('productquantity','noodles') == True

def test_main():
    filedeleter(file_path+'/noodles.db')
    main('noodles')
    assert tablechecker('productquantity','noodles') == True
    assert tablechecker('productprice','noodles') == True

if __name__ == "__main__":
    test_remove_punctuation()
    test_quantity_generator()
    test_stopwordremover()
    test_ngramcreator()
    test_weightgen()
    test_scrape()
    test_scrape_and_insertproducts()
    test_productprice_into_db()
    test_extract_productprice_from_db()
    test_extract_and_insert_productquantity()
    test_productquantity_into_db()
    test_main()

