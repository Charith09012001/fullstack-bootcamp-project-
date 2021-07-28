from flask import Blueprint,url_for,redirect
from flask import render_template,request,flash

bp = Blueprint("register","register",url_prefix="/register")
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
        cur.execute("INSERT INTO users(usermail,username,pass) VALUES(%s,%s,%s)",(user_mail,username,password))
        conn.commit()
        flash("You Have registered. Log in to continue")
        return redirect(url_for("login.loginform"),302)
        
        
