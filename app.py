from flask import Flask, render_template, request,redirect
from bson.objectid import ObjectId
import os, pymongo
from pymongo import database

  
# Replace your URL here. Don't forget to replace the password.
connection_url = "mongodb://ntust:jkjgff955DB@cluster0-shard-00-00.lclzf.mongodb.net:27017,cluster0-shard-00-01.lclzf.mongodb.net:27017,cluster0-shard-00-02.lclzf.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-6g59en-shard-0&authSource=admin&retryWrites=true&w=majority"
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)
  
# Database
# Database = client.get_database('test')
Database = client['test']
# Table
#SampleTable = Database.product
SampleTable = Database['product']

class product:
    def __init__(self,id,address,price,size,safety,strTime,endTime):
        self.id=id
        self.addr=address
        self.p=price
        self.si=size
        self.sa=safety
        self.strT=strTime
        self.endT=endTime


@app.route('/LaunchInfo', methods=['GET', 'POST'])
def LaunchSpaces():
    if request.method == 'POST':
        if request.values['send']=='Send':
            address = request.form['address']
            price = request.form['price']
            size = request.form['size']
            safety = request.form['safety']
            strTime = request.form['startTime']
            endTime = request.form['endTime']
            queryObject = {
                'addr': address,
                'price': price,
                'size': size,
                'safety': safety,
                'strtime': strTime,
                'endtime': endTime
            }
            SampleTable.insert_one(queryObject)
            return "Query inserted...!!!"
    return render_template('LaunchInfo.html')


@app.route('/MySpaces', methods=['GET', 'POST'])
def ShowMySpaces():
    space_list = SampleTable.find()
    return render_template("MySpaces.html", it = space_list)

@app.route('/MySpaces/delete/<id>', methods=['GET', 'POST'])
def deleteSpaces(id):           
    product_id=ObjectId(id)
    myquery = { "_id": product_id }
    SampleTable.delete_one(myquery)
    return redirect('/MySpaces')

@app.route('/EditMySpace/<id>', methods=['GET', 'POST'])
def editSpaces(id):             #Can't display the checked status of the radio buttons.
    #sizeIsBig = False
    #sizeIsMedium = False
    #sizeIsSmall = False
    product_id=ObjectId(id)
    myquery = { "_id": product_id }
    space = SampleTable.find_one(myquery)
    if request.method == 'POST':
        if request.values['send']=='Send':
            address = request.form['address']
            price = request.form['price']
            size = request.form['size']
            safety = request.form['safety']
            strTime = request.form['startTime']
            endTime = request.form['endTime']
            SampleTable.update_many(myquery, {"$set" : { "addr" : address, "price" : price, "size" : size, "safety" : safety, "strtime" : strTime, "endtime" : endTime}})
            return "Data updated!"
        #if request.values['size']=='big':
            #sizeIsBig = True
            #sizeIsMedium = False
            #sizeIsSmall = False
        #elif request.values['size']=='medium':
            #sizeIsBig = False
            #sizeIsMedium = True
            #sizeIsSmall = False
        #else:
            #sizeIsBig = False
            #sizeIsMedium = False
            #sizeIsSmall = True
    return render_template("EditMySpace.html", space = space)

port = int(os.getenv('PORT', 8080))    
if __name__ == '__main__' : 
    app.run(host='0.0.0.0', port=port, debug=True)