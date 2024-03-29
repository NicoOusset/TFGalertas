from alerta import Alerta

def NivelRiesgoLluvia(milimetrosLluvia):

    nivel = "";

    if(milimetrosLluvia!=None):

        milimetrosLluvia=float(milimetrosLluvia)
        if(milimetrosLluvia < 3):
            nivel = "nulo"
        if(milimetrosLluvia >= 3 and milimetrosLluvia < 16):
            nivel = "leve" 
        if(milimetrosLluvia >= 16 and milimetrosLluvia < 31):
            nivel = "moderado"
        if(milimetrosLluvia >= 31 and milimetrosLluvia < 60):
            nivel = "alto"
        if(milimetrosLluvia >= 60):
            nivel = "extrema"

    else:
        nivel = "sin datos"

    return nivel  
    

def NivelRiesgoViento(velocidadViento):
    
    nivel = "";
    
    if(velocidadViento!=None):

        velocidadViento=float(velocidadViento)
        if(velocidadViento < 29):
            nivel = "nulo"
        if(velocidadViento >= 29 and velocidadViento < 39):
            nivel = "leve" 
        if(velocidadViento >= 39 and velocidadViento < 50):
            nivel = "moderado"
        if(velocidadViento >= 50 and velocidadViento < 62):
            nivel = "alto"
        if(velocidadViento >= 62):
            nivel = "extrema"

    else:
        nivel = "sin datos"    

    return nivel  


def NivelRiesgoNiebla(temperatura, velocidadViento, presion, puntoRocio):
    
    nivel = "";

    if(temperatura!=None and velocidadViento!=None and presion!=None and puntoRocio!=None):

        nivel = "nulo"

        presion=float(presion)
        velocidadViento=float(velocidadViento)
        temperatura=float(temperatura)
        puntoRocio=float(puntoRocio)

        if(presion > 1020):
            if(velocidadViento < 10):
                if(temperatura < 12):
                    if((temperatura-puntoRocio) <= 1):
                        nivel = "alto"

    else:
        nivel = "sin datos"    

    return nivel  


def NivelRiesgoHumo(humo):
    
    nivel = "";
    
    if(humo!=None):
        humo=float(humo)
        if(humo == 0):
            nivel = "nulo"       
        if(humo == 1):
            nivel = "alto"      
    else:
        nivel = "sin datos"    

    return nivel  


def NivelRiesgoVehiculos(velocidadVehic, longitudVehic):
    
    nivel = "";

    if(velocidadVehic!=None and longitudVehic!=None):

        nivel = "nulo"

        velocidadVehic=float(velocidadVehic)
        longitudVehic=float(longitudVehic)
        
        if(longitudVehic !=0 and longitudVehic < 5):
            if(velocidadVehic  !=0 and velocidadVehic < 20):
                nivel = "alto" 
            elif(velocidadVehic < 40):
                nivel = "leve" 
            elif(velocidadVehic < 80):
                nivel = "nulo" 
            elif(velocidadVehic >= 80):
                nivel = "nulo"

        elif(longitudVehic < 10):
            if(velocidadVehic  !=0 and velocidadVehic < 20):
                nivel = "alto" 
            elif(velocidadVehic < 40):
                nivel = "moderado" 
            elif(velocidadVehic < 80):
                nivel = "nulo" 
            elif(velocidadVehic >= 80):
                nivel = "nulo"

        elif(longitudVehic < 20):
            if(velocidadVehic  !=0 and velocidadVehic < 20):
                nivel = "extrema" 
            elif(velocidadVehic < 40):
                nivel = "alto" 
            elif(velocidadVehic < 80):
                nivel = "leve" 
            elif(velocidadVehic >= 80):
                nivel = "nulo"

        elif(longitudVehic >= 20):
            if(velocidadVehic  !=0 and velocidadVehic < 20):
                nivel = "extrema" 
            elif(velocidadVehic < 40):
                nivel = "extrema" 
            elif(velocidadVehic < 80):
                nivel = "leve" 
            elif(velocidadVehic >= 80):
                nivel = "nulo"

    else:
        nivel = "sin datos"    

    return nivel

