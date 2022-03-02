from flask import Flask, render_template,request,redirect
import os,pymongo,datetime,googlemaps,requests,json,time
from bson.objectid import ObjectId
from sqlalchemy import true

mongodb_uri = "mongodb://ntust:jkjgff955DB@cluster0-shard-00-00.lclzf.mongodb.net:27017,cluster0-shard-00-01.lclzf.mongodb.net:27017,cluster0-shard-00-02.lclzf.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-6g59en-shard-0&authSource=admin&retryWrites=true&w=majority"
myclient = pymongo.MongoClient(mongodb_uri)
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["test"]
mycol = mydb["customer"]

# post = {"_id" : 90, "name" : "suck"}
# mycol.insert_one(post) //新增

# x = mycol.find_one()
# print(x) //查詢第一條


shoppingList=mydb["shoppingList"]
favor=mydb["favor"]
userid="abc"
# mydict = { "addr": "台北市大安區基隆路4段43號", "price": "60", "sellerID": "abcd" ,"size":"大" ,"safety":"有監視器" ,"strtime":datetime.datetime.strptime('2022-10-04 21:01:35', '%Y-%m-%d %H:%M:%S'),"endtime":datetime.datetime.strptime('2022-10-20 21:01:35', '%Y-%m-%d %H:%M:%S')}
# mycol.insert_one(mydict)
# mydict = { "addr": "台北市中正區重慶南路一段122號", "price": "60", "sellerID": "ccc" ,"size":"大" ,"safety":"有監視器" ,"strtime":datetime.datetime.strptime('2022-10-04 21:01:35', '%Y-%m-%d %H:%M:%S'),"endtime":datetime.datetime.strptime('2022-10-20 21:01:35', '%Y-%m-%d %H:%M:%S')}
# mycol.insert_one(mydict)

api_key ='AIzaSyBKDu39T3dK5YYZ3RPD9agDkbNX1HL7C4c'
# source = "台灣大學"
# dest = "台灣科技大學"
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
# payload={}
# headers = {}
# r = requests.request("GET",url + 'origins=' + source +
#                    '&destinations=' + dest +
#                    '&key=' + api_key ,headers=headers, data=payload)
# r = requests.get(url + 'origins=' + source +
#                    '&destinations=' + dest +
#                    '&key=' + api_key)
# u=url + 'origins=' + source + '&destinations=' + dest +'&key=' + api_key                   
# data = requests.get(u).json()
# rows=data['rows']
# elements=rows['elements']
# distance=elements['distance']

# print(distance['text'])


# importing googlemaps module
import googlemaps
  
# Requires API key
gmaps = googlemaps.Client(key=api_key)
  
# Requires cities name
# my_dist = gmaps.distance_matrix('台科大','台大',mode="walking")['rows'][0]['elements'][0]
  
# # Printing the result
# print(my_dist)
# d=my_dist['distance']
# d=d['text']
# t=my_dist['duration']
# t=t['text']
# print(d)
# print(t)

class product:
    def __init__(self,id,address, distance, walkingTime, price,size,safety):
        self.id=id
        self.addr=address
        self.dist=distance
        self.walking=walkingTime
        self.p=price
        self.s=size
        self.safe=safety

app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def search():
    items=[]
    if request.method == 'POST':
        address = request.form['address']
        strtime = request.form['strtime']
        t=strtime.replace('T',' ')
        t=datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        for x in mycol.find({'strtime':{'$lte':t},'endtime':{'$gte':t}}):
            try:
                my_dist = gmaps.distance_matrix(address,x['addr'],mode="walking")['rows'][0]['elements'][0]
            except:
                return "<h3>該地址不存在！</h3>"

            # print(my_dist)
            d=my_dist['distance']
            d=d['text']
            t=my_dist['duration']
            t=t['text']
            m=t.find("m")
            t=t[:m-1]
            index=t.find("h")
            if(index!=-1):
                min=t[(t.find("r")+2):]
                hour=t[:(index-1)]
                t=int(min)+int(hour)*60
            t=int(t)
            items.append(product(x['_id'],x['addr'],d,t,x['price'],x['size'],x['safety']))
            items.sort(key=lambda s: s.walking)
        return render_template("search.html", it = items,ad=address,t=strtime)
    else:
        localtime = time.localtime()
        d = time.strftime("%Y-%m-%d", localtime)
        t=d+"T"+time.strftime("%H:%M:%S", localtime)        
        return render_template("search.html",t=t)

@app.route('/search/favorites/<id>')
def addfavorites(id):
    # query = { "_id": ObjectId(id) }    
    result=favor.update_one({"product_id":id},{"$setOnInsert":{"user_id":userid,"product_id":id}},True)
    return redirect('/favorites')

@app.route('/favorites')
def myfavorites():
    myfavorites=[]
    for y in favor.find():
        product_id=ObjectId(y['product_id'])
        x=mycol.find_one({"_id":product_id})
        # print(product_id)
        myfavorites.append(product(x['_id'],x['addr'],0,0,x['price'],x['size'],x['safety']))
    return render_template("favorites.html", it = myfavorites)

@app.route('/favorites/delete/<id>')
def deletefavor(id):
    # print(id)
    favor.delete_one({"product_id":id})
    return redirect('/favorites')

@app.route('/order/<id>')
def order(id):
    result=shoppingList.update_one({"product_id":id},{"$setOnInsert":{"user_id":userid,"product_id":id}},True)  
    return redirect('/order')

@app.route('/order')
def orderList():
    myshoppingList=[]
    for s in shoppingList.find():
        product_id=ObjectId(s['product_id'])
        x=mycol.find_one({"_id":product_id})
        myshoppingList.append(product(x['_id'],x['addr'],0,0,x['price'],x['size'],x['safety']))
    return render_template("shoppingCart.html", it = myshoppingList)

@app.route('/order/delete/<id>')
def deleteOrder(id):
    # print(id)
    shoppingList.delete_one({"product_id":id})
    return redirect('/order')

port = int(os.getenv('PORT', 8080))    
if __name__ == '__main__' : 
    app.run(host='0.0.0.0', port=port, debug=true)