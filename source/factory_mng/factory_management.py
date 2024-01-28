from source.factory_mng.factory_db import SetupFactoryDB, ProductionRegistry
from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory, render_template_string
import json

class factory_management:
    def __init__(self,app):
        self.app = app
        SetupFactoryDB()
        self.production_registry =ProductionRegistry()

    def setup_routes(self):
        self.app.add_url_rule('/producao','producao',self.index, methods=['GET','POST'])
        self.app.add_url_rule('/line_monitoring','line_monitoring',self.line_monitoring, methods=['GET','POST'])
        self.app.add_url_rule('/register_production','register_production', self.register_production, methods=['GET','POST'])
        self.app.add_url_rule('/current_production','current_production', self.current_production, methods=['GET','POST'])

    def index(self):
        session['current_page']= 'Produção'
        return render_template('factory_management/index.html', current_page=session['current_page'])
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
       