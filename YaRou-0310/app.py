

# hash密碼
import bcrypt

# 解析 URL
from urllib import parse

# mysql connector
#from flask_mysqldb import MySQL, MySQLdb
import pymongo

# flask
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)

#app.config['MYSQL_HOST'] = '127.0.0.1'          # 登入ip
#app.config['MYSQL_USER'] = 'root'               # 登入帳號
#app.config['MYSQL_PASSWORD'] = 'root'           # 登入密碼
#app.config['MYSQL_DB'] = 'db'                   # 登入資料庫名稱
# app.config['MYSQL_PORT'] = '3306'             # Port號（預設就是3306)
#mysql = MySQL(app)




#mongodb_uri = "mongodb://ntust:jkjgff955DB@cluster0-shard-00-00.lclzf.mongodb.net:27017,cluster0-shard-00-01.lclzf.mongodb.net:27017,cluster0-shard-00-02.lclzf.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-6g59en-shard-0&authSource=admin&retryWrites=true&w=majority"
#myclient = pymongo.MongoClient(mongodb_uri)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["test"]
mycollection = mydb["personal_information"]

personal_information = {
    "name": "xyz",

}





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
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        result = mycollection.insert_many(name, email, hash_password)
        #cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
                   # (name, email, hash_password))
        #collection.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))


# 登入頁面
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        print("email:",email)
        password = request.form['password'].encode('utf-8')
        user = mycollection.find({"email":request.form['email']})
        #curl = collection.connection.cursor(pymongo.cursors.DictCursor)
        #curl.execute("SELECT * FROM users WHERE email=%s", [email])
        #user = curl.fetchone()
        #curl.close()
        if user == None:
            return "沒有這個帳號"
        if len(user) != 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "您的密碼錯誤"
    else:
        return render_template("login.html")


# 登出
@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


if __name__ == '__main__':
    app.secret_key = "This is a secret_key"
    app.run(debug=True, host='0.0.0.0', port=5000)


