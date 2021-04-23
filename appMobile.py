from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList, ThreeLineListItem
from kivy.uix.scrollview import ScrollView
import app
import time
import threading
from kivymd.theming import ThemeManager

screen_helper = """
ScreenManager:
    Home:
    PantallaGenerarIncidentes:
    PantallaNovedades:

<Home>:
    name: 'home'
    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            canvas:
                Rectangle:
                    source: 'static/logo.png'
                    pos: (((self.parent.size[0])/2)+200,self.pos[1])
                    size: (40, 60)
            title: "Alertas de riesgos Ruta Nº38"
            elevation: 10

        MDLabel:
            text: ""
        MDRectangleFlatButton:
            text: 'Novedades'
            
            pos_hint: {'center_x':0.5,'center_y':0.6}
            on_press: root.manager.current = 'novedad'
                
        MDLabel:
            text: ""

        MDRectangleFlatButton:
            text: 'Generar Incidente'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            on_press: root.manager.current = 'incidente'
        
        MDLabel:
            text: ""
            

    
<PantallaGenerarIncidentes>:
    name: 'incidente'
    
    tipo : tipo
    comentario : comentario
    tramo: tramo

    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            canvas:
                Rectangle:
                    source: 'static/logo.png'
                    pos: (((self.parent.size[0])/2)+200,self.pos[1])
                    size: (40, 60)
            title: "Alertas de riesgos Ruta Nº38 - GENERAR UN INCIDENTE"
            elevation: 10

        MDLabel:
            text: ''      
       

        MDTextField:
            id: tipo
            hint_text: "Tipo de Riesgo"        
            helper_text_mode: "on_focus"
            icon_right: "weather-pouring"
            icon_right_color: app.theme_cls.primary_color
            pos_hint:{'center_x': 0.5, 'center_y': 0.7}
            size_hint_x:None
            width:300
        
        MDTextField:
            id: comentario
            hint_text: "Comentario"        
            helper_text_mode: "on_focus"
            icon_right: "comment-alert"
            icon_right_color: app.theme_cls.primary_color
            pos_hint:{'center_x': 0.5, 'center_y': 0.5}
            size_hint_x:None
            width:300


        MDTextField:
            id: tramo
            hint_text: "Tramo de la ruta"        
            helper_text_mode: "on_focus"
            icon_right: "map-marker"
            icon_right_color: app.theme_cls.primary_color
            pos_hint:{'center_x': 0.5, 'center_y': 0.3}
            size_hint_x:None
            width:300
        
        
        MDLabel:
            text: ""

        MDRectangleFlatButton:
            text: 'Generar'
            pos_hint: {'center_x':0.5,'center_y':0.1}
            on_press: root.generarIncidente()
            on_release: root.manager.current = 'home'

        MDLabel:
            text: ""
        MDRectangleFlatButton:
            text: 'Volver'
            pos_hint: {'center_x':0.5,'center_y':0.05}
            on_press: root.manager.current = 'home'

        MDLabel:
            text: ""
            
<PantallaNovedades>:
    name: 'novedad'
    on_enter: root.novedades()
    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            canvas:
                Rectangle:
                    source: 'static/logo.png'
                    pos: (((self.parent.size[0])/2)+200,self.pos[1])
                    size: (40, 60)

            title: "Alertas de riesgos Ruta Nº38 - NOVEDADES"
            elevation: 10
            


        ScrollView:
            MDList:
                id: container
                pos_hint:{'center_x': 0.5, 'center_y': 0.3}    

       
        MDIconButton:
            icon: "static/logo.png"
            size: (40, 60)
            pos_hint: {'center_x':0.5,'center_y':0.3}
            on_press: root.novedades()
                    
        MDRectangleFlatButton:
            text: 'Volver'
            pos_hint: {'center_x':0.5,'center_y':0.1}
            on_press: root.manager.current = 'home'
       
"""


class Home(Screen):
    pass  
    

class PantallaGenerarIncidentes(Screen):
    tipo = ObjectProperty(None)
    comentario = ObjectProperty(None)
    tramo = ObjectProperty(None)
    
    def generarIncidente(self):
        tipoRiesgo = self.tipo.text
        comentarioUsuario = self.comentario.text
        tramoRuta = self.tramo.text
        print(tipoRiesgo)
        mensaje = app.nuevoIncidenteMovil(tipoRiesgo,comentarioUsuario,tramoRuta)
        self.tipo.text = ""
        self.comentario.text = ""
        self.tramo.text = ""
        print(mensaje)


class PantallaNovedades(Screen):

    def novedades(self):

        self.ids.container.clear_widgets()
        alertas = app.UltimasAlertasMobile()
        for i in alertas:
            itemi = ThreeLineListItem(text="Tipo de Riesgo: "+str(i['tipo']) + " - Nivel: "+str(i['nivel']),secondary_text=str(i['descripcion']), tertiary_text="Tramo de la ruta: "+str(i['tramo'])+" - Fecha: "+str(i['fecha_inicio']))
            self.ids.container.add_widget(itemi)


sm = ScreenManager()
sm.add_widget(Home(name='home'))
sm.add_widget(PantallaGenerarIncidentes(name='incidente'))
sm.add_widget(PantallaNovedades(name='novedad'))


class Alertas_38_Mobile(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


Alertas_38_Mobile().run()