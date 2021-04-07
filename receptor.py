import app

def recibirDatos(datos):
    
    print(datos)

    fecha = datos[0]
    ubicacion = datos[1]
    temperatura = datos[2]
    humedad =  datos[3] 
    presion = datos[4]
    velocidadViento = datos[5]
    milimetrosLluvia = datos[6]      
    puntoRocio =  datos[7]
    velocidadVehic =  datos[8]
    longitudVehic = datos[9]
    existenciaHumo = datos[10]

    app.tiempoReal(fecha, ubicacion, temperatura, humedad, presion, velocidadViento, milimetrosLluvia, puntoRocio, velocidadVehic, longitudVehic, existenciaHumo)

    