#import pymongo
from conexion import Conexion
from datetime import datetime
from alerta import Alerta

'''
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = '27017'
MONGODB_TIMEOUT = 1000
MONGODB_DATABASE = 'tfgAlertas'

URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT +  "/"

try:
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    client.server_info()
    print('OK -- Connected to MongoDB at server %s' % (MONGODB_HOST)) 
    client.close()
except pymongo.errors.ServerSelectionTimeoutError as error:
    print('Error with MongoDB connection: %s' % error)
except pymongo.errors.ConnectionFailure as error:
    print('Could not connect to MongoDB: %s' % error)

'''
MONGODB_DATABASE = 'tfgAlertas'
client = Conexion.conectar()

database_entry = {}
database_entry['name'] = 'John'
database_entry['surname'] = 'Wick'
database_entry['city'] = 'New York'
 
# or equivalent database_entry={'name':'John', 'surname':'Wick', 'city':'New York'}
def testInsert():  
    try:
        destination = 'USERS'
        collection = client[MONGODB_DATABASE][destination]
        collection.insert_one(database_entry)
        print ("Data saved at %s collection in %s database: %s" % (destination, MONGODB_DATABASE, database_entry))
    except Exception as error:
        print ("Error saving data: %s" % str(error))


def cargarAlerta(tipo,descripcion,tramo,nivel):

    database_entry = {}
    database_entry['tipo'] = tipo
    database_entry['descripcion'] = descripcion
    database_entry['tramo'] = tramo
    database_entry['nivel'] = nivel
    database_entry['fecha'] = datetime.now()
    
    try:
        destination = 'Alertas'
        collection = client[MONGODB_DATABASE][destination]
        collection.insert_one(database_entry)
    except Exception as error:
        print ("Error saving data: %s" % str(error))


#modificar = client[MONGODB_DATABASE]['Alertas'].update_one({'tramo': 'aguilares-consepcion'}, {'$set': {'tramo': 'aguilares-concepcion'}})

a = Alerta('niebla','poca niebla', 'aguilares-concepcion', 'leve')
a.cargarAlerta(client,MONGODB_DATABASE)

#resultado = client[MONGODB_DATABASE]['Alertas'].find({'tramo': 'aguilares-concepcion'})
resultado = Alerta.buscarAlertas(client,MONGODB_DATABASE)

for r in resultado:
    print(r['tipo'])


'''       
tiempoReal(16,b,'concepcion-rio')  
tiempoReal(36,b,'concepcion-rio')

tiempoReal(50,b,'concepcion-rio')

tiempoReal(65,b,'concepcion-rio')

'''


def actualizarAlerta():
        cliente[db]['Alertas'].update_many({
            'tramo': "concepcion-rio"
        }, {'$set':
        {
            'tramo': "Concepcion - Rio Seco"
        }})