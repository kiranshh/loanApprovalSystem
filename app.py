from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import pickle
import numpy as np
import pandas as pd
import json
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'loan'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
model = pickle.load(open('model.pkl', 'rb'))
data={}
@app.route('/')
def index():
    return render_template('login.html')
@app.route('/home')
def home():
    if session.get('log') ==True:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        name = request.form.get('name')
        email = request.form.get('emailup')
        password = request.form.get('passwordup')
        print(name)
        print(password)
        print(email)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)", (name, email, password,))
        mysql.connection.commit()
        session['name'] = request.form.get('name')
        session['email'] = request.form.get('email')
        return redirect(url_for('index'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('password')
        if len(email) == 0:
            e="*Enter EmailID"
            return render_template("login.html",error=e)
        if len(password) == 0:
            e="*Enter Password"
            return render_template("login.html",error=e)

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()
        if email == "admin@gmail.com" and password == user["password"]:
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM data ")
            user = curl.fetchall()
            curl.close()
            return render_template("admin.html",users=user)
        if user!=None:
            if password == user["password"]:
                session['email'] = user['email']
                session['log']=True
                return redirect("/home")
            else:
                e="*Error password or email not match"
                return render_template("login.html",error=e)
        else:
            e="*Error user not found"
            return render_template("login.html",error=e)
    else:
        return render_template("login.html")

@app.route('/filter', methods=["GET", "POST"])
def filter():
    f=request.form.get('s')
    print(f)
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM data having label=%s",(f,))
    user = curl.fetchall()
    curl.close()
    return render_template("admin.html", users=user)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")
@app.route('/admin')
def admin():
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM data ")
    user = curl.fetchall()
    curl.close()
    return render_template("admin.html", users=user)


@app.route('/chart')
def chart():
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT label,count(*) FROM data group by label")
    user = curl.fetchall()
    curl.close()
    data["0"]=user[0]['count(*)']
    data["1"] = user[1]['count(*)']

    return render_template("chart.html",abc=json.dumps(user))

@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        int_features = [[int(x) for x in request.form.values()]]
        final = np.array(int_features)
        print(final)

        col = np.array(['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                        'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                        'Loan_Amount_Term', 'Credit_History', 'Property_Area'])
        email = session['email']
        df = pd.DataFrame(final, columns=col)
        prediction = model.predict(df)
        Gender = request.form.get('Gender')
        Married = request.form.get('Married')
        Dependents = request.form.get('Dependents')
        Education = request.form.get('Education')
        SelfEmployed = request.form.get('SelfEmployed')
        ApplicantIncome = request.form.get('ApplicantIncome')
        CoapplicantIncome = request.form.get('CoapplicantIncome')
        LoanAmount = request.form.get('LoanAmount')
        LoanAmountTerm = request.form.get('LoanAmountTerm')
        CreditHistory = request.form.get('CreditHistory')
        PropertyArea = request.form.get('PropertyArea')
        cur = mysql.connection.cursor()

        if prediction == 1:
            cur.execute(
                "INSERT INTO data (Email,Gender,Married,Dependents,Education,SelfEmployed,ApplicantIncome,CoapplicantIncome,LoanAmount,LoanAmountTerm,CreditHistory,PropertyArea,Label) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (email, Gender, Married, Dependents, Education, SelfEmployed, ApplicantIncome, CoapplicantIncome,
                 LoanAmount,
                 LoanAmountTerm, CreditHistory, PropertyArea, 1,))
            mysql.connection.commit()
            return render_template('index.html', pred='Loan can be approved')
        else:
            cur.execute(
                "INSERT INTO data (Email,Gender,Married,Dependents,Education,SelfEmployed,ApplicantIncome,CoapplicantIncome,LoanAmount,LoanAmountTerm,CreditHistory,PropertyArea,Label) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (email, Gender, Married, Dependents, Education, SelfEmployed, ApplicantIncome, CoapplicantIncome,
                 LoanAmount,
                 LoanAmountTerm, CreditHistory, PropertyArea, 0,))
            mysql.connection.commit()
            return render_template('index.html', pred='Loan cannot be approved')

if __name__ == '__main__':
    app.secret_key = "localpred"
    app.run(debug=True)
