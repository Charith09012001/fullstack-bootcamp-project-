from flask import Blueprint
from flask import render_template,request,url_for,redirect,flash
import datetime
from . import db

bp = Blueprint("todo","todo",url_prefix="/todo")


def diff_dates(a,b):
    obj = datetime.datetime.strptime(a,"%Y-%m-%d %H:%M:%S")
    if b > obj:
        diff = b - obj
        dur_in_sec = diff.total_seconds()
        days = int(dur_in_sec/86400)
        hours = int((dur_in_sec % 86400)/3600)
        minutes = int((((dur_in_sec % 86400) % 3600)/60))
        seconds = int(((dur_in_sec % 86400) % 3600) %60)
        return f"Overdue by {days} days,{hours} hours,{minutes} minutes and {seconds} seconds"
    elif obj > b:
        diff = obj - b
        dur_in_sec = diff.total_seconds()
        days = int(dur_in_sec/86400)
        hours = int((dur_in_sec % 86400)/3600)
        minutes = int((((dur_in_sec % 86400) % 3600)/60))
        seconds = int(((dur_in_sec % 86400) % 3600) %60)
        return f"Due, Time remaining: {days} days,{hours} hours,{minutes} minutes and {seconds} seconds"



@bp.route("/<uid>")
def todolist(uid):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("select * from task_status")
    statuses=cur.fetchall()
    today = datetime.date.today()
    now = datetime.datetime.now()
    time = now.time()
    cur.execute("select date_time from tasks where user_id=%s",(uid,))
    for x in cur.fetchall():
        diff = diff_dates(x[0],now)
        cur.execute("update tasks set due_status=%s where date_time = %s",(diff,x))
        conn.commit()
    cur.execute("select count(*) from tasks where user_id=%s and due_date=%s",(uid,today))
    tasks_due_today = cur.fetchone()[0]
    cur.execute("select count(*) from tasks where user_id=%s and due_date<%s",(uid,today))
    due_tasks_1 = cur.fetchone()[0]
    cur.execute("select count(*) from tasks where user_id=%s and due_date=%s and due_time<%s",(uid,today,time))
    due_tasks_2 = cur.fetchone()[0]
    total_due = due_tasks_1 + due_tasks_2  
    cur.execute("select t.id,t.task_name,t.added_on,t.due_date,t.due_time,ts.name,t.due_status from tasks t,task_status ts where user_id=%s and ts.id=t.status",(uid,))
    tasks=cur.fetchall()  
    
    
    cur.close()
    return render_template("todolist.html",tasks=tasks,uid=uid,statuses=statuses,tasks_due_today=tasks_due_today,total_due=total_due)
    
    
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
        date_time=str(datetime.datetime.strptime(due_date+' '+due_time,"%Y-%m-%d %H:%M"))
        status='1'
        now=datetime.datetime.now()
        cur.execute("insert into tasks (user_id,task_name,task_description,added_on,due_date,due_time,date_time,status,due_status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(uid,task_name,task_description,added_on,due_date,due_time,date_time,status,"due"))
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
       
        
        
         
    
     
    

