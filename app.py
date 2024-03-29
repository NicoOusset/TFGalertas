from conexion import Conexion
from datetime import datetime
from alerta import Alerta
from tramo import Tramo
from tipo import Tipo
from nivel import Nivel
from incidente import Incidente
from usuario import Usuario
from bson.json_util import dumps
import lectorCSV
import calculos
import pandas as pd
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, json, Response
from flask_login import UserMixin, current_user, login_user, logout_user, login_required
from flask_login import LoginManager
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
    if sesion_usuario != "":
        if sesion_usuario.is_authenticated:        
            return render_template('novedades.html')
    else:
        return render_template('novedades.html')

@app.route('/buscador', methods=['POST', 'GET'])
def buscador():
    Tramos = list(Tramo.buscarTramos())
    Tipos = list(Tipo.buscarTipos())
    return render_template('buscador.html' , Tramos=Tramos, Tipos=Tipos)

@app.route('/ultimas24hs', methods=['POST', 'GET'])
def ultimas24hs():
    Tramos = list(Tramo.buscarTramos())
    return render_template('ultimas24hs.html', Tramos=Tramos)

@app.route('/informes', methods=['POST', 'GET'])
def informes():
    return render_template('informes.html', imagen={ 'imagen': '' }, fechaDesde=fechaDesde, fechaHasta=fechaHasta)

@app.route('/informesPorTipo', methods=['POST', 'GET'])
def informesPorTipo():
    Tipos = list(Tipo.buscarTipos())
    return render_template('informesPorTipo.html', Tipos=Tipos, fechaDesde=fechaDesde, fechaHasta=fechaHasta , tipoRiesgo=tipoRiesgo)

@app.route('/informesPorTramo', methods=['POST', 'GET'])
def informesPorTramo():
    Tramos = list(Tramo.buscarTramos())
    Tipos = list(Tipo.buscarTipos())
    return render_template('informesPorTramo.html', fechaDesde=fechaDesde, fechaHasta=fechaHasta, tipoRiesgo=tipoRiesgo ,tramoRuta=tramoRuta, Tramos=Tramos, Tipos=Tipos)

@app.route('/incidentes', methods=['POST', 'GET'])
def incidentes():
    Tramos = list(Tramo.buscarTramos())
    Tipos = list(Tipo.buscarTipos())
    return render_template('incidentes.html', Tramos=Tramos, Tipos=Tipos)

@app.route('/generarIncidente', methods=['POST', 'GET'])
def generarIncidente():
    Tramos = list(Tramo.buscarTramos())
    Tipos = list(Tipo.buscarTipos())
    return render_template('generarIncidente.html', Tramos=Tramos, Tipos=Tipos)

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


def UltimasAlertasMobile():  
    
    ultAlertas = list(Alerta.buscarUltimasAlertas())
    
    for i in ultAlertas:
        f = (i['fecha_inicio'])
        i['fecha_inicio'] = "{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}".format(f.day, f.month, f.year, f.hour, f.minute, f.second)

    return ultAlertas


def tiempoReal(fecha, ubicacion, temperatura, humedad, presion, velocidadViento, milimetrosLluvia, puntoRocio, velocidadVehic, longitudVehic, existenciaHumo):
         
    calculos.AlertasLluvia(milimetrosLluvia, fecha, ubicacion)
    calculos.AlertasViento(velocidadViento, fecha, ubicacion)
    calculos.AlertasNiebla(temperatura, velocidadViento, presion, puntoRocio, fecha, ubicacion)
    calculos.AlertasHumo(existenciaHumo, fecha, ubicacion)
    calculos.AlertasVehiculos(velocidadVehic, longitudVehic, fecha, ubicacion)
    

@app.route('/estadisticasGenerales', methods=['POST'])
def estadisticasGenerales():
    if request.method=='POST':
        desde=request.form.get("desde")  
        hasta=request.form.get("hasta")  
        try:
            graficosNiveles = graficos.informeGeneralNivel(desde,hasta)
            graficosTipos = graficos.informeGeneralTipo(desde,hasta)
            global fechaDesde            
            fechaDesde=desde
            global fechaHasta           
            fechaHasta=hasta
            

        except Exception as e:
            error=str(e)
            return jsonify({'result':'error','error':error})
       
        return jsonify({'result':'success', 'imagenNiveles': graficosNiveles, 'imagenTipos': graficosTipos })


@app.route('/estadisticasPorTipo', methods=['POST'])
def estadisticasPorTipo():
    if request.method=='POST':
        tipo=request.form.get("tipo")  
        desde=request.form.get("desde")  
        hasta=request.form.get("hasta")  
        try:
            global fechaDesde            
            fechaDesde=desde
            global fechaHasta           
            fechaHasta=hasta
            global tipoRiesgo
            tipoRiesgo = tipo

            graficosNiveles = graficos.informeTipoNivel(tipo,desde,hasta)  
            graficosNivelesSemana = graficos.informeTipoNivelSemana(tipo,desde,hasta)        
            graficosNivelesMes = graficos.informeTipoNivelMes(tipo,desde,hasta) 

        except Exception as e:
            error=str(e)
            return jsonify({'result':'error','error':error})

        return jsonify({'result':'success', 'imagenNiveles': graficosNiveles , 'imagenNivelesSemana': graficosNivelesSemana, 'imagenNivelesMes': graficosNivelesMes })

