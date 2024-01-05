from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory
import sqlite3
from os import rename , remove, makedirs, getcwd
from config.KEY import key

app = Flask(__name__)
app.secret_key = key


class SetupUserDB():
    def __init__(self):
        self.montaTabelas()
        
    def conecta_bd(self):
        self.conn = sqlite3.connect("DB/Users.db")
        self.cursor = self.conn.cursor(); 
        #print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); 
        #print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela de de usuarios
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS Users (
                    ID INTEGER PRIMARY KEY,
                    Username CHAR(40),
                    Password CHAR(40),
                    Role CHAR(40)
                );
            """)
        self.conn.commit(); 
        #print("Banco de dados criado")
        self.desconecta_bd()

class UserManagement(SetupUserDB):
    def __init__(self):
        pass

    def showAll(self):
        self.conecta_bd()   # Chassis Comp Subcomp content  
        self.cursor.execute(""" SELECT * FROM Users """)
        lista=self.cursor.fetchall()
        self.desconecta_bd()
        #print(lista)
        return lista
    def showUser(self,i_d):
        self.conecta_bd()   # Chassis Comp Subcomp content  
        self.cursor.execute(f""" SELECT * FROM Users WHERE ID LIKE {i_d} """)
        user=self.cursor.fetchone()
        self.desconecta_bd()
        #print(user)
        return user
    def add_user(self, username="",password="",role=""):
        self.conecta_bd()
        self.cursor.execute(""" INSERT INTO Users (Username, Password, Role)
                VALUES (?, ?, ?)""", (username,password,role))
        self.conn.commit()
        self.desconecta_bd()
        #print("Usiario adicionado")
    
    def editar_user(self,i_d, username="",password="",role=""):
        self.conecta_bd()
        self.cursor.execute(""" UPDATE Users SET Username= ?, Password =?, Role =?
                WHERE ID = ?""", (username,password,role, i_d))
        self.conn.commit()
        self.desconecta_bd()
        #print("Usiario editado")
        self.showAll()

    def dele_user(self,i_d):
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM Users  WHERE ID = ?""", ( i_d,))
        self.conn.commit()
        self.desconecta_bd()
        #print("Usiario deletado")
        self.showAll()
    
    def authenticate(self,user,password):
        self.conecta_bd()   # Chassis Comp Subcomp content  
        self.cursor.execute(f""" SELECT * FROM Users WHERE (Username LIKE '{user}' AND  Password LIKE '{password}')""")
        user=self.cursor.fetchone()
        self.desconecta_bd()
        if user is not None: 
            user_id=user[3] 
        else: 
            user_id=None
        return [user is not None, user_id]

class SetupAreasDB():
    def __init__(self):
        self.montaTabelas()
        
    def conecta_bd(self):
        self.conn = sqlite3.connect("DB/Areas.db")
        self.cursor = self.conn.cursor(); 
        print("Conectando ao banco de dados areas")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados areas")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela de de usuarios
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS Areas (
                    ID INTEGER PRIMARY KEY,
                    Name CHAR(40) UNIQUE,
                    Description CHAR(40),
                    Aditional CHAR(40)
                );
            """)
        self.conn.commit(); print("Banco de dados criado areas")
        self.desconecta_bd()

class AreasManagement(SetupAreasDB):
    def __init__(self):
        pass

    def showAll(self):
        self.conecta_bd()   # Chassis Comp Subcomp content  
        self.cursor.execute(""" SELECT * FROM Areas """)
        lista=self.cursor.fetchall()
        self.desconecta_bd()
        
        return lista
    def showarea(self,i_d):
        self.conecta_bd()   # Chassis Comp Subcomp content  
        self.cursor.execute(f""" SELECT * FROM Areas WHERE ID LIKE {i_d} """)
        user=self.cursor.fetchone()
        self.desconecta_bd()
        
        return user
    def add_area(self, Name="",Description="",Aditional=""):
        self.conecta_bd()
        self.cursor.execute(""" INSERT INTO Areas (Name, Description, Aditional)
                VALUES (?, ?, ?)""", (Name,Description,Aditional))
        self.conn.commit()
        self.desconecta_bd()
        print("Usiario adicionado areas")
        self.showAll()
    
    def editar_area(self,i_d, Name="",Description="",Aditional=""):
        self.conecta_bd()
        self.cursor.execute(""" UPDATE Areas SET Name = ?, Description =?, Aditional =?
                WHERE ID = ?""", (Name,Description,Aditional, i_d))
        self.conn.commit()
        self.desconecta_bd()
        print("Usiario editado areas")
        self.showAll()

    def dele_area(self,i_d):
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM Areas  WHERE ID = ?""", ( i_d,))
        self.conn.commit()
        self.desconecta_bd()
        print("Usiario deletado areas")
        self.showAll()
    