def AlertasLluvia(milimetrosLluvia, fecha, ubicacion):

    nivel= NivelRiesgoLluvia(milimetrosLluvia)

    if(nivel!="sin datos"):        

        AlertaActiva = Alerta.buscarAlertaActiva('lluvia',ubicacion)  
        descr = 'Luvia '+nivel+' de '+str(milimetrosLluvia)+' milimetros'
        descripcion = descr
    
        if(AlertaActiva==""):

            print("No hay alertas activas para ese tipo y ubicacion")

            if(nivel!="nulo"):
                nuevaAlerta = Alerta('lluvia',descripcion, ubicacion, nivel, fecha, None)
                nuevaAlerta.cargarAlerta() 

                return "alerta super nueva"         

                print("NUEVA ALERTA PARA LLUVIA, NIVEL: "+nivel)
                print("-----------------------------")

            else:
                print("No hay nueva alerta por ser nivel de lluvia Nulo") 
                print("-----------------------------")
                return ""

        else:

            print("El nivel de la alerta activa es: ",AlertaActiva['nivel'])
            print("nivel nuevo: ",nivel) 

            if(nivel!=AlertaActiva['nivel']):
                
                idAlertaAnterior = AlertaActiva['_id']
                Alerta.inactivarAlerta(idAlertaAnterior,fecha)            
                print("Se inactiva Alerta anterior")

                if(nivel!="nulo"):
                    nuevaAlerta = Alerta('lluvia',descripcion, ubicacion, nivel, fecha, None)
                    nuevaAlerta.cargarAlerta()                

                    print("NUEVA ALERTA PARA LLUVIA, NIVEL: "+nivel)
                    print("-----------------------------") 
                    return "alerta super nueva"

                else:
                    print("No hay nueva alerta por ser nivel de lluvia Nulo") 
                    print("-----------------------------") 
                    return ""  
                
            else:
                print("No hay que actualizar alerta")
                print("-----------------------------") 
                return ""

    else:
        print("No hay DATOS")
        print("-----------------------------")
        return ""
        

def AlertasViento(velocidadViento, fecha, ubicacion):
    
    nivel= NivelRiesgoViento(velocidadViento)

    if(nivel!="sin datos"): 

        AlertaActiva = Alerta.buscarAlertaActiva('viento',ubicacion)   
        descr = 'Viento '+nivel+' de '+str(velocidadViento)+' velocidad (km/h)'
        descripcion = descr
        
        if(AlertaActiva==""):

            print("No hay alertas activas para Viento en esa ubicacion")

            if(nivel != "nulo"):
                nuevaAlerta = Alerta('viento',descripcion, ubicacion, nivel, fecha, None)
                nuevaAlerta.cargarAlerta()           

                print("NUEVA ALERTA PARA VIENTO, NIVEL: "+nivel)
                print("-----------------------------")

            else:
                print("No hay nueva alerta por ser nivel de Viento Nulo") 
                print("-----------------------------")

        else:

            print("El nivel de la alerta activa de VIENTO es: ",AlertaActiva['nivel'])
            print("nivel nuevo de VIENTO: ",nivel) 

            if(nivel!=AlertaActiva['nivel']):
                
                idAlertaAnterior = AlertaActiva['_id']
                Alerta.inactivarAlerta(idAlertaAnterior,fecha)            
                print("Se inactiva Alerta anterior")

                if(nivel!="nulo"):
                    nuevaAlerta = Alerta('viento',descripcion, ubicacion, nivel, fecha, None)
                    nuevaAlerta.cargarAlerta()                

                    print("NUEVA ALERTA PARA VIENTO, NIVEL: "+nivel)
                    print("-----------------------------") 

                else:
                    print("No hay nueva alerta por ser nivel de Viento Nulo") 
                    print("-----------------------------")   
                
            else:
                print("No hay que actualizar alerta")
                print("-----------------------------") 

    else:
        print("No hay DATOS")
        print("-----------------------------") 


def AlertasNiebla(temperatura, velocidadViento, presion, puntoRocio, fecha, ubicacion):
    
    nivel = NivelRiesgoNiebla(temperatura, velocidadViento, presion, puntoRocio)

    if(nivel!="sin datos"): 

        AlertaActiva = Alerta.buscarAlertaActiva('niebla',ubicacion)        
        descripcion = 'Hay niebla que impide la visión'

        if(AlertaActiva==""):

            print("No hay alertas activas para Niebla en esa ubicacion")

            if(nivel != "nulo"):
                nuevaAlerta = Alerta('niebla',descripcion, ubicacion, nivel, fecha, None)
                nuevaAlerta.cargarAlerta()           

                print("NUEVA ALERTA PARA NIEBLA, NIVEL: "+nivel)
                print("-----------------------------")

            else:
                print("No hay nueva alerta por ser nivel de NIEBLA Nulo") 
                print("-----------------------------")

        else:

            print("El nivel de la alerta activa de NIEBLA es: ",AlertaActiva['nivel'])
            print("nivel nuevo de NIEBLA: ",nivel) 

            if(nivel!=AlertaActiva['nivel']):
                
                idAlertaAnterior = AlertaActiva['_id']
                Alerta.inactivarAlerta(idAlertaAnterior,fecha)            
                print("Se inactiva Alerta anterior")

                if(nivel!="nulo"):
                    nuevaAlerta = Alerta('niebla', descripcion, ubicacion, nivel, fecha, None)
                    nuevaAlerta.cargarAlerta()                

                    print("NUEVA ALERTA PARA NIEBLA, NIVEL: "+nivel)
                    print("-----------------------------") 

                else:
                    print("No hay nueva alerta por ser nivel de NIEBLA Nulo") 
                    print("-----------------------------")   
                
            else:
                print("No hay que actualizar alerta")
                print("-----------------------------") 

    else:
        print("No hay DATOS")
        print("-----------------------------") 



