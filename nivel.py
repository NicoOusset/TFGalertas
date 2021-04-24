from conexion import Conexion
import pymongo
from bson.json_util import dumps

db = 'tfgAlertas'
cliente = Conexion.conectar()

class Nivel:

    def __init__(self,nombre,descripcion):
        
        self.nombre = nombre
        self.descripcion = descripcion
        
    def cargarNuevoNivel(self):
    
        database_entry = {}
        database_entry['nombre'] = self.nombre
        database_entry['descripcion'] = self.descripcion

              
        try:
            destination = 'Niveles'
            collection = cliente[db]['Niveles']
            collection.insert_one(database_entry)

        except Exception as error:
            print ("Error cargando Niveles de riesgo: %s" % str(error))


    def buscarNiveles():
        Niveles = cliente[db]['Niveles'].find()      
        return Niveles 

""" tipos = [("leve","Leve"),("moderado","Moderado"),("alto","Alto"),("extrema","Extrema")]
for t in tipos:
    tip = Nivel(t[0],t[1])
    tip.cargarNuevoNivel()  """