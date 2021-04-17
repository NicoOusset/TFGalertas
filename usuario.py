from werkzeug.security import generate_password_hash, check_password_hash
""" from flask_login import UserMixin, current_user, login_user, logout_user, login_required
from flask_login import LoginManager
from flask import Flask """
#from app.forms import Login
from datetime import datetime
from conexion import Conexion
import pymongo


db = 'tfgAlertas'
cliente = Conexion.conectar()

""" app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
login.init_app(app)
 """

class Usuario():
    def __init__(self, nombreUsuario, nombre, apellido, contrasena, tipo):
        self.nombreUsuario = nombreUsuario
        self.nombre = nombre
        self.apellido = apellido       
        self.contrasena = contrasena
        self.tipo = tipo
        self.fechaCreacion = datetime.now() 

    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(contrasena, contrasenaNueva):
        return check_password_hash(contrasena, contrasenaNueva)

   
    def is_authenticated():
        return True


    def buscarUsuarioPorNombre(nombreUsuario):
        u = cliente[db]['Usuarios'].find_one({"nombreUsuario": nombreUsuario})
        if not u:
            return None
        usu = Usuario(u['nombreUsuario'],u['nombre'],u['apellido'],u['contrasena'],u['tipo'])
        return usu

    def generarUsuario(self):
        database_entry = {}
        database_entry['nombreUsuario'] = self.nombreUsuario
        database_entry['nombre'] = self.nombre
        database_entry['apellido'] = self.apellido
        database_entry['contrasena'] = generate_password_hash(self.contrasena)
        database_entry['tipo'] = self.tipo
        database_entry['fechaCreacion'] = self.fechaCreacion
              
        try:
            destination = 'Usuarios'
            collection = cliente[db]['Usuarios']
            collection.insert_one(database_entry)

        except Exception as error:
            print ("Error cargando Usuario: %s" % str(error))


    def __repr__(self):
        return '<User {}>'.format(self.nombre)



""" usu = Usuario("NicoOusset","Nicolas", "Ousset", "alertas38", "admin")
usu.generarUsuario() """

""" @app.route('/')
def index():

    #------ buscar el usuario por el nombre de usurio --------
    usu = Usuario.load_user("NicoOusset")

    # --------   poner un if para que se fije si existe o no ese nombre
    if usu == None:
        print("No existe ese nombre de usuario")
    else:
        contraseniaNueva = "alertas38"
        
        print(Usuario.contrasena)
        #-------- se fija que las contras sean iguales------
        correcto = User.check_password(Usuario.contrasena,contraseniaNueva)
        print(correcto)

        if correcto:
            print("podes entrar")
            
            login_user(usu)

        else: 
            print("no podes entrar")

    if current_user.is_authenticated:
        print("vos podes creer que esto funca??")

    return 'algo' """

""" app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

if __name__ == "__main__":
    app.run(debug=True,
            port=5000) """




