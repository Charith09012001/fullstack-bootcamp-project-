from flask import Blueprint
from flask import request,render_template

bp = Blueprint("login","login",url_prefix="/login")

@bp.route("/",methods=['GET','POST'])
def loginform():
    if request.method=='GET':
        return render_template('login.html')
