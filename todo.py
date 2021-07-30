from flask import Blueprint
from flask import render_template,request,url_for,redirect,flash
import datetime
from . import db

bp = Blueprint("todo","todo",url_prefix="/todo")

@bp.route("/<uid>")
def todolist(uid):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("select t.id,t.task_name,t.added_on,t.due_date,t.due_time,ts.name from tasks t,task_status ts where user_id=%s and ts.id=t.status",(uid,))
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
        task_description=request.form.get("task_desc")
        added_on=datetime.date.today()
        due_date=request.form.get("due_date")
        due_time=request.form.get("due_time")
        status='1'
        cur.execute("insert into tasks (user_id,task_name,task_description,added_on,due_date,due_time,status) values(%s,%s,%s,%s,%s,%s,%s)",(uid,task_name,task_description,added_on,due_date,due_time,status))
        conn.commit()
        cur.close()
        flash("added one task")
        return render_template("addtask.html",uid=uid)

@bp.route("/<uid>/delete/<tid>")
def DelTask(uid,tid):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("delete from tasks where user_id=%s and id=%s",(uid,tid))
    conn.commit()
    cur.close()
    flash("deleted 1 task")
    return redirect(url_for("todo.todolist",uid=uid))

@bp.route("/<uid>/edit/<tid>",methods=['GET','POST'])
def EditTask(uid,tid):
    conn=db.get_db()
    cur=conn.cursor()
    cur.execute("select t.task_name,t.task_description,t.due_date,t.due_time,ts.name from tasks t,task_status ts where t.user_id=%s and t.id=%s and t.status=ts.id",(uid,tid))
    task_name,task_desc,due_date,due_time,status=cur.fetchall()[0]
    
    if request.method=='GET':
        cur.execute("select id,name from task_status")
        statuses = cur.fetchall()
        return render_template("edittask.html",uid=uid,tid=tid,task_name=task_name,task_desc=task_desc,due_date=due_date,due_time=due_time,status=status,statuses=statuses)
    if request.method=='POST':
        task_name=request.form.get("task_name")
        task_desc=request.form.get("task_desc")
        status=request.form.get("status")
        due_date=request.form.get("due_date")
        due_time=request.form.get("due_time")
        cur.execute("update tasks set task_name=%s,task_description=%s,due_date=%s,due_time=%s,status=%s where id=%s and user_id=%s",(task_name,task_desc,due_date,due_time,status,tid,uid))
        conn.commit()
        cur.close()
        flash("edited successfully")
        return redirect(url_for("todo.todolist",uid=uid),302)
       
        
        
         
    
     
    

