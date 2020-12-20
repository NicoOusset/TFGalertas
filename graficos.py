from alerta import Alerta
from bson.json_util import dumps
import lectorCSV
import calculos
import pandas as pd
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, json, Response

import numpy as np
import os
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64


def informeGeneralTipo(desde, hasta):
    
    tipos = []
    cantidades = []
    plt.clf() 
    resultados = Alerta.informeGeneralTipo(desde,hasta)
    tipos = resultados[0]
    cantidades = resultados[1]
    if(tipos==[]):
        print("sin informacion")
        plot_url = "SinDatos"
    else:
        print("con info")    
        colores = ['y','r','b','m','g']
        img= None
        img = io.BytesIO()
        #plt.title("tipos")
        
        plt.bar(tipos, cantidades, width = 0.4)
        
        print(tipos)
        print(cantidades)
        
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def informeGeneralNivel(desde, hasta):

    niveles = []
    cantidades = []
    plt.clf() 
    resultados = Alerta.informeGeneralNivel(desde,hasta)
    niveles = resultados[0]
    cantidades = resultados[1]
    if(niveles==[]):
        print("sin informacion")
        plot_url = "SinDatos"

    else:
        colores = ['y','r','b','m','g']
        img= None
        img = io.BytesIO()
        #plt.title("niveles")
        
        plt.pie(cantidades, labels = niveles, colors = colores, autopct='%1.1f%%',  startangle=90)
        
        print(niveles)
        print(cantidades)
        
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def informeTipoNivel(tipo, desde, hasta):
    
    niveles = []
    cantidades = []
    plt.clf() 
    resultados = Alerta.informePorTipoNivel(tipo,desde,hasta)
    niveles = resultados[0]
    cantidades = resultados[1]
    if(niveles==[]):
        print("sin informacion")
        plot_url = "SinDatos"

    else:
        colores = ['y','r','b','m','g']
        img= None
        img = io.BytesIO()
        #plt.title("niveles")
        
        plt.pie(cantidades, labels = niveles, colors = colores, autopct='%1.1f%%',  startangle=90)
        
        print(niveles)
        print(cantidades)
        
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def informeTipoNivelSemana(tipo, desde, hasta):
    
    dias = []
    niveles = []
    cantidades = []
    
    resultados = Alerta.informePorTipoNivelSemana(tipo,desde,hasta)
    dias = resultados[0]
    niveles = resultados[1]
    cantidades = resultados[2]

    semana = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']
    leve = [0,0,0,0,0,0,0]
    moderado = [0,0,0,0,0,0,0]
    alto = [0,0,0,0,0,0,0]
    extrema = [0,0,0,0,0,0,0]
 
    for j in range(len(semana)):
        for i in range(len(dias)): 
            
            if(dias[i]==(j+1)):
                if(niveles[i]=='leve'):
                    leve[j] = cantidades[i]
            
                if(niveles[i]=='moderado'):
                    moderado[j] = cantidades[i]
                
                if(niveles[i]=='alto'):
                    alto[j] = cantidades[i]
            
                if(niveles[i]=='extrema'):
                    extrema[j] = cantidades[i]
            
    plt.clf() 

    if(niveles==[]):
        print("sin informacion")
        plot_url = "SinDatos"

    else:
        w = 0.1
        colores = ['y','r','b','m','g']
        img= None
        img = io.BytesIO()
        #plt.title("niveles")

        bar1 = np.arange(len(semana))
        bar2 = [i+w for i in bar1] 
        bar3 = [i+w for i in bar2] 
        bar4 = [i+w for i in bar3] 


        plt.bar(bar1, leve,w,label="leve")
        plt.bar(bar2, moderado,w,label="moderado")
        plt.bar(bar3, alto,w,label="alto")
        plt.bar(bar4, extrema,w,label="extrema")
        plt.xticks(bar1+w, semana)
        plt.legend()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def informeTipoNivelMes(tipo, desde, hasta):
    
    meses = []
    niveles = []
    cantidades = []

    resultados = Alerta.informePorTipoNivelMes(tipo,desde,hasta)
    meses = resultados[0]
    niveles = resultados[1]
    cantidades = resultados[2]

    mes = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    leve = [0,0,0,0,0,0,0,0,0,0,0,0]
    moderado = [0,0,0,0,0,0,0,0,0,0,0,0]
    alto = [0,0,0,0,0,0,0,0,0,0,0,0]
    extrema = [0,0,0,0,0,0,0,0,0,0,0,0]    
    

    for j in range(len(mes)):
        for i in range(len(meses)): 
            
            if(meses[i]==(j+1)):
                if(niveles[i]=='leve'):
                    leve[j] = cantidades[i]
            
                if(niveles[i]=='moderado'):
                    moderado[j] = cantidades[i]
                
                if(niveles[i]=='alto'):
                    alto[j] = cantidades[i]
            
                if(niveles[i]=='extrema'):
                    extrema[j] = cantidades[i]              

    plt.clf() 
    if(niveles==[]):
        print("sin informacion")
        plot_url = "SinDatos"

    else:
        w = 0.1
        colores = ['y','r','b','m','g']
        img= None
        img = io.BytesIO()
        #plt.title("niveles")

        bar1 = np.arange(len(mes))
        bar2 = [i+w for i in bar1] 
        bar3 = [i+w for i in bar2] 
        bar4 = [i+w for i in bar3] 


        plt.bar(bar1, leve,w,label="leve")
        plt.bar(bar2, moderado,w,label="moderado")
        plt.bar(bar3, alto,w,label="alto")
        plt.bar(bar4, extrema,w,label="extrema")
        plt.xticks(bar1+w, mes)
        plt.legend()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url