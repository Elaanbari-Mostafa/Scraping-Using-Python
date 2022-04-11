#https://www.ldlc.com/informatique/ordinateur-portable/pc-portable/c4265/


import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv

dic = {}

#open csv file
filecsv = open('SouqDataapple.csv', 'w',encoding='utf8')
csv_columns = ['name','price','image','Description for the website','Sales Description','Is published',"Extra Product Media/Name","Extra Product Media/Image","Product Attributes/Attribute","Product Attributes/values"]
writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
writer.writeheader()

#open json file
file =  open("scrp.json", "w",encoding='utf8')
file.write('[\n')

req = requests.get("https://www.ldlc.com/informatique/ordinateur-portable/pc-portable/c4265/")
soup = BeautifulSoup(req.content, "html.parser")

#start script
produits = soup.find('div',{'class' : 'listing-product'}).ul.findAll('li')
print(len(produits))

countP = 1
for produit in produits:
    urlP = "https://www.ldlc.com" + produit.find('h3',{'class':'title-3'}).a.get('href')
    print("----"+str(countP)+"----")
    print(urlP)
    countP+=1
    #go to url Product
    roc = requests.get(urlP)
    sop = BeautifulSoup(roc.content, "html.parser")

    name  = sop.find('h1',{'class':'title-1'}).text.strip("\n").strip()  
    priceTemp = float(sop.find('aside').div.div.text.replace('€','.').replace(' ','')) * 10.61
    price = str(round(priceTemp, 2))
    #description = sop.find('div',{'class':'title'}).h2.text
    description = str(sop.find('div',{'id':'descriptif'})).replace('<div class="title-1">Descriptif</div>','').replace('<div class="brand-logo">Acer</div>','').replace("<div class=\"emphasis\"><strong>Qu\'est ce que le DAS ou Débit d'Absorption Spécifique ?</strong><p>Le débit d'absorption spécifique (DAS) local quantifie l\'exposition de l\'utilisateur aux ondes électromagnétiques de l\'équipement concerné. Le DAS maximal autorisé est de 2 W/kg pour la tête et le tronc et de 4 W/kg pour les membres.</p><p><em>Tous les produits vendus sur le site LDLC.com sont conformes à cette réglementation. Les valeurs DAS des produits concernés sont indiquées au niveau des fiches produits dans la partie fiche technique.</em></p></div>",'')

    Sales_Description = sop.find('p',{'class':'desc'}).text.strip()
    img = sop.find('div',{'class':'product'}).a.img.get('src')
    Media_ = sop.find('div',{'class':'zoom'}).find_all('a',{'class':'pVignette photo'})
    TableTR = sop.find('table',{'id':'product-parameters'}).find_all('tr')
    TablesRows = []
    for tr in TableTR:
      # TablesRows.append(tr.text[1:-1].strip().split('\n'))
      TablesRows.append(tr.get_text()[1:-1].replace(' ',''))
    print(TablesRows)
    break
    # write csv
    del Media_[0]
    Media_Name = Media_[0].get('href').split('/')[-1].split('.')[0]
    writer.writerow({'name': name, 'price': price, 'image':img,'Description for the website': description,'Sales Description':Sales_Description,'Is published':'True',"Extra Product Media/Name": Media_Name,"Extra Product Media/Image":Media_[0].get('href') ,"Product Attributes/Attribute":"+++","Product Attributes/Attribute,Product Attributes/values":"+++"})
    for imgMedia in Media_:
       Media_Name = imgMedia.get('href').split('/')[-1].split('.')[0]
       writer.writerow({'name': '', 'price': '', 'image':'','Description for the website': '','Sales Description':'','Is published':'',"Extra Product Media/Name": Media_Name,"Extra Product Media/Image":imgMedia.get('href') })
   


    #write json
   # dic['name'] = name
   # dic['price'] = price
   # dic['image'] = img
   # dic['Description for the website'] = description
   # dic['Sales Description'] = Sales_Description
  #  dic["Is published"] = "true"
    
    #json_data = json.dumps(dic,ensure_ascii=False)
    #file.write(json_data)
   # file.write(",\n")   

    #clear db
   # dic  = {} 


file.write("\n]")
file.close()

filecsv.close()