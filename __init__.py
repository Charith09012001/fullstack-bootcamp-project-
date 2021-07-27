from flask import Flask,render_template




def create_app():
    app = Flask("ToDo Manager",template_folder="Project/templates")
    
    app.config.from_mapping(
    DATABASE = 'todo'
    )
    
    @app.route("/")
    def frontpage():
        return "hi"
        
    from . import login
    app.register_blueprint(login.bp)
    
    return app
