import sqlite3

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
