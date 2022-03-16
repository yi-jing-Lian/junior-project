
# flask
from flask import Flask, render_template, request, redirect, url_for, session
from bson.objectid import ObjectId
import os, pymongo


app = Flask(__name__)



#mongodb_uri = "mongodb://ntust:jkjgff955DB@cluster0-shard-00-00.lclzf.mongodb.net:27017,cluster0-shard-00-01.lclzf.mongodb.net:27017,cluster0-shard-00-02.lclzf.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-6g59en-shard-0&authSource=admin&retryWrites=true&w=majority"
#myclient = pymongo.MongoClient(mongodb_uri)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['test']
mycollection = mydb['personal_information']

class personal_information:
    def __init__(self,id,name,email,password):
        self.id=id
        self.name=name
        self.email=email
        self.password=password







# 主頁
@app.route('/')
def home():
    return render_template("home.html")

# 註冊頁面
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        #password = request.form['password'].encode('utf-8')
        input = {
            'name': name,
            'email': email,
            'password': password
        }
        mycollection.insert_one(input)
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect(url_for('home'))


# 登入頁面
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #password = request.form['password'].encode('utf-8')

        userEmail = mycollection.find({'email': email})
        userPassword = mycollection.find({'password': password})
        if userEmail == None:
            return "沒有這個帳號"
        if userEmail:
            if userPassword:
                session['email'] = request.form['email']
                session['password'] = request.form['password']
                return render_template("home.html")
            else:
                return "您的密碼錯誤"
    else:
        return render_template("login.html")


# 修改頁面
@app.route('/editUserData', methods=["GET", "POST"])
def editUserData():
    personal_information_id = ObjectId(id)
    condition = { "_id": personal_information_id }
    #condition = {'email': email}
    userData = mycollection.find_one(condition)
    if request.method == 'POST':
        if request.values['edit']=='Edit':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            #password = request.form['password'].encode('utf-8')
            userData = {
                'name': name,
                'email': email,
                'password': password
            }
            mycollection.update_many(condition, {"$set" : userData})
            return "資料已更新！"
            #session['name'] = request.form['name']
            #session['email'] = request.form['email']
            #session['password'] = request.form['password']
    return render_template("editUserData.html", userData = userData)
        


# 登出
@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


port = int(os.getenv('PORT', 8080)) 
if __name__ == '__main__':
    app.secret_key = "This is a secret_key"
    app.run(host='0.0.0.0', port=port , debug=True)


