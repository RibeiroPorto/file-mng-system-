import sqlite3

class SetupFactoryDB():
    def __init__(self):
        self.montaTabelas()
        
    def conecta_bd(self):
        self.conn = sqlite3.connect("DB/factory/factory.db")
        self.cursor = self.conn.cursor(); 
        #print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); 
        #print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela de de usuarios
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS Production (
                    ID INTEGER PRIMARY KEY,
                    PartNumber CHAR(40),
                    NI CHAR(40),
                    Operador CHAR(40)
                );
            """)
        self.conn.commit(); 
        #print("Banco de dados criado")
        self.desconecta_bd()

class ProductionRegistry(SetupFactoryDB):
    def __init__(self):
        pass

    def showAll(self):
        self.conecta_bd()   # Chassis Comp Subcomp content  
        self.cursor.execute(""" SELECT * FROM Production """)
        lista=self.cursor.fetchall()
        self.desconecta_bd()
        #print(lista)
        return lista
    def showOne(self,i_d):
        self.conecta_bd()   # Chassis Comp Subcomp content  
        self.cursor.execute(f""" SELECT * FROM Production WHERE ID LIKE {i_d} """)
        user=self.cursor.fetchone()
        self.desconecta_bd()
        #print(user)
        return user
    def addOne(self, PartNumber="",NI="",Operador=""):
        self.conecta_bd()
        self.cursor.execute(""" INSERT INTO Production (PartNumber, NI, Operador)
                VALUES (?, ?, ?)""", (PartNumber,NI,Operador))
        self.conn.commit()
        self.desconecta_bd()
        #print("Usiario adicionado")
    
    def edit(self,i_d, PartNumber="",NI="",Operador=""):
        self.conecta_bd()
        self.cursor.execute(""" UPDATE Production SET PartNumber= ?, NI =?, Operador =?
                WHERE ID = ?""", (PartNumber,NI,Operador, i_d))
        self.conn.commit()
        self.desconecta_bd()
        #print("Usiario editado")
        self.showAll()

    def deleteOne(self,i_d):
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM Production WHERE ID = ?""", ( i_d,))
        self.conn.commit()
        self.desconecta_bd()
        #print("Usiario deletado")
        self.showAll()
    

