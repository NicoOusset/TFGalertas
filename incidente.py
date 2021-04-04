from conexion import Conexion
import pymongo
from bson.json_util import dumps
from datetime import datetime
import pprint
from bson.objectid import ObjectId


db = 'tfgAlertas'
cliente = Conexion.conectar()


class Incidente:
    
    def __init__(self,tipo,comentario,tramo,fecha_creacion):
        
        self.tipo = tipo
        self.comentario = comentario
        self.tramo = tramo  
        self.fecha_creacion = fecha_creacion



    def cargarIncidente(self):

        database_entry = {}
        database_entry['tipo'] = self.tipo
        database_entry['comentario'] = self.comentario
        database_entry['tramo'] = self.tramo
        database_entry['fecha_creacion'] = self.fecha_creacion
        database_entry['estado'] = 'NoVisualizado'
              
        try:
            destination = 'Incidentes'
            collection = cliente[db]['Incidentes']
            collection.insert_one(database_entry)

        except Exception as error:
            print ("Error cargando el incidente: %s" % str(error))


    def buscarIncidentes(tramo, tipo, desde, hasta, sinVisualizar, sinAlertar):
        
        tramoRuta  = tramo
        tipoRiesgo = tipo
    
        if desde == "":
            fechaDesde = datetime(2020, 1, 1)
        else:            
            fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')

        if hasta == "":            
            fechaHasta = datetime(2220, 1, 1)
        else:            
            fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')

        print(sinVisualizar)
        if sinAlertar == "false":            
            aaa = ".*"+""+".*"
        else:            
            aaa = ".*"+"Visualizado"+".*"

        if sinVisualizar == "true":                       
            aaa = ".*"+"NoVisualizado"+".*"

        
        
        print(fechaDesde)   
        print(fechaHasta)
        
        ttt = ".*"+tipoRiesgo+".*"
        mmm=".*"+tramoRuta+".*"
        print(sinVisualizar)
        print(sinAlertar)

        incidentes = cliente[db]['Incidentes'].find({'tipo': { "$regex": ttt }  ,'tramo': { "$regex": mmm },'estado': { "$regex": aaa }, 'fecha_creacion': {'$lt': fechaHasta, '$gte': fechaDesde} }).sort("fecha_creacion", pymongo.DESCENDING)       
        
        return incidentes      

    def buscarIncidentePorId(idIncidente):     
        incidenteBuscado = cliente[db]['Incidentes'].find_one({'_id':  ObjectId(idIncidente)  })   

        return incidenteBuscado
    
    def modificarEstadoIncidente(id, nuevoEstado):
        print("visualizar el incidente")
        cliente[db]['Incidentes'].update_one({'_id': ObjectId(id)}, {'$set': {'estado': nuevoEstado}})