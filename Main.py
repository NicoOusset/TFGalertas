import kivy
from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

import app

class Contenedor(Widget):
    tipo = ObjectProperty(None)
    comentario = ObjectProperty(None)
    tramo = ObjectProperty(None)
    
    def generarIncidente(self):
        tipoRiesgo = self.tipo.text
        comentarioUsuario = self.comentario.text
        tramoRuta = self.tramo.text
        mensaje = app.nuevoIncidenteMovil(tipoRiesgo,comentarioUsuario,tramoRuta)
        self.tipo.text = ""
        self.comentario.text = ""
        self.tramo.text = ""
        print(mensaje)



''' class contenedor2(GridLayout):
    def __init__(self,**kwargs):
        super(contenedor, self).__init__(**kwargs)
        self.cols = 1
        self.inside = GridLayout()
        self.inside.cols = 2
        
        self.inside.add_widget(Label(text="Tipo: "))
        self.tipo= TextInput(multiline=False)
        self.inside.add_widget(self.tipo)

        self.inside.add_widget(Label(text="Comentario: "))
        self.comentario= TextInput(multiline=False)
        self.inside.add_widget(self.comentario)

        self.inside.add_widget(Label(text="Tramo: "))
        self.tramo= TextInput(multiline=False)
        self.inside.add_widget(self.tramo)

        self.add_widget(self.inside)
        
        self.generar= Button(text="Generar incidente", font_size=40)
        self.generar.bind(on_press=self.generarIncidente)
        self.add_widget(self.generar)

    def generarIncidente(self, instance):
        tipo = self.tipo.text
        comentario = self.comentario.text
        tramo = self.tramo.text
        app.nuevoIncidente2(tipo,comentario,tramo)
       
        self.tipo.text = ""
        self.comentario.text = ""
        self.tramo.text = "" '''


class GenerarIncidentes(App):
    def build(self):
        return Contenedor()

if __name__ == "__main__":
    GenerarIncidentes().run() 