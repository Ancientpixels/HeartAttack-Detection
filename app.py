from flask import Flask, render_template, request
import pymysql as pms
import pickle
import os

mod = pickle.load(open('model.pkl','rb'))

conn = pms.connect(host="host.docker.internal", 
                   port=3006,
                   user="root",
                   password="Fa$T@NdFur1ou$7",
                   db="login")
cur = conn.cursor()
app = Flask(__name__)

@app.route("/")
def start():
    return render_template("index.html")
    
@app.route("/login", methods=['post'])
def login():
    u=request.form["uname"]
    p=request.form["pswd"]
    d="select * from credentials where username=%s and password=%s"
    cur.execute(d,(u,p))
    r=cur.fetchall()
    if (not r)==False:
        return render_template("model.html")        
    else:
        return render_template("index.html", error="Invalid Login")
    
@app.route("/class", methods=["post"])
def classif():
    age= int(request.form['age'])
    sex= int(request.form['sex'])
    cp= int(request.form['cp'])
    trtbps= int(request.form['trtbps'])
    chol= int(request.form['chol'])
    fbs= int(request.form['fbs'])
    rest_ecg= int(request.form['rest_ecg'])
    thalach= int(request.form['thalach'])
    exang= int(request.form['exang'])
    oldpeak= float(request.form['oldpeak'])
    slp= int(request.form['slp'])
    ca= int(request.form['ca'])
    thall=int(request.form["thall"])
    pred = mod.predict([[age,sex,cp,trtbps,chol,fbs,rest_ecg,thalach,exang,oldpeak,slp,ca,thall]])[0]
    print(pred)
    if(pred==1):
        result="YOU MAY SUFFER HEART ATTACK"
        return render_template("success.html",data=result)
    else:
        result="YOU HAVE LESS CHANCES OF HEART ATTACK"
        return render_template("success.html",data=result)

    
if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)