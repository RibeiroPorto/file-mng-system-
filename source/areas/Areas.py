from flask import session, request, render_template, redirect, url_for, send_from_directory

from os import remove, rename, getcwd, makedirs
from source.areas.Areas_db import  AreasManagement
from source.areas.data_bd import  EAchAreaManagemnet



class Areas_app:
    def __init__(self, app):
        self.app = app
        self.area_management = AreasManagement()
        self.eachArea = EAchAreaManagemnet()
    def setup_routes(self):
        
        #navigate routes
        self.app.add_url_rule('/add_area','add_area',self.AddArea, methods=['GET', 'POST'])
        self.app.add_url_rule('/edit_area/<int:area_id>','edit_area',self.editArea, methods=['GET', 'POST'])
        self.app.add_url_rule('/delete_area/<int:area_id>','delete_area',self.deleteArea, methods=[ 'POST'])
        self.app.add_url_rule('/view_area/<int:area_id>','view_area',self.viewArea, methods=['GET', 'POST'])

        #Sub area routes
        self.app.add_url_rule('/add_sub_area','add_sub_area',self.AddSubArea, methods=['GET', 'POST'])
        self.app.add_url_rule('/delete_sub_area/<string:subarea>','delete_sub_area',self.deleteSubArea, methods=['GET', 'POST'])
        self.app.add_url_rule('/edit_sub_area/<string:subarea>','edit_sub_area',self.editeSubArea, methods=['GET', 'POST'])

        #data routes
        self.app.add_url_rule('/view_sub_area/<string:sub_area>','view_sub_area',self.view_sub_area, methods=['GET', 'POST'])
        self.app.add_url_rule('/add_data','add_data',self.add_data, methods=['GET', 'POST'])
        self.app.add_url_rule('/download/<string:name>','download',self.download_data, methods=['GET', 'POST'])
        self.app.add_url_rule('/delete/<string:name>','delete',self.delete_data, methods=['GET', 'POST'])
        self.app.add_url_rule('/display_image/<string:area>/<string:image>','display_image',self.display_image, methods=['GET', 'POST'])
        self.app.add_url_rule('/show_image/<string:name>','show_image',self.show_image, methods=['GET', 'POST'])

        self.app.add_url_rule('/areas','areas',self.index)
    
    def index(self):
        if 'username' not in session:
            return redirect(url_for('login'))
        else:
            areas = self.area_management.showAll()
            session['current_page']='Areas'
            return render_template('areas/areas.html', username=session['username'], role=session['role'], areas=areas, current_page= session['current_page'])
        
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
        
        
        area = self.area_management.showarea(area_id)
        session['current_area']= area
        subareas=self.eachArea.showAll(area[1])
        
        return render_template('areas/view_area.html',area=area,subareas=subareas) 
    def AddSubArea(self):
        if 'role' in session and session['role'] != "Manager":
            return redirect(url_for('index'))
        area_name=session['current_area'][1]
        if request.method == 'POST':
            Name = request.form['Name']
            Description = request.form['Description']
            Aditional = request.form['Aditional']
            print((Name, Description, Aditional))
            self.eachArea.add_sub_area(area_name, Name, Description, Aditional)

            #Criar DB para area
            #self.eachArea.criar_db(Name)
            lista=self.eachArea.showAlltables(area_name)
            
        return render_template('areas/add_sub_area.html', area=area_name)
    def deleteSubArea(self,subarea):
        
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        area_name=session['current_area'][1]
        if request.method == 'POST':
        
            self.eachArea.delete_sub_area(area_name,subarea)
            
            return redirect(url_for('index'))
    def editeSubArea(self,subarea):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        area_name=session['current_area'][1]
        if request.method == 'POST':
            Name = request.form['Name']
            Description = request.form['Description']
            Aditional = request.form['Aditional']
            print((Name, Description, Aditional))
            sub_area = self.eachArea.showSubArea(area_name,subarea)
            self.eachArea.edit_sub_area(area_name,sub_area[0],Name, Description, Aditional)

            
            self.eachArea.rename_main_table(area_name,"temp",Name)
            return redirect(url_for('index')) 
        else:
            #area = self.area_management.showarea(area)
            
            self.eachArea.rename_main_table(area_name,subarea,"temp")
            sub_area = self.eachArea.showSubArea(area_name,subarea) 
            return render_template('areas/edit_sub_area.html',area=area_name,subarea=sub_area)     
    def view_sub_area(self,sub_area):
        if 'role' in session and session['role'] !="Manager":
            return redirect(url_for('index'))
        area_name=session['current_area'][1]
        subarea= self.eachArea.showSubArea(area_name,sub_area)
        session['current_sub_area']= subarea
        #area = self.area_management.showarea(area_id)
        datas=self.eachArea.showData(area_name,sub_area)
        return render_template('data_mng/view_sub_area.html',area=area_name,subarea=sub_area,datas=datas) 
    def add_data(self):
        if 'role' in session and session['role'] != "Manager":
            return redirect(url_for('index'))
        area_name = session['current_area'][1]
        sub_area_name = session['current_sub_area'][1]
        if request.method == 'POST':
            
            Description = request.form['Description']
            
            file = request.files['file']
            filename = file.filename
            filetype= file.content_type
            filecontent=  file.read()
            
            self.eachArea.addData(area_name,sub_area_name ,filename,Description, filetype, filecontent)
            print('\x1b[6;30;42m' +f"\nOLA OLA\n"+'\x1b[0m')


        
        return render_template('data_mng/add_data.html', area=area_name,sub_area=sub_area_name)
    def download_data(self,name):
        if 'role' in session and session['role'] != "Manager":
            return redirect(url_for('index'))
        area_name=session['current_area'][1]
        sub_area_name=session['current_sub_area'][1]
        data = self.eachArea.extractData(area_name,sub_area_name,name)
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

        return self.display_image(area_name,f"{data[1]}")
        #return redirect(url_for('display_image',**params))
    
        #return send_file(f"{cd}/temp/{data[1]}",as_attachment=True)
    def delete_data(self,name):
        area_name=session['current_area'][1]
        sub_area_name=session['current_sub_area'][1]
        self.eachArea.delete(area_name,sub_area_name,name)
        params={'area':area_name,'sub_area':sub_area_name}
        return redirect(url_for(f'view_sub_area',**params))
    def display_image(self,area,image):
        area_name=session['current_area'][1]
        
        return render_template(f'/data_mng/view_image.html',area=area_name,image=image)
    def show_image(self,name):
        print('\x1b[6;30;42m' +f"IMAGEM"+'\x1b[0m')
        print(name)

        return send_from_directory(f"{getcwd()}\\temp\\",name)
        