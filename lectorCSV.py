import pandas as pd
import app
from datetime import datetime
import time
import numpy as np

def leerCSV(nombre):

    nombreCSV = nombre+'.csv'
    print("Leyendo el csv "+nombreCSV)

    df = pd.read_csv(nombreCSV, sep=',', index_col=0, encoding = "ISO-8859-1")
    df = df.replace({np.nan: None})
    print(len(df))

    print(df.head())
            #range(len(df))
    for i in range(len(df)):

        #fecha, ubicacion, temperatura, humedad, presion, velocidadViento, milimetrosLluvia, puntoRocio, velocidadVehic, longitudVehic
        #niebla lluvia humo viento animales vehiculos
        print("bucle")
        fechaLectura = df.loc[i, "Fecha"]
        print(fechaLectura)
        ubicacion = df.loc[i, "Ubicacion"]
        temperatura = df.loc[i, "Temperatura"]   
        humedad =  df.loc[i, "Humedad"]     
        presion =  df.loc[i, "Presion"]
        velocidadViento =  df.loc[i, "VelocidadViento"]
        milimetrosLluvia = df.loc[i, "Precipitacion"]        
        puntoRocio =  df.loc[i, "PuntoRocio"]
        velocidadVehic =  df.loc[i, "VelocidadVehiculo"]
        longitudVehic =  df.loc[i, "LongitudVehiculo"]
        
        fecha = datetime.strptime(fechaLectura, '%Y-%m-%d %H:%M:%S.%f')
        print(fecha)

        #app.tiempoReal(fecha, ubicacion, 1, 1, 1, 1, milimetrosLluvia, puntoRocio, 1, 1)
        app.tiempoReal(fecha, ubicacion, temperatura, humedad, presion, velocidadViento, milimetrosLluvia, puntoRocio, velocidadVehic, longitudVehic)
        time.sleep(1)
        #print(milimetrosLluvia , "---", fechaLectura)    
        #print(df.loc[i, "lluvia"], df.loc[i, "fechas"]) 