from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory, render_template_string

from source.users.Users_db import SetupUserDB
from source.users.Users import Users_app
from source.areas.Areas_db import SetupAreasDB, AreasManagement
from source.areas.Areas import Areas_app
from config.KEY import key

app = Flask(__name__)
app.secret_key = key


from source.factory_mng.factory_db import SetupFactoryDB, ProductionRegistry
import json

class factory_management:
    def __init__(self,app):
        self.app = app
        SetupFactoryDB()
        self.production_registry =ProductionRegistry()

    def setup_routes(self):
        self.app.add_url_rule('/line_monitoring','line_monitoring',self.line_monitoring, methods=['GET','POST'])
        self.app.add_url_rule('/register_production','register_production', self.register_production, methods=['GET','POST'])
        self.app.add_url_rule('/current_production','current_production', self.current_production, methods=['GET','POST'])

    def line_monitoring(self):
        return render_template('factory_management/line_monitoring.html')
    
    def register_production(self):
        if request.method == 'POST':
            PartName = request.form['partname']
            NI = request.form['n_i']
            Operador = request.form['worker']

            self.production_registry.addOne(PartName,NI,Operador)
            self.current_production()
        return render_template('factory_management/register.html') 
    
    def current_production(self):
        current_data = self.production_registry.showAll()

        keys = ['id', 'pn', 'ni', 'operator']

        dict_list = [dict(zip(keys, tpl)) for tpl in current_data]

        j_str = json.dumps(dict_list)

        
        return j_str
       

    
    

class FlaskApp:

    def __init__(self):
        self.area_management = AreasManagement()

        self.app = app
        self.users = Users_app(self.app)
        self.areas = Areas_app(self.app)
        
        self.factory = factory_management(self.app)

        self.setup_routes()
        
    def setup_routes(self):
        self.users.setup_routes()
        self.areas.setup_routes()
        self.factory.setup_routes()
        
        self.app.add_url_rule('/','index',self.index)

  
    #pages
    def index(self):
        if 'username' not in session:
            return redirect(url_for('login'))
        else:
            areas = self.area_management.showAll()
            
            return render_template('index.html', username=session['username'], role=session['role'], areas=areas)



if __name__ == '__main__':
    
    print('\x1b[6;30;42m' +f"inicio"+'\x1b[0m')
    SetupUserDB()
    SetupAreasDB()
    flask_app = FlaskApp()
    flask_app.app.run(host='0.0.0.0', port=80, debug=True)