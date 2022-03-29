from flask import Flask, render_template, request,redirect
from bson.objectid import ObjectId
import os, pymongo
from pymongo import database

  
# Replace your URL here. Don't forget to replace the password.
connection_url = "mongodb://ntust:jkjgff955DB@cluster0-shard-00-00.lclzf.mongodb.net:27017,cluster0-shard-00-01.lclzf.mongodb.net:27017,cluster0-shard-00-02.lclzf.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-6g59en-shard-0&authSource=admin&retryWrites=true&w=majority"
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)
  
# Database
Database = client['test']
# Table
SampleTable = Database['product']

class product:
    def __init__(self,id,address,price,size,camera,guard,lockable,moreSecurityDescription,strTime,endTime):
        self.id=id
        self.addr=address
        self.p=price
        self.si=size
        self.ca=camera
        self.gu=guard
        self.lo=lockable
        self.msd=moreSecurityDescription
        self.strT=strTime
        self.endT=endTime


@app.route('/LaunchInfo', methods=['GET', 'POST'])
def LaunchSpaces():
    if request.method == 'POST':
        if request.values['send']=='Send':
            address = request.form['address'].replace(" ", "")
            price = request.form['price']
            size = request.form['size']
            camera = request.form.get('camera')
            guard = request.form.get('guard')
            lockable = request.form.get('lockable')
            cameraBol = optionIsChecked(camera)
            guardBol = optionIsChecked(guard)
            lockableBol = optionIsChecked(lockable)
            moreSecurityDescription = request.form['moreSecurityDescription']
            strTime = request.form['startTime']
            endTime = request.form['endTime']
            note = request.form['note']
            queryObject = {
                'addr': address,
                'price': price,
                'size': size,
                'camera': cameraBol,
                'guard': guardBol,
                'lockable': lockableBol,
                'moreSecurityDescription': moreSecurityDescription,
                'strtime': strTime,
                'endtime': endTime,
                'note': note
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
def editSpaces(id):
    product_id=ObjectId(id)
    myquery = { "_id": product_id }
    space = SampleTable.find_one(myquery)
    if request.method == 'POST':
        if request.values['send']=='Send':
            address = request.form['address'].replace(" ", "")
            price = request.form['price']
            size = request.form['size']
            camera = request.form.get('camera')
            guard = request.form.get('guard')
            lockable = request.form.get('lockable')
            cameraBol = optionIsChecked(camera)
            guardBol = optionIsChecked(guard)
            lockableBol = optionIsChecked(lockable)
            moreSecurityDescription = request.form['moreSecurityDescription']
            strTime = request.form['startTime']
            endTime = request.form['endTime']
            note = request.form['note']
            SampleTable.update_many(myquery, {"$set" : { "addr" : address, "price" : price, "size" : size, 'camera' : cameraBol, 'guard' : guardBol, 'lockable' : lockableBol, 'moreSecurityDescription' : moreSecurityDescription, "strtime" : strTime, "endtime" : endTime, 'note' : note}})
            return "Data updated!"
    return render_template("EditMySpace.html", space = space)

def optionIsChecked(optionStr):        #Check whether the security option is checked.
    if not optionStr:
        return False
    else:
        return True

port = int(os.getenv('PORT', 8080))    
if __name__ == '__main__' : 
    app.run(host='0.0.0.0', port=port, debug=True)