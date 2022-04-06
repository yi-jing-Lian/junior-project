
# hash密碼
import bcrypt

# flask
from pickle import TRUE
from flask import Flask, render_template, request, redirect, url_for, session
import os, pymongo


from flask_mail import Mail
from flask_mail import Message
import smtplib
from random import randint
import random


app = Flask(__name__)
#app.config.update(
    #  gmail的設置
#    MAIL_SERVER='smtp.gmail.com',
#    MAIL_PROT=465,
#    MAIL_USE_TLS=True,
#    MAIL_USERNAME='shanon891101@gmail.com',
#    MAIL_PASSWORD='555555522'
#)
mail = Mail(app)


mongodb_uri = "mongodb://ntust:jkjgff955DB@cluster0-shard-00-00.lclzf.mongodb.net:27017,cluster0-shard-00-01.lclzf.mongodb.net:27017,cluster0-shard-00-02.lclzf.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-6g59en-shard-0&authSource=admin&retryWrites=true&w=majority"
myclient = pymongo.MongoClient(mongodb_uri)
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['test']
mycollection = mydb['personal_information']

class personal_information:
    def __init__(self,id,name,phone,email,password):
        self.id=id
        self.name=name
        self.phone=phone
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
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        
        encrypt_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        input = {
            'id': id,
            'name': name,
            'phone': phone,
            'email': email,
            'password': encrypt_password,
        }
        mycollection.insert_one(input)
        session['id'] = request.form['id']
        session['name'] = request.form['name']
        session['phone'] = request.form['phone']
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
        
        if userId is None:
            return render_template("login.html", userId = userId)
            #return "沒有這個帳號"
        
        if len(userId) != 0:
            if bcrypt.checkpw(inputPassword.encode('utf-8'), userId['password']):
                session['id'] = request.form['id']
                session['password'] = request.form['password']
                return render_template("home.html")
            else:
                userPasswordIncorrect = 1
                return render_template("login.html", userPasswordIncorrect = userPasswordIncorrect)
                #return "您的密碼錯誤"
    else:
        return render_template("login.html")



# 寄驗證碼(Send mail by Gmail with TLS)
@app.route("/message/<email>")
def index(email):
    smtp=smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login("shanon891101@gmail.com", "aivviczwdizjzfpt")
    from_addr = "shanon891101@gmail.com"
    to_addr = email
    random_code = get_random_code()
    msg="Subject:Ask to reset password\nYour verification code is %s" % random_code
    status=smtp.sendmail(from_addr, to_addr, msg)
    if status=={}:
        return render_template("resetPassword.html", random_code = random_code)
        #return "郵件傳送成功!"
    else:
        return "郵件傳送失敗!"
    smtp.quit()

def get_random_code():
    nums_str = ''                      # 建立 nums_str 變數，內容為空字串
    for i in range(6):                 # 重複六次的 for 迴圈
        nums = random.randint(0, 9)      # 產生 0～9 的隨機整數
        nums_str = nums_str + str(nums)
    return nums_str



# 忘記密碼頁面
@app.route('/forgetPassword', methods=["GET", "POST"])
def forgetPassword():
    if request.method == 'GET':
        return render_template("forgetPassword.html")
    else:
        email = request.form['email']
        session['email'] = request.form['email']
        return index(email)
        #return render_template('message.html', email = email)
    

# 重設密碼頁面
@app.route('/resetPassword/<random_code>/<email>', methods=["GET", "POST"])
def resetPassword(random_code,email):
    condition = {'email': session.get('email')}
    newPassword = mycollection.find_one(condition)
    if request.method == 'POST':
        if request.values['edit']=='Edit':
            verificationCode = request.form['verificationCode']
            password = request.form['password']
            encrypt_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            if verificationCode == random_code:
                newPassword = {
                    'email': email,
                    'password': encrypt_password,
                }
                mycollection.update_many(condition, {"$set" : newPassword})
            return render_template("login.html")
    return render_template("resetPassword.html", newPassword = newPassword)



# 修改頁面
@app.route('/editUserData/<id>', methods=["GET", "POST"])
def editUserData(id):
    condition = {'id': session.get('id')}
    userData = mycollection.find_one(condition)
    if request.method == 'POST':
        if request.values['edit']=='Edit':
            id = request.form['id']
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            password = request.form['password']
            
            encrypt_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            userData = {
                'id': id,
                'name': name,
                'phone': phone,
                'email': email,
                'password': encrypt_password,
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









