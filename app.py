from conexion import Conexion
from datetime import datetime
from alerta import Alerta
from bson.json_util import dumps
import lectorCSV
import calculos
import pandas as pd
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, json, Response
import graficos

import os
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/novedades', methods=['POST', 'GET'])
def novedades():
    return render_template('novedades.html')

@app.route('/ultimas24hs', methods=['POST', 'GET'])
def ultimas24hs():
    return render_template('ultimas24hs.html')

@app.route('/informes', methods=['POST', 'GET'])
def informes():
    return render_template('informes.html', imagen={ 'imagen': '' })

@app.route('/informesPorTipo', methods=['POST', 'GET'])
def informesPorTipo():
    return render_template('informesPorTipo.html')

@app.route('/informesPorTramo', methods=['POST', 'GET'])
def informesPorTramo():
    return render_template('informesPorTramo.html')

@app.route('/leerUnCSV', methods=['POST'])
def leerUnCSV():
    
    if request.method=='POST':
        try:
            nombreCSV=request.form.get("nombreCSV")
            print(nombreCSV)
            lectorCSV.leerCSV(nombreCSV)
           

        except Exception as e:
            error=str(e)
            return jsonify({'result':'error','error':error})   
    
    return jsonify({'result':'success'})

@app.route('/UltimasAlertas', methods=['POST'])
def UltimasAlertas():  
    
    ultAlertas = list(Alerta.buscarUltimasAlertas())
    
    for i in ultAlertas:
        f = (i['fecha_inicio'])
        i['fecha_inicio'] = "{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}".format(f.day, f.month, f.year, f.hour, f.minute, f.second)

    datosJson = dumps(ultAlertas)

    return jsonify({'result':'success', 'alertas': datosJson})


def tiempoReal(fecha, ubicacion, temperatura, humedad, presion, velocidadViento, milimetrosLluvia, puntoRocio, velocidadVehic, longitudVehic):
          
    
    calculos.AlertasLluvia(milimetrosLluvia, fecha, ubicacion)
    calculos.AlertasViento(velocidadViento, fecha, ubicacion)
    calculos.AlertasNiebla(temperatura, velocidadViento, presion, puntoRocio, fecha, ubicacion)
    



@app.route('/estadisticasGenerales', methods=['POST'])
def estadisticasGenerales():
    if request.method=='POST':
        desde=request.form.get("desde")  
        hasta=request.form.get("hasta")  
        try:
            graficosNiveles = graficos.informeGeneralNivel(desde,hasta)
            graficosTipos = graficos.informeGeneralTipo(desde,hasta)

        except Exception as e:
            error=str(e)
            return jsonify({'result':'error','error':error})
       
        return jsonify({'result':'success', 'imagenNiveles': graficosNiveles, 'imagenTipos': graficosTipos  })


@app.route('/estadisticasPorTipo', methods=['POST'])
def estadisticasPorTipo():
    if request.method=='POST':
        tipo=request.form.get("tipo")  
        desde=request.form.get("desde")  
        hasta=request.form.get("hasta")  
        try:
            print(desde)
            print(hasta)

            graficosNiveles = graficos.informeTipoNivel(tipo,desde,hasta)  
            graficosNivelesSemana = graficos.informeTipoNivelSemana(tipo,desde,hasta)        
            graficosNivelesMes = graficos.informeTipoNivelMes(tipo,desde,hasta) 

        except Exception as e:
            error=str(e)
            return jsonify({'result':'error','error':error})

        return jsonify({'result':'success', 'imagenNiveles': graficosNiveles , 'imagenNivelesSemana': graficosNivelesSemana, 'imagenNivelesMes': graficosNivelesMes })



if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
       








#modificar = client[MONGODB_DATABASE]['Alertas'].update_one({'tramo': 'aguilares-consepcion'}, {'$set': {'tramo': 'aguilares-concepcion'}})

#a = Alerta('humo','no se ve nada', 'concepcion-rio', 'extrema')
#a.cargarAlerta(cliente,db)

#resultado = client[MONGODB_DATABASE]['Alertas'].find({'tramo': 'aguilares-concepcion'})
'''
resultado = Alerta.buscarAlertas(cliente,db)

for r in resultado:
    print(r['tipo'])
'''    