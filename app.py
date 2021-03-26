import os
import psycopg2
from flask import Flask, render_template, redirect,request,session
app = Flask(__name__)
app.secret_key = "test"
conn = psycopg2.connect(
   database="postgres", user='devesh', password='3349696', host='127.0.0.1', port= '5432'
)

cursor = conn.cursor()
cursor.execute("select * from users")
data = []
products = []
data = cursor.fetchall()
cursor.execute("select * from products")
products = cursor.fetchall()
print(products)
print(data)

@app.route("/")
def index():
    return render_template('landing.html')

@app.route("/sign-log.html", methods = ["GET", "POST"])
def signUp():
    return render_template('sign-log.html')

@app.route('/settings.html')
def settings():
    if (session["userName"] != "Guest"):
            return render_template('settings.html', user = session["userName"],logout = "logout" ,link = "/homePage_logout")
    elif (session["userName"] == "Guest"):
            return render_template('settings.html' , logout = "Sign up", user="Guest",link = "/sign-log.html") 

@app.route("/homePage_logout")
def logout():
    session.clear()
    session["userName"] = "Guest"
    return redirect("/homePage.html", code=302)
@app.route("/itemSubmit.html", methods=["POST"])
def sellingPage():
     name = request.form.get('item-name')
     price = request.form.get('item-price')
     description = request.form.get('item-discription')
     print(name, price, description)
     cursor.execute("INSERT INTO products (prouctname, price, description) VALUES (%s , %s , %s)"  , (name, price, description))
     conn.commit()
     cursor.execute("select * from products")
     products = cursor.fetchall()
     print(cursor.fetchall())
     return redirect("/homePage.html", code=302)
@app.route("/selling")
def selling():
    return render_template("sellingPage.html")
@app.route("/homePage.html" ,methods=["POST","GET","POST"])
def home():
    if request.method == "POST":
        username = request.form.get('sign-username')
        email = request.form.get('sign-email')
        password = request.form.get('sign-password')
        session["userName"] = username
        print(username, email, password)
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s , %s , %s)"  , (username, email, password))
        conn.commit()
        cursor.execute("select * from users")
        print(cursor.fetchall())
        if "userName" in session:
            if (session["userName"] != "Guest"):
                return render_template('homePage.html', user = session["userName"],logout = "logout" ,link = "/homePage_logout", products = products  )
            elif (session["userName"] == "Guest"):
                return render_template('homePage.html' , logout = "Sign up", user="Guest",link = "/sign-log.html", products = products)
    else:
        if "userName" in session:
            if (session["userName"] != "Guest"):
                return render_template('homePage.html', user = session["userName"],logout = "logout" ,link = "/homePage_logout", products = products)
            elif (session["userName"] == "Guest"):
                return render_template('homePage.html' , logout = "Sign up", user="Guest",link = "/sign-log.html", products = products)

if  __name__=="__main__":
    app.run(debug=True)