
# flask
from pickle import TRUE
from flask import Flask, render_template, request, redirect, url_for, session
from bson.objectid import ObjectId
import os, pymongo


app = Flask(__name__)



mongodb_uri = "mongodb://ntust:jkjgff955DB@cluster0-shard-00-00.lclzf.mongodb.net:27017,cluster0-shard-00-01.lclzf.mongodb.net:27017,cluster0-shard-00-02.lclzf.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-6g59en-shard-0&authSource=admin&retryWrites=true&w=majority"
myclient = pymongo.MongoClient(mongodb_uri)
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")

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
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        input = {
            'id': id,
            'name': name,
            'email': email,
            'password': password
        }
        mycollection.insert_one(input)
        session['id'] = request.form['id']
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect(url_for('home'))


# 登入頁面
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        inputId = request.form['id']
        inputPassword = request.form['password']

        userId = mycollection.find_one({'id': inputId})
        userPassword = mycollection.find_one({'password': inputPassword})
        if userId is None:
            return render_template("login.html", userId = userId)
            #return "沒有這個帳號"
        else:
            if userPassword:
                session['id'] = request.form['id']
                session['password'] = request.form['password']
                return render_template("home.html")
            else:
                userPasswordIncorrect = 1
                return render_template("login.html", userPasswordIncorrect = userPasswordIncorrect)
                #return "您的密碼錯誤"
    else:
        return render_template("login.html")


# 修改頁面
@app.route('/editUserData/<id>', methods=["GET", "POST"])
def editUserData(id):
    condition = {'id': session.get('id')}
    userData = mycollection.find_one(condition)
    if request.method == 'POST':
        if request.values['edit']=='Edit':
            id = request.form['id']
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            userData = {
                'id': id,
                'name': name,
                'email': email,
                'password': password
            }
            mycollection.update_many(condition, {"$set" : userData})
            returnValue = 1
            return render_template("home.html", returnValue = returnValue)
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