@app.route('/estadisticasPorTramo', methods=['POST'])
def estadisticasPorTramo():
    if request.method=='POST':
        tramo=request.form.get("tramo")  
        desde=request.form.get("desde")  
        hasta=request.form.get("hasta")  
        try:
            global fechaDesde            
            fechaDesde=desde
            global fechaHasta           
            fechaHasta=hasta
            global tramoRuta
            tramoRuta = tramo

            graficosTramosTipos = graficos.informeTramoTipos(tramo,desde,hasta)
            graficosNiveles = graficos.informeTramoNivel(tramo,desde,hasta)  
            #graficosNivelesMes = graficos.informeTipoNivelMes(tipo,desde,hasta)  

        except Exception as e:
            error=str(e)
            return jsonify({'result':'error','error':error})

        return jsonify({'result':'success', 'imagenTramoTipos': graficosTramosTipos, 'imagenNiveles': graficosNiveles   })


@app.route('/estadisticasPorTramoTipo', methods=['POST'])
def estadisticasPorTramoTipo():
    if request.method=='POST':
        tramo=request.form.get("tramo")  
        tipo=request.form.get("tipo") 
        desde=request.form.get("desde")  
        hasta=request.form.get("hasta")  
        try:
           
            graficosTramosTiposMes = graficos.informeTramoTipoNivelMes(tramo,tipo,desde,hasta) 
            graficosTramosTiposSemana = graficos.informeTramoTipoNivelSemana(tramo,tipo,desde,hasta)
            global tipoRiesgo
            tipoRiesgo = tipo
            global tramoRuta
            tramoRuta = tramo
             

        except Exception as e:
            error=str(e)
            return jsonify({'result':'error','error':error})

        return jsonify({'result':'success', 'imagenTramoTiposMes': graficosTramosTiposMes, 'imagenTramoTiposSemana': graficosTramosTiposSemana   })


@app.route('/estadisticasUltimas24', methods=['POST'])
def estadisticasUltimas24():
    if request.method=='POST':

        tramo=request.form.get("tramo")           
        try:
            graficos24Lluvia = graficos.informe24Lluvia(tramo) 
            graficos24Niebla = graficos.informe24Niebla(tramo) 
            graficos24Humo = graficos.informe24Humo(tramo) 
            graficos24Viento = graficos.informe24Viento(tramo) 
            graficos24Animales = graficos.informe24Animales(tramo) 
            graficos24Vehiculos = graficos.informe24Vehiculos(tramo) 


        except Exception as e:
            error=str(e)
            return jsonify({'result':'error','error':error})

        return jsonify({'result':'success', 'imagenLluvia': graficos24Lluvia, 'imagenNiebla': graficos24Niebla, 'imagenHumo': graficos24Humo, 'imagenViento': graficos24Viento, 'imagenAnimales': graficos24Animales, 'imagenVehiculos': graficos24Vehiculos   })


@app.route('/buscadorAlertas', methods=['POST'])
def buscadorAlertas():
    tramo=request.form.get("tramo")  
    tipo=request.form.get("tipo") 
    desde=request.form.get("desde")  
    hasta=request.form.get("hasta")   
    try:

        Alertas = list(Alerta.buscarAlertas(tramo, tipo, desde, hasta))
        
        for i in Alertas:
            
            f = (i['fecha_inicio'])
            i['fecha_inicio'] = "{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}".format(f.day, f.month, f.year, f.hour, f.minute, f.second)

        datosJson = dumps(Alertas)

    except Exception as e:
        error=str(e)
        return jsonify({'result':'error','error':error})

    return jsonify({'result':'success', 'alertas': datosJson})


@app.route('/buscadorIncidentes', methods=['POST'])
def buscadorIncidentes():
    tramo=request.form.get("tramo")  
    tipo=request.form.get("tipo") 
    desde=request.form.get("desde")  
    hasta=request.form.get("hasta") 
    sinVisualizar=request.form.get("sinVisualizar")  
    sinAlertar=request.form.get("sinAlertar")  
    try:

        ListaIncidentes = list(Incidente.buscarIncidentes(tramo, tipo, desde, hasta,sinVisualizar,sinAlertar))
        
        for i in ListaIncidentes:
            
            f = (i['fecha_creacion'])
            i['fecha_creacion'] = "{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}".format(f.day, f.month, f.year, f.hour, f.minute, f.second)

        datosJson = dumps(ListaIncidentes)
        
    except Exception as e:
        error=str(e)
        return jsonify({'result':'error','error':error})

    return jsonify({'result':'success', 'incidentes': datosJson})