def AlertasHumo(humo, fecha, ubicacion):
    
    nivel = NivelRiesgoHumo(humo)

    if(nivel!="sin datos"): 

        AlertaActiva = Alerta.buscarAlertaActiva('humo',ubicacion)        
        descripcion = 'Hay humo que impide la visión'

        if(AlertaActiva==""):

            print("No hay alertas activas para Humo en esa ubicacion")

            if(nivel != "nulo"):
                nuevaAlerta = Alerta('humo',descripcion, ubicacion, nivel, fecha, None)
                nuevaAlerta.cargarAlerta()           

                print("NUEVA ALERTA PARA HUMO, NIVEL: "+nivel)
                print("-----------------------------")

            else:
                print("No hay nueva alerta por ser nivel de HUMO Nulo") 
                print("-----------------------------")

        else:

            print("El nivel de la alerta activa de HUMO es: ",AlertaActiva['nivel'])
            print("nivel nuevo de HUMO: ",nivel) 

            if(nivel!=AlertaActiva['nivel']):
                
                idAlertaAnterior = AlertaActiva['_id']
                Alerta.inactivarAlerta(idAlertaAnterior,fecha)            
                print("Se inactiva Alerta anterior")

                if(nivel!="nulo"):
                    nuevaAlerta = Alerta('humo', descripcion, ubicacion, nivel, fecha, None)
                    nuevaAlerta.cargarAlerta()                

                    print("NUEVA ALERTA PARA HUMO, NIVEL: "+nivel)
                    print("-----------------------------") 

                else:
                    print("No hay nueva alerta por ser nivel de HUMO Nulo") 
                    print("-----------------------------")   
                
            else:
                print("No hay que actualizar alerta")
                print("-----------------------------") 

    else:
        print("No hay DATOS")
        print("-----------------------------") 


def AlertasVehiculos(velocidadVehic, longitudVehic, fecha, ubicacion):
    
    nivel = NivelRiesgoVehiculos(velocidadVehic, longitudVehic)

    if(nivel!="sin datos"): 

        AlertaActiva = Alerta.buscarAlertaActiva('vehiculos',ubicacion)        
        descripcion = 'Un vehiculo de '+str(longitudVehic)+'m de largo transita a '+str(velocidadVehic)+' km/h'

        if(AlertaActiva==""):

            print("No hay alertas activas para vehiculos lentos en esa ubicacion")

            if(nivel != "nulo"):
                nuevaAlerta = Alerta('vehiculos',descripcion, ubicacion, nivel, fecha, None)
                nuevaAlerta.cargarAlerta()           

                print("NUEVA ALERTA PARA VEHICULOS, NIVEL: "+nivel)
                print("-----------------------------")

            else:
                print("No hay nueva alerta por ser nivel de VEHICULOS Nulo") 
                print("-----------------------------")

        else:

            print("El nivel de la alerta activa de VEHICULOS es: ",AlertaActiva['nivel'])
            print("nivel nuevo de VEHICULOS: ",nivel) 

            if(nivel!=AlertaActiva['nivel']):
                
                idAlertaAnterior = AlertaActiva['_id']
                Alerta.inactivarAlerta(idAlertaAnterior,fecha)            
                print("Se inactiva Alerta anterior")

                if(nivel!="nulo"):
                    nuevaAlerta = Alerta('vehiculos', descripcion, ubicacion, nivel, fecha, None)
                    nuevaAlerta.cargarAlerta()                

                    print("NUEVA ALERTA PARA VEHICULOS, NIVEL: "+nivel)
                    print("-----------------------------") 

                else:
                    print("No hay nueva alerta por ser nivel de VEHICULOS Nulo") 
                    print("-----------------------------")   
                
            else:
                print("No hay que actualizar alerta")
                print("-----------------------------") 

    else:
        print("No hay DATOS")
        print("-----------------------------") 