from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
app.config['DATABASE'] = 'users.db'  # SQLite database file

class DBHandler:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(app.config['DATABASE'])
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None, fetchone=False, fetchall=False):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        else:
            result = None

        cursor.close()
        return result

    def commit(self):
        self.conn.commit()
class UserManager:
    def __init__(self, db_handler):
        self.db = db_handler

    def add_user(self, username, password, role):
        query = 'INSERT INTO users (username, password, role) VALUES (?, ?, ?)'
        params = (username, password, role)
        self.db.execute(query, params)
        self.db.commit()
        print("Usuar adicionado")

    def edit_user(self, username, new_password, new_role):
        query = 'UPDATE users SET password = ?, role = ? WHERE username = ?'
        params = (new_password, new_role, username)
        self.db.execute(query, params)
        self.db.commit()

    def remove_user(self, username):
        query = 'DELETE FROM users WHERE username = ?'
        params = (username,)
        self.db.execute(query, params)
        self.db.commit()

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class DatabaseManager:
    def __init__(self):
        self.db = None

    def init_app(self, app):
        app.teardown_appcontext(self.close_db)
        app.cli.add_command(self.init_db_command,name="init_db" )

    def get_db(self):
        if 'db' not in g:
            g.db = DBHandler()
            g.db.connect()
        return g.db

    def close_db(self, e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def teardown_db(self, e=None):
        self.close_db()

    def init_db_command(self):
        db = self.get_db()
        with app.app_context():
            with app.open_resource('schema.sql', mode='r') as f:
                db.execute(f.read())
            db.commit()
        print('Initialized the database.')

db_handler = DBHandler()
db_manager = DatabaseManager()
user_manager = UserManager(db_handler)

class FlaskApp:
    def __init__(self):
        self.app = app
        self.setup_routes()
        db_manager.init_app(app)

    def setup_routes(self):
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout', 'logout', self.logout)
        self.app.add_url_rule('/dashboard', 'dashboard', self.dashboard)
        self.app.add_url_rule('/','index',self.index)
        self.app.add_url_rule('/register','register',self.register, methods=['GET', 'POST'])
    
    def register(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            user_manager.add_user(username, password, role)
        return render_template('register.html')
    
    def index(self):
        if 'username' not in session:
            return render_template('login.html', error='Invalid credentials')
        return render_template('index.html')
    
    def authenticate(self, username, password):
        db = db_manager.get_db()
        user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password), fetchone=True)
        return user is not None

    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if self.authenticate(username, password):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid credentials')

        return render_template('login.html')

    def logout(self):
        session.pop('username', None)
        return redirect(url_for('login'))

    def dashboard(self):
        if 'username' in session:
            db = db_manager.get_db()
            user = db.execute('SELECT * FROM users WHERE username = ?', (session['username'],), fetchone=True)
            role = user['role']
            return render_template('dashboard.html', username=session['username'], role=role)
        else:
            return redirect(url_for('login'))

if __name__ == '__main__':
    flask_app = FlaskApp()
    flask_app.app.run(debug=True)