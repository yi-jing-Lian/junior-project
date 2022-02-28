from flask import Flask, render_template, request
import os, pymongo

  
# Replace your URL here. Don't forget to replace the password.
connection_url = "mongodb+srv://Test01:jQ!jqkzMR!g6NUS@test.w4pfg.mongodb.net/SalesDB?retryWrites=true&w=majority"
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)
  
# Database
# Database = client.get_database('SalesDB')
Database = client['SalesDB']
# Table
#SampleTable = Database.Spaces
SampleTable = Database['Spaces']

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
def LaunchInfo():
    if request.method == 'POST':
        if request.values['send']=='Send':
            address = request.form['address']
            price = request.form['price']
            size = request.form['size']
            safety = request.form['safety']
            strTime = request.form['startTime']
            endTime = request.form['endTime']
            queryObject = {
                'address': address,
                'price': price,
                'size': size,
                'safety': safety,
                'startTime': strTime,
                'endTime': endTime
            }
            SampleTable.insert_one(queryObject)
            return "Query inserted...!!!"
    return render_template('LaunchInfo.html')


port = int(os.getenv('PORT', 8080))    
if __name__ == '__main__' : 
    app.run(host='0.0.0.0', port=port, debug=True)