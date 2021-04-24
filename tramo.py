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

""" 
trs = ["Rumi Punco - Pueblo Viejo","Pueblo Viejo - Rio el Sueño","Rio el Sueño - Huasa Pampa","Huasa Pampa - Rio Marapa","Rio Marapa - Villa Belgrano","Villa Belgrano - Aguilares","Aguilares - Concepcion","Concepcion - Rio Seco","Rio Seco - Monteros","Monteros - Rio Caspichango","Rio Caspichango - Interseccion ruta 322","Interseccion ruta 322 - Interseccion ruta 321","Interseccion ruta 321 - S M de Tuc"]

for t in trs:
    tip = Tramo(t)
    tip.cargarNuevoTramo()  """