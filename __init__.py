from flask import Flask,render_template,url_for,flash




def create_app():
    app = Flask("ToDo Manager",template_folder="Project/templates")
    
    app.config.from_mapping(
    DATABASE = 'todo'
    )
    app.secret_key="123"
    from . import login
    app.register_blueprint(login.bp)
    
    from . import db
    db.init_app(app)
    
    from . import register
    app.register_blueprint(register.bp)   
    
    from . import todo
    app.register_blueprint(todo.bp)
    
    
        
    
    
    return app