class SetupEachAreaDB():
    def __init__(self,nome):
        self.nome = nome
        self.montaTabelaPrincipal(self.nome)
    def conecta_bd(self,nome):
        self.conn = sqlite3.connect(f"DB/DB_area/{nome}.db")
        self.cursor = self.conn.cursor(); 
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        print("Conectando ao banco de dados ")
        
    def desconecta_bd(self):
        self.conn.close(); 
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        print("Desconectando ao banco de dados")
    def montaTabelaPrincipal(self,nome):
        self.conecta_bd(nome)
        ### Criar tabela de de usuarios
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS '{nome}' (
                    ID INTEGER PRIMARY KEY,
                    Name CHAR(40) UNIQUE,
                    Description CHAR(40),
                    Aditional CHAR(40)
                );
            """)
        
        self.conn.commit(); 
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        print("Banco de dados criado")
        self.desconecta_bd()
    def montaTabelaAuxiliar(self,nome,subnome):
        self.conecta_bd(nome)
        ### Criar tabela de de usuarios
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {subnome} (
                    ID INTEGER PRIMARY KEY,
                    File_Name CHAR(80) UNIQUE,
                    Description CHAR(80),
                    Type CHAR(80),
                    file BLOB
                );
            """)
        self.conn.commit(); 
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        print("Banco de dados criado")
        self.desconecta_bd()

