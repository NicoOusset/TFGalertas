from conexion import Conexion
import pymongo
from bson.json_util import dumps
from datetime import datetime
import pprint

import matplotlib.pyplot as plt 

db = 'tfgAlertas'
cliente = Conexion.conectar()


class Alerta:
    
    def __init__(self,tipo,descripcion,tramo,nivel,fecha_inicio, fecha_fin):
        
        self.tipo = tipo
        self.descripcion = descripcion
        self.tramo = tramo
        self.nivel = nivel
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


    def cargarAlerta(self):

        database_entry = {}
        database_entry['tipo'] = self.tipo
        database_entry['descripcion'] = self.descripcion
        database_entry['tramo'] = self.tramo
        database_entry['nivel'] = self.nivel
        database_entry['fecha_inicio'] = self.fecha_inicio
        database_entry['fecha_fin'] = self.fecha_fin
        database_entry['activa'] = 'True'
              
        try:
            destination = 'Alertas'
            collection = cliente[db]['Alertas']
            collection.insert_one(database_entry)

        except Exception as error:
            print ("Error cargando alerta: %s" % str(error))

    
    def buscarAlertaActiva(tipo,ubicacion):    
        
        alertaActiva = cliente[db]['Alertas'].find({'tipo': tipo,'tramo': ubicacion, 'activa': "True"  })
        resultado = ""       
        
        for r in alertaActiva:
            #resultado = r['nivel']
            resultado = r

        return resultado

    
    def inactivarAlerta(idAlerta, fecha):
        cliente[db]['Alertas'].update_one({'_id': idAlerta}, {'$set': {'activa': 'False', 'fecha_fin': fecha}})
          

    def buscarUltimasAlertas():
        
        ultimasAlertas = cliente[db]['Alertas'].find().sort("fecha_inicio", pymongo.DESCENDING).limit(10)
        
        return ultimasAlertas

        '''resultado = []  
        for r in ultimasAlertas:
            r1 = r['fecha_inicio'],' - ',r['_id']
            resultado.append(r1)

        print(resultado)
        return resultado'''
        

    def informeGeneralTipo(desde, hasta):
    
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        print(fechaDesde)
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')
        print(fechaHasta)
       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} } },
                                                { "$group" : {"_id":"$tipo", "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id":1} }
                                            ])

        tipos = []
        cantidades = []
        resultados = []

        for a in ver:
            n = a['_id']
            c = a['total']
            tipos.append(n)
            cantidades.append(c)

        resultados = [tipos, cantidades]
        print(resultados)
        return resultados


    def informeGeneralNivel(desde, hasta):
    
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        print(fechaDesde)
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')
        print(fechaHasta)
       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} } },
                                                { "$group" : {"_id":"$nivel", "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id":1} }
                                            ])

        niveles = []
        cantidades = []
        resultados = []

        for a in ver:
            n = a['_id']
            c = a['total']
            niveles.append(n)
            cantidades.append(c)

        resultados = [niveles, cantidades]
        print(resultados)
        return resultados


    def informePorTipoNivel(tipo, desde, hasta):
        
        tipoAlerta = tipo
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')

       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} , 'tipo': tipoAlerta } },
                                                { "$group" : {"_id":"$nivel", "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id":1} }
                                            ])

        niveles = []
        cantidades = []
        resultados = []

        for a in ver:
            n = a['_id']
            c = a['total']
            niveles.append(n)
            cantidades.append(c)

        resultados = [niveles, cantidades]
        print(resultados)
        return resultados

    def informePorTipoNivelMes(tipo, desde, hasta):
        
        tipoAlerta = tipo
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')

       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} , 'tipo': tipoAlerta } },
                                                { "$group" : {"_id": { "day" : {"$month":"$fecha_inicio"},"nivel":"$nivel"}, "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id.day":1} }
                                            ])

        meses  = []
        niveles = []
        cantidades = []
        resultados = []

        for a in ver:
            m = a['_id']['day']
            n = a['_id']['nivel']
            c = a['total']
            meses.append(m)
            niveles.append(n)
            cantidades.append(c)
            #resultados.append(a)

        resultados = [meses, niveles, cantidades]
        print(resultados)
        return resultados

    def informePorTipoNivelSemana(tipo, desde, hasta):
        
        tipoAlerta = tipo
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')

       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} , 'tipo': tipoAlerta } },
                                                { "$group" : {"_id": { "day" : {"$dayOfWeek":"$fecha_inicio"},"nivel":"$nivel"}, "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id.day":1} }
                                            ])

        dias  = []
        niveles = []
        cantidades = []
        resultados = []

        for a in ver:
            d = a['_id']['day']
            n = a['_id']['nivel']
            c = a['total']
            dias.append(d)
            niveles.append(n)
            cantidades.append(c)
            #resultados.append(a)

        resultados = [dias, niveles, cantidades]
        print(resultados)
        return resultados


    def informePorTramoNivel(tramo, desde, hasta):
        
        tramoRuta = tramo
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')

       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} , 'tramo': tramoRuta } },
                                                { "$group" : {"_id":"$nivel", "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id":1} }
                                            ])

        niveles = []
        cantidades = []
        resultados = []

        for a in ver:
            n = a['_id']
            c = a['total']
            niveles.append(n)
            cantidades.append(c)

        resultados = [niveles, cantidades]
        print(resultados)
        return resultados


    def informeTramoTipos(tramo, desde, hasta):
        
        tramoRuta = tramo
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        print(fechaDesde)
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')
        print(fechaHasta)
       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} , 'tramo': tramoRuta } },
                                                { "$group" : {"_id":"$tipo", "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id":1} }
                                            ])

        tipos = []
        cantidades = []
        resultados = []

        for a in ver:
            n = a['_id']
            c = a['total']
            tipos.append(n)
            cantidades.append(c)

        resultados = [tipos, cantidades]
        print(resultados)
        return resultados

    def informeTramoTipoNivelMes(tramo, tipo, desde, hasta):
        
        tramoRuta  = tramo
        tipoAlerta = tipo
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')

       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} , 'tramo': tramoRuta , 'tipo': tipoAlerta } },
                                                { "$group" : {"_id": { "day" : {"$month":"$fecha_inicio"},"nivel":"$nivel"}, "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id.day":1} }
                                            ])

        meses  = []
        niveles = []
        cantidades = []
        resultados = []

        for a in ver:
            m = a['_id']['day']
            n = a['_id']['nivel']
            c = a['total']
            meses.append(m)
            niveles.append(n)
            cantidades.append(c)
            #resultados.append(a)

        resultados = [meses, niveles, cantidades]
        print(resultados)
        return resultados

    
    def informeTramoTipoNivelSemana(tramo, tipo, desde, hasta):
        
        tramoRuta  = tramo
        tipoAlerta = tipo
        fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')
        fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')

       
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} , 'tramo': tramoRuta , 'tipo': tipoAlerta } },
                                                { "$group" : {"_id": { "day" : {"$dayOfWeek":"$fecha_inicio"},"nivel":"$nivel"}, "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id.day":1} }
                                            ])

        dias  = []
        niveles = []
        cantidades = []
        resultados = []

        for a in ver:
            d = a['_id']['day']
            n = a['_id']['nivel']
            c = a['total']
            dias.append(d)
            niveles.append(n)
            cantidades.append(c)
           

        resultados = [dias, niveles, cantidades]
        print(resultados)
        return resultados


    def informePorTramoTipoNivel(tramo, tipo, desde, hasta):
        
        tramoRuta = tramo
        tipoRiesgo = tipo
        fechaDesde1 = desde
        fechaHasta1 = hasta   
        fechaDesde = datetime(fechaDesde1.year, fechaDesde1.month, fechaDesde1.day, fechaDesde1.hour,fechaDesde1.minute,fechaDesde1.second)
        fechaHasta = datetime(fechaHasta1.year, fechaHasta1.month, fechaHasta1.day, fechaHasta1.hour,fechaHasta1.minute,fechaHasta1.second)
        print(fechaDesde)
        print(fechaHasta)
          
        ver = cliente[db]['Alertas'].aggregate([
                                                { "$match" : {'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} , 'tramo': tramoRuta ,'tipo': tipoRiesgo  } },
                                                { "$group" : {"_id":"$nivel", "total" : {"$sum":1} } } , 
                                                { "$sort"  : {"_id":1} }
                                            ])
        

        niveles = []
        cantidades = []
        resultados = []

        for a in ver:
            n = a['_id']
            c = a['total']
            niveles.append(n)
            cantidades.append(c)

        resultados = [niveles, cantidades]
        print(resultados)
        return resultados




    def buscarAlertas(tramo, tipo, desde, hasta):
        
        tramoRuta  = tramo
        tipoAlerta = tipo
    
        if desde == "":
            fechaDesde = datetime(2020, 1, 1)
        else:            
            fechaDesde = datetime.strptime(desde, '%Y-%m-%dT%H:%M')

        if hasta == "":
            
            fechaHasta = datetime(2220, 1, 1)
        else:            
            fechaHasta = datetime.strptime(hasta, '%Y-%m-%dT%H:%M')
        
        print(fechaDesde)   
        print(fechaHasta)
        

        ttt = ".*"+tipoAlerta+".*"
        mmm=".*"+tramoRuta+".*"

        alertas = cliente[db]['Alertas'].find({'tipo': { "$regex": ttt }  ,'tramo': { "$regex": mmm }, 'fecha_inicio': {'$lt': fechaHasta, '$gte': fechaDesde} }).sort("fecha_inicio", pymongo.ASCENDING)       
        #"/.*"+tipoAlerta+".*/i"

        return alertas       
        
        