# from quantitytester.total import *
# import os,pandas as pd

# def filedeleter(file_path): # return True if the file is deleted, else return False
#     if os.path.isfile(file_path):
#         os.remove(file_path)
#         return True
#     else:
#         return False

# def filechecker(filename): #return True if the file has data, else return False
#     path ='../files/'+filename
#     try:
#         with open(path,'r') as f:
#             f.readline()
#             line = f.readline()
#             if line == '':
#                 return False
#             else:
#                 return True
#     except:
#         return False


# def test_quantitytester():
#     # Pass case
#     assert quantitygen(
#         "Wai Wai Zing Hot & Spicy Instant Noodle, 5 Packs, Free BowlS") == 5
#     assert quantitygen("Maggi Veg Atta Noodles Masala 290 gm") == None
#     assert quantitygen(
#         "Yashoda Foods Current Noodles Hot 'n' Spicy Chilli + Pepper 100gm Carton 20 Pieces") == 20
#     assert quantitygen(
#         "Samyang Single Spicy Hot Chicken Ramen- 140gm* 5 pcs") == 5
#     assert quantitygen("Current 2X Spicy Noodles (Pack of 5 X 100 gm)") == 5


# def test_remove_punctuation():
#     assert remove_punctuation("What are you doing?") == "What are you doing"
#     assert remove_punctuation(
#         "Samyang Single Spicy Hot Chicken Ramen- 140gm* 5 pcs") == "Samyang Single Spicy Hot Chicken Ramen 140gm 5 pcs"


# def test_stopwordremover():
#     assert stopwordsremover(
#         "CG Wai Wai Quick Masala Curry Instant Noodle 60gm Pack of 5") == "CG Wai Wai Quick Masala Curry Instant Noodle 60gm Pack 5"
#     assert stopwordsremover(
#         "Wai Wai Chicken Bhujia Curry 750g") == "Wai Wai Chicken Bhujia Curry 750g"


# def test_ngramcreator():
#     assert ngramcreator("Hot Pot Gourmet Spicy Vegetable Noodles 100G", 2) == [
#         'Hot Pot', 'Pot Gourmet', 'Gourmet Spicy', 'Spicy Vegetable', 'Vegetable Noodles', 'Noodles 100G']
#     assert ngramcreator("Samyang Buldak Jjajang Hot Chicken Flavor Ramen(Pack of 5)",2) == [
#         'Samyang Buldak', 'Buldak Jjajang', 'Jjajang Hot', 'Hot Chicken', 'Chicken Flavor', 'Flavor RamenPack', 'RamenPack 5']
#     assert ngramcreator("Spartan Egg Chowmein 360G",1) == ["Spartan","Egg","Chowmein","360G"]

# def test_scrape(): 
#     #Fail Case, no file is created because of a bad url
#     scrape("randomthing")
#     assert filechecker("randomthingprice.csv") == False
    
#     #Pass Case, the scraped data is stored in a csv file
#     filedeleter("../files/noodlesprice.csv")
#     scrape("noodles")
#     assert filechecker("noodlesprice.csv")== True

# def test_csvquantity():
#     filedeleter("../files/noodlesquantity.csv")
#     csvquantity("noodles")
#     assert filechecker("noodlesquantity.csv") == True
#     assert filechecker("wrongfile.csv") == False

# def test_weightgen():
#     assert weightgen("Hot Pot Gourmet Spicy Vegetable Noodles 100G") == 100
#     assert weightgen("Parle Monaco Classic Regular 150g") == 150
#     assert weightgen("Mcvities Digestive -1Kg") == 1000
#     return "Passed"

# def test_main():
#     filedeleter("../files/noodlesprice.csv")
#     filedeleter("../files/noodlesquantity.csv")
#     main("noodles")
#     assert filechecker("noodlesprice.csv") == True
#     assert filechecker("noodlesquantity.csv") ==True

#     assert len(pd.read_csv("../files/noodlesprice.csv"))==len(pd.read_csv("../files/noodlesquantity.csv"))

# if __name__ == "__main__":
#     test_remove_punctuation()
#     test_quantitytester()
#     test_stopwordremover()
#     test_ngramcreator()
#     test_scrape()
#     test_main()
#     test_csvquantity()
#     test_weightgen()

