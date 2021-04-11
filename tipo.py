from conexion import Conexion
import pymongo
from bson.json_util import dumps

db = 'tfgAlertas'
cliente = Conexion.conectar()

class Tipo:

    def __init__(self,nombre,descripcion):
        
        self.nombre = nombre
        self.descripcion = descripcion
        
    def cargarNuevoTipo(self):
    
        database_entry = {}
        database_entry['nombre'] = self.nombre
        database_entry['descripcion'] = self.descripcion

              
        try:
            destination = 'Tipos'
            collection = cliente[db]['Tipos']
            collection.insert_one(database_entry)

        except Exception as error:
            print ("Error cargando Tipo de riesgo: %s" % str(error))


    def buscarTipos():
        Tipos = cliente[db]['Tipos'].find()      
        return Tipos 