@app.route('/detalleIncidente', methods=['POST', 'GET'])
def detalleIncidente():
    idIncidente=request.args.get("id")

    IncidenteBuscado = Incidente.buscarIncidentePorId(idIncidente)
    TipoInc = IncidenteBuscado['tipo']
    TramoInc = IncidenteBuscado['tramo']
    Comentario  = IncidenteBuscado['comentario']
    f = IncidenteBuscado['fecha_creacion']
    FechaCreacion = "{:02d}-{:02d}-{} {:02d}:{:02d}:{:02d}".format(f.day, f.month, f.year, f.hour, f.minute, f.second)
    Estado  = IncidenteBuscado['estado']

    Tramos = list(Tramo.buscarTramos())
    Tipos = list(Tipo.buscarTipos())
    Niveles = list(Nivel.buscarNiveles())

    if Estado=='NoVisualizado':
        Incidente.modificarEstadoIncidente(idIncidente,"Visualizado")
    
    return render_template('detalleIncidente.html', idIncidente=idIncidente, tipo=TipoInc, tramo=TramoInc, comentario=Comentario, fechaCreacion=FechaCreacion, estado=Estado, Tramos=Tramos, Tipos=Tipos, Niveles=Niveles)



@app.route('/nuevoIncidente', methods=['POST'])
def nuevoIncidente():  
    tipo=request.form.get("tipo") 
    comentario=request.form.get("comentario")   
    tramo=request.form.get("tramo") 
    fecha_creacion= datetime.now()  
    try:
        nuevoIncidente = Incidente(tipo,comentario,tramo, fecha_creacion)
        nuevoIncidente.cargarIncidente()

    except Exception as e:
        error=str(e)
        return jsonify({'result':'error','error':error})

    return jsonify({'result':'success'})


def nuevoIncidenteMovil(tipo,comentario,tramo):  
    tipo=tipo
    comentario=comentario
    tramo=tramo
    fecha_creacion= datetime.now() 
    mensaje=""

    if(tipo==""):
        mensaje="Debe indicar el tipo de riesgo"
    elif(comentario==""):
        mensaje="Debe escribir un comentario"
    elif(tramo==""):
        mensaje="Debe indicar un tramo de la ruta"
    else:
        mensaje="ok"
        try:        
            nuevoIncidente = Incidente(tipo,comentario,tramo, fecha_creacion)
            nuevoIncidente.cargarIncidente()
            print("Se genero el incidente")

        except Exception as e:
            error=str(e)
            print(error)
    return mensaje

@app.route('/generarAlertaDesdeIncidente', methods=['POST'])
def generarAlertaDesdeIncidente(): 
    tipo=request.form.get("tipo") 
    nivel=request.form.get("nivel") 
    descripcion=request.form.get("descripcion")   
    tramo=request.form.get("tramo") 
    idIncidente= request.form.get("idIncidente")   
    fecha= datetime.now() 

    try:
        print(tipo)        
        nuevaAlerta = Alerta(tipo,descripcion, tramo, nivel, fecha, None)
        nuevaAlerta.cargarAlerta() 
        Incidente.modificarEstadoIncidente(idIncidente,"Alertado")


    except Exception as e:
        error=str(e)
        return jsonify({'result':'error','error':error})

    return jsonify({'result':'success'})

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method=='GET':
        return render_template('login.html')

    if request.method=='POST':        
        nombre=request.form.get("nombreUsuario") 
        contra=request.form.get("contrasena") 

    usu = Usuario.buscarUsuarioPorNombre(nombre)

    if usu == None:
        return render_template('login.html')

    else:
        correcto = Usuario.check_password(usu.contrasena,contra)


        if correcto:
            global sesion_usuario
            sesion_usuario = usu
            return redirect(url_for('novedades'))
           
        else: 
            return render_template('login.html')


global fechaDesde
fechaDesde1 = datetime.now()
fechaDesde= datetime(fechaDesde1.year, fechaDesde1.month, fechaDesde1.day, 00, 00, 00, 00000)
fechaDesde= "{}-{}-{}T{}:{}".format(fechaDesde.year, fechaDesde.strftime("%m"), fechaDesde.strftime("%d"),fechaDesde.strftime("%H"),fechaDesde.strftime("%M"))

global fechaHasta
fechaHasta1 = datetime.now()
fechaHasta= datetime(fechaHasta1.year, fechaHasta1.month, fechaHasta1.day, 23, 59, 59, 00000)
fechaHasta= "{}-{}-{}T{}:{}".format(fechaHasta.year, fechaHasta.strftime("%m"), fechaHasta.strftime("%d"),fechaHasta.strftime("%H"),fechaHasta.strftime("%M"))

global tipoRiesgo
tipoRiesgo = ""

global tramoRuta
tramoRuta = ""

global sesion_usuario
sesion_usuario = ""

if __name__ == "__main__":
    app.run(debug=False,
            port=5000)
       