class EAchAreaManagemnet(SetupEachAreaDB):
    def __init__(self,):
        pass

    def criar_db(self,nome):
        SetupEachAreaDB(nome)

    def add_sub_area(self,area, Name, Description,Aditional):
        self.conecta_bd(area)
        self.cursor.execute(f""" INSERT INTO {area} (Name, Description, Aditional)
                VALUES (?, ?, ?)""", (Name,Description,Aditional))
        self.conn.commit()
        self.desconecta_bd()
        self.montaTabelaAuxiliar(area, Name)
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        print("seção criada")
    def rename_main_table(self,area,oldName,newName):
        self.conecta_bd(area)
        self.cursor.execute(f""" ALTER TABLE {oldName} RENAME TO {newName};""")
        self.conn.commit()
        self.desconecta_bd()
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        print('nome tabela alterado')

    def showAll(self,area):
        self.conecta_bd(area)   # Chassis Comp Subcomp content  
        self.cursor.execute(f""" SELECT * FROM {area} """)
        lista=self.cursor.fetchall()
        self.desconecta_bd()
        
        return lista
    def showAlltables(self,area):
        self.conecta_bd(area)   # Chassis Comp Subcomp content  
        self.cursor.execute(f"""SELECT name FROM sqlite_master  
  WHERE type='table';""")
        lista=self.cursor.fetchall()
        self.desconecta_bd()
        
        return lista
    def delete_sub_area(self,area,name):

        self.conecta_bd(area)
        self.cursor.execute(f""" DELETE FROM {area}  WHERE Name = ?""", ( name,))
        self.cursor.execute(f""" DROP TABLE IF EXISTS {name}""")
        self.conn.commit()
        self.desconecta_bd()
        
        
    def showSubArea(self,area,name):
        self.conecta_bd(area)   # Chassis Comp Subcomp content  
        self.cursor.execute(f""" SELECT * FROM {area}  WHERE Name = ?""", ( name,))
        subarea=self.cursor.fetchone()
        self.desconecta_bd()
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        return subarea
    def edit_sub_area(self,area,subarea_id,Name,Description,Aditional):
        self.conecta_bd(area)
        self.cursor.execute(f""" UPDATE {area} SET Name = ?, Description =?, Aditional =?
                WHERE ID = ?""", (Name,Description,Aditional, subarea_id))
        self.conn.commit()
        self.desconecta_bd()
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        self.showAll(area)
    def showData(self,area,name):
        self.conecta_bd(area)   # Chassis Comp Subcomp content  
        self.cursor.execute(f""" SELECT * FROM {name} """)
        lista=self.cursor.fetchall()
        self.desconecta_bd()
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        
        return lista
    def addData(self,area,subarea,Name,Description, Type, File):
        self.conecta_bd(area)
        self.cursor.execute(f""" INSERT INTO {subarea} (File_Name, Description, type, file)
                VALUES (?, ?, ?, ?)""", (Name,Description,Type, File))
        self.conn.commit()
        self.desconecta_bd()
       
        print("Usiario adicionado")
    def extractData(self,area,subarea,Name):
        self.conecta_bd(area)   # Chassis Comp Subcomp content  
        self.cursor.execute(f""" SELECT * FROM {subarea} WHERE File_Name = ? """, (Name,))
        data=self.cursor.fetchone()
        self.desconecta_bd()
        print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
        
        return data
    def delete(self, area, sub_area, Name):
        self.conecta_bd(area)
        self.cursor.execute(f""" DELETE FROM {sub_area}  WHERE File_Name = ?""", ( Name,))
        self.conn.commit()
        self.desconecta_bd()
        print("Arquivo deletado areas")
        
