from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory, render_template_string

from source.users.Users_db import SetupUserDB
from source.users.Users import Users_app
from source.areas.Areas_db import SetupAreasDB, AreasManagement
from source.areas.Areas import Areas_app
from config.KEY import key
from source.factory_mng.factory_management import factory_management
from source.product_development.product_development import Product_development

app = Flask(__name__)
app.secret_key = key



class FlaskApp:

    def __init__(self):
        self.area_management = AreasManagement()
        self.app = app
        self.users = Users_app(self.app)
        self.areas = Areas_app(self.app)
        self.factory = factory_management(self.app)
        self.product_dev = Product_development(self.app)

        self.setup_routes()
        
    def setup_routes(self):
        self.users.setup_routes()
        self.areas.setup_routes()
        self.factory.setup_routes()
        self.product_dev.setup_routes()

        
        self.app.add_url_rule('/','index',self.index)
        self.app.add_url_rule('/configuracoes','configuracoes', self.configuration_panel)

  
    #pages
    def index(self):
        if 'username' not in session:
            return redirect(url_for('login'))
        else:
            session['current_page']= 'Index'
            
            return render_template('index.html', username=session['username'], role=session['role'], current_page= session['current_page'])

    def configuration_panel(self):
        session['current_page']= 'Configuration Panel'
        return render_template('config_panel.html', username=session['username'], current_page= session['current_page'])


if __name__ == '__main__':
    
    print('\x1b[6;30;42m' +f"inicio"+'\x1b[0m')
    SetupUserDB()
    SetupAreasDB()
    flask_app = FlaskApp()
    flask_app.app.run(host='0.0.0.0', port=80, debug=True)