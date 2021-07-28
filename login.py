from flask import Blueprint
from flask import request,render_template,url_for,redirect,flash

bp = Blueprint("login","login",url_prefix="/login")

from . import db

@bp.route("/",methods=['GET','POST'])
def loginform():
    return render_template('login.html')
        
@bp.route("/validate",methods=['GET','POST'])
def validate():
    username = request.form["usermail"]
    password = request.form["password"]
    try:
        from . import db
        conn=db.get_db()
        cur=conn.cursor()
        cur.execute("select pass from users where usermail=%s",(username,))
        pass_check = cur.fetchone()[0]
    except:
        flash("user not defined. Please register first")
        return redirect(url_for("register.register"))
    if request.method=='POST' and password ==pass_check:
        flash("You are logged in")
        return redirect(url_for("frontpage"))
    flash(f"Invalid username or Password {pass_check}")
    return redirect(url_for("login.loginform"))
    