class FlaskApp:
    def __init__(self):
        self.app = app
        self.setup_routes()
        self.user_manager = UserManagement()
        self.area_management = AreasManagement()
        self.eachArea = EAchAreaManagemnet()
    def setup_routes(self):
        self.app.add_url_rule('/','index',self.index)

        #user routes
        self.app.add_url_rule('/register','register',self.register, methods=['GET', 'POST'])
        self.app.add_url_rule('/view_users','view_users',self.viewUsers)
        self.app.add_url_rule('/edit_user/<int:user_id>','edit_user',self.editUser, methods=['GET', 'POST'])
        self.app.add_url_rule('/delete_user/<int:user_id>','delete_user',self.deleteUser, methods=[ 'POST'])
        self.app.add_url_rule('/login','login',self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout','logout',self.logout)

        #navigate routes
        self.app.add_url_rule('/add_area','add_area',self.AddArea, methods=['GET', 'POST'])
        self.app.add_url_rule('/edit_area/<int:area_id>','edit_area',self.editArea, methods=['GET', 'POST'])
        self.app.add_url_rule('/delete_area/<int:area_id>','delete_area',self.deleteArea, methods=[ 'POST'])
        self.app.add_url_rule('/view_area/<int:area_id>','view_area',self.viewArea, methods=['GET', 'POST'])

        #Sub area routes
        self.app.add_url_rule('/add_sub_area/<string:area>/','add_sub_area',self.AddSubArea, methods=['GET', 'POST'])
        self.app.add_url_rule('/delete_sub_area/<string:area>/<string:subarea>','delete_sub_area',self.deleteSubArea, methods=['GET', 'POST'])
        self.app.add_url_rule('/edit_sub_area/<string:area>/<string:subarea>','edit_sub_area',self.editeSubArea, methods=['GET', 'POST'])

        #data routes
        self.app.add_url_rule('/view_sub_area/<string:area>/<string:sub_area>','view_sub_area',self.view_sub_area, methods=['GET', 'POST'])
        self.app.add_url_rule('/add_data/<string:area>/<string:sub_area>','add_data',self.add_data, methods=['GET', 'POST'])
        self.app.add_url_rule('/download/<string:area>/<string:sub_area>/<string:name>','download',self.download_data, methods=['GET', 'POST'])
        self.app.add_url_rule('/delete/<string:area>/<string:sub_area>/<string:name>','delete',self.delete_data, methods=['GET', 'POST'])
        self.app.add_url_rule('/display_image/<string:area>/<string:image>','display_image',self.display_image, methods=['GET', 'POST'])
        self.app.add_url_rule('/show_image/<string:name>','show_image',self.show_image, methods=['GET', 'POST'])

    #pages
    def index(self):
        if 'username' not in session:
            return redirect(url_for('login'))
        else:
            areas = self.area_management.showAll()
            return render_template('index.html', username=session['username'], role=session['role'], areas=areas)
    def register(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            print((username, password, role))
            self.user_manager.add_user(username, password, role)
        return render_template('user/register.html') 
    def viewUsers(self):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        users = self.user_manager.showAll()
        return render_template('user/view_users.html',users=users) 
    def editUser(self,user_id):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            print((username, password, role))
            self.user_manager.editar_user(user_id,username, password, role)
            return redirect(url_for('view_users')) 
        else:
            user = self.user_manager.showUser(user_id)
        
            return render_template('user/edit_user.html',user=user) 
    def deleteUser(self,user_id):
        if request.method == 'POST':
            self.user_manager.dele_user(user_id)
            return redirect(url_for('view_users'))
    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            if self.user_manager.authenticate(username, password)[0]:
                session['username'] = username
                session['role'] = self.user_manager.authenticate(username, password)[1]
                return redirect(url_for('index'))
            else:
                print('Invalid Credentials')
                return render_template('user/login.html', error='Invalid credentials')
        return render_template('user/login.html')
    def logout(self):
        session.pop('username', None)
        session.pop('role', None)
        return redirect(url_for('login'))
    
    def AddArea(self):
        if 'role' in session and session['role'] != "Manager":
            return redirect(url_for('index'))
        if request.method == 'POST':
            Name = request.form['Name']
            Description = request.form['Description']
            Aditional = request.form['Aditional']
            print((Name, Description, Aditional))
            self.area_management.add_area(Name, Description, Aditional)

            #Criar DB para area
            self.eachArea.criar_db(Name)
        return render_template('areas/add_area.html')
    def editArea(self,area_id):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        if request.method == 'POST':
            Name = request.form['Name']
            Description = request.form['Description']
            Aditional = request.form['Aditional']
            print((Name, Description, Aditional))
            self.area_management.editar_area(area_id,Name, Description, Aditional)
            rename(f'DB/DB_area/temp.db',f'DB/DB_area/{Name}.db')
            self.eachArea.rename_main_table(f'{Name}',"temp",Name)
            return redirect(url_for('index')) 
        else:
            area = self.area_management.showarea(area_id)
            rename(f'DB/DB_area/{area[1]}.db', 'DB/DB_area/temp.db')
            self.eachArea.rename_main_table('temp',area[1],"temp") 
            return render_template('areas/edit_area.html',area=area)     
    def deleteArea(self,area_id):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        if request.method == 'POST':
            area = self.area_management.showarea(area_id)
            self.area_management.dele_area(area_id)
            remove(f'DB/DB_area/{area[1]}.db')
            return redirect(url_for('index'))
    def viewArea(self,area_id):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        
        print("\n\n\n OK \n\n\n")
        area = self.area_management.showarea(area_id)
        subareas=self.eachArea.showAll(area[1])
        return render_template('areas/view_area.html',area=area,subareas=subareas) 
    def AddSubArea(self, area):
        if 'role' in session and session['role'] != "Manager":
            return redirect(url_for('index'))
        if request.method == 'POST':
            Name = request.form['Name']
            Description = request.form['Description']
            Aditional = request.form['Aditional']
            print((Name, Description, Aditional))
            self.eachArea.add_sub_area(area, Name, Description, Aditional)

            #Criar DB para area
            #self.eachArea.criar_db(Name)
            lista=self.eachArea.showAlltables(area)
            
        print(area)
        return render_template('areas/add_sub_area.html', area=area)
    def deleteSubArea(self,area,subarea):
        print('\x1b[6;30;42m' +f"\n{area}{subarea}\n"+'\x1b[0m')
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        if request.method == 'POST':
        
            self.eachArea.delete_sub_area(area,subarea)
            print('\x1b[6;30;42m' +f"\n{area}{subarea}\n"+'\x1b[0m')
            return redirect(url_for('index'))
    def editeSubArea(self,area,subarea):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        if request.method == 'POST':
            Name = request.form['Name']
            Description = request.form['Description']
            Aditional = request.form['Aditional']
            print((Name, Description, Aditional))
            sub_area = self.eachArea.showSubArea(area,subarea)
            self.eachArea.edit_sub_area(area,sub_area[0],Name, Description, Aditional)

            
            self.eachArea.rename_main_table(area,"temp",Name)
            return redirect(url_for('index')) 
        else:
            #area = self.area_management.showarea(area)
            
            self.eachArea.rename_main_table(area,subarea,"temp")
            sub_area = self.eachArea.showSubArea(area,subarea) 
            return render_template('areas/edit_sub_area.html',area=area,subarea=sub_area) 
    
    def view_sub_area(self,area,sub_area):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        
        
        #area = self.area_management.showarea(area_id)
        datas=self.eachArea.showData(area,sub_area)
        return render_template('data_mng/view_sub_area.html',area=area,subarea=sub_area,datas=datas) 
    
    def add_data(self,area,sub_area):
        if 'role' in session and session['role'] != "Manager":
            return redirect(url_for('index'))
        if request.method == 'POST':
            
            Description = request.form['Description']
            
            file = request.files['file']
            filename = file.filename
            filetype= file.content_type
            filecontent=  file.read()
            
            self.eachArea.addData(area,sub_area,filename,Description, filetype, filecontent)
            print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')


        
        return render_template('data_mng/add_data.html', area=area,sub_area=sub_area)
    def download_data(self,area,sub_area,name):
        if 'role' in session and session['role'] != "Manager":
            return redirect(url_for('index'))
        data = self.eachArea.extractData(area,sub_area,name)
        cd=getcwd()
        try:
            makedirs(f'{cd}/temp')
        except:
            pass
        with open(f"{cd}/temp/{data[1]}", 'wb') as output_file:
            output_file.write(data[4])
            print('\x1b[6;30;42m' +f"\n\n"+'\x1b[0m')
            print('arquivo salvo')
        #params={'area':area,'image':f"temp/{data[1]}"}

        return self.display_image(area,f"{data[1]}")
        #return redirect(url_for('display_image',**params))
    
        #return send_file(f"{cd}/temp/{data[1]}",as_attachment=True)
    
    def delete_data(self,area,sub_area,name):
        self.eachArea.delete(area,sub_area,name)
        params={'area':area,'sub_area':sub_area}
        return redirect(url_for(f'view_sub_area',**params))
    
    def display_image(self,area,image):

        return render_template(f'/data_mng/view_image.html',area=area,image=image)
    
    def show_image(self,name):
        print('\x1b[6;30;42m' +f"IMAGEM"+'\x1b[0m')
        print(name)
        return send_from_directory(f"{getcwd()}\\temp\\",name)
    
if __name__ == '__main__':
    #app()
    print('\x1b[6;30;42m' +f"inicio"+'\x1b[0m')
    SetupUserDB()
    SetupAreasDB()
    flask_app = FlaskApp()
    flask_app.app.run(host='0.0.0.0', port=80, debug=True)