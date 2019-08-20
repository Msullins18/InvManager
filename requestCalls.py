import requests, json
import Product

URL = "http://marcus5150.pythonanywhere.com/product"
productList = []

def getProducts():
    global productList
    productList = []
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        
        for i in data:
            productList.append(Product.Product(i.get("id"),i.get("name"),i.get("description"),i.get("price"),i.get("qty")))
            # print(str(i.get("id")) +" "+ i.get("name") + " " + i.get("description") +" "+ str(i.get("price")) +" "+ str(i.get("qty")))
        return productList

def getProductsOffline():
    return productList

def postProduct(name,description,price,qty):
    r=requests.post(URL, json={
    'name':name,
    'description':description,
    'price':price,
    'qty':qty
    })
    return r

def putProduct(id,name,description,price,qty):
    r=requests.put(URL+ "/"+str(id), json={
    'name':name,
    'description':description,
    'price':price,
    'qty':qty
    })
    return r

def deleteProduct(id):
    r = requests.delete(URL+ "/"+str(id))
    return r

def deleteProducts():
    r = requests.delete("http://marcus5150.pythonanywhere.com/product/delete")
    return r

def postCSV():
    url="http://marcus5150.pythonanywhere.com/csv"
    headers = {"Content-Type":"application/json"}
    r = requests.post(url, headers=headers,data=open('products.json', 'rb'))
    if r.status_code != 200:
        print('Status:', r.status_code, 'Headers:', r.headers)