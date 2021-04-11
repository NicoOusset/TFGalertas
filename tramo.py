from conexion import Conexion
import pymongo
from bson.json_util import dumps

db = 'tfgAlertas'
cliente = Conexion.conectar()



class Tramo:

    def __init__(self,nombre):
        
        self.nombre = nombre
        
    def cargarNuevoTramo(self):
    
        database_entry = {}
        database_entry['nombre'] = self.nombre
              
        try:
            destination = 'Tramos'
            collection = cliente[db]['Tramos']
            collection.insert_one(database_entry)

        except Exception as error:
            print ("Error cargando tramo: %s" % str(error))


    def buscarTramos():
        Tramos = cliente[db]['Tramos'].find()      
        return Tramos 
