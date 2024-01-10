from flask import request, session, redirect, render_template, url_for
from .Users_db import UserManagement

class Users_app:
    def __init__(self, app):
        self.app = app
        self.user_manager = UserManagement()
    def setup_routes(self):
        self.app.add_url_rule('/register','register',self.register, methods=['GET', 'POST'])
        self.app.add_url_rule('/view_users','view_users',self.viewUsers)
        self.app.add_url_rule('/edit_user/<int:user_id>','edit_user',self.editUser, methods=['GET', 'POST'])
        self.app.add_url_rule('/delete_user/<int:user_id>','delete_user',self.deleteUser, methods=[ 'POST'])
        self.app.add_url_rule('/login','login',self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout','logout',self.logout)
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
  