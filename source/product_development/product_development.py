from flask import session, render_template, request, url_for,redirect,jsonify


class Product_development:
    def __init__(self,app):
        self.app = app
        
    def setup_routes(self):
        self.app.add_url_rule('/desenvolvimento','desenvolvimento',self.index, methods=['GET','POST'])
        self.app.add_url_rule('/add_project','add_project',self.add_project, methods=['GET','POST'])
        self.app.add_url_rule('/api/projects','projects',self.projects, methods=['GET','POST'])
        
    def index(self):
        session['current_page']= 'Product_dev'
        return render_template('product_development/index.html', current_page=session['current_page'])
    def add_project(self):
        session['current_page']= 'add_project'

        return render_template('product_development/add.html', current_page=session['current_page'])
    
    def projects(self):
        lista = [
                    {
                        "id": 1,
                        "nome": "Projeto A",
                        "descrição": "Descrição do Projeto A",
                        "status": "Em andamento"
                    },
                    {
                        "id": 2,
                        "nome": "Projeto B",
                        "descrição": "Descrição do Projeto B",
                        "status": "Não iniciado"
                    },
                    {
                        "id": 3,
                        "nome": "Projeto C",
                        "descrição": "Descrição do Projeto C",
                        "status": "Concluído"
                    }
                ]
        json_file = jsonify(lista)
        return json_file
