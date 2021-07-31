from flask import Blueprint,url_for,redirect
from flask import render_template,request,flash
from uuid import uuid4

bp = Blueprint("register","register")
from . import db

@bp.route("/",methods=['GET','POST'])
def register():
    
    conn = db.get_db()
    cur = conn.cursor()
    if request.method=='GET':
        return render_template("register.html")
    elif request.method == 'POST':
        user_mail= request.form.get("user_email")
        username = request.form.get('user_name')
        password = request.form.get('pass')
        uuid = str(uuid4())
        cur.execute("INSERT INTO users(id,usermail,username,pass) VALUES(%s,%s,%s,%s)",(uuid,user_mail,username,password))
        conn.commit()
        flash("You Have registered. Log in to continue")
        return redirect(url_for("login.loginform"),302)
        
        
