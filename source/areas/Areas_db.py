import sqlite3

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
