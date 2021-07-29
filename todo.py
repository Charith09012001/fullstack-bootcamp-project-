from flask import Blueprint
from flask import render_template,request,url_for,redirect,flash

from . import db

bp = Blueprint("todo","todo",url_prefix="/todo")

@bp.route("/<uid>")
def todolist(uid):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("select t.id,t.task_name,t.added_on,t.due_datetime,ts.name from tasks t,task_status ts where user_id=%s and ts.id=t.status",(uid,))
    tasks=cur.fetchall()
    conn.commit()
    cur.close()
    return render_template("todolist.html",tasks=tasks,uid=uid)
    
    
    
@bp.route("/<uid>/addTask",methods=['GET','POST'])
def addtask(uid):
    conn = db.get_db()
    cur = conn.cursor()
    if request.method=='GET':
        return render_template("addtask.html")
    elif request.method=='POST':
        task_name=request.form.get('task_name')
        task_description=request.form.get("task_description")
        added_on=request.form.get("add_date")
        due_date=request.form.get("due_date")
        status='1'
        cur.execute("insert into tasks (user_id,task_name,task_description,added_on,due_datetime,status) values(%s,%s,%s,%s,%s,%s)",(uid,task_name,task_description,added_on,due_date,status))
        conn.commit()
        flash("added one task")
        return render_template("addtask.html",uid=uid)
    
    
    

