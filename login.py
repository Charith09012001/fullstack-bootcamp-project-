from flask import Blueprint
from flask import request,render_template,url_for,redirect,flash

bp = Blueprint("login","login")

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
        cur.execute("select id from users where usermail=%s",(username,))
        uid=cur.fetchone()[0]
        return redirect(url_for("todo.todolist",uid=uid))
    flash(f"Invalid username or Password {pass_check}")
    return redirect(url_for("login.loginform"))
    

