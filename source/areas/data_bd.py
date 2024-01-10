import sqlite3


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
        