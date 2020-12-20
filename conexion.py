import pymongo

class Conexion:      

    def conectar():     
        MONGODB_HOST = '127.0.0.1'
        MONGODB_PORT = '27017'
        MONGODB_TIMEOUT = 1000           

        URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT +  "/"
        
        try:
            client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
            client.server_info()
            print('Conectado al servidor MongoDB %s' % (MONGODB_HOST))
            print("---------------------------------------------------") 
            client.close()
            return client

        except pymongo.errors.ServerSelectionTimeoutError as error:
            print('Error en la conexion a MongoDB: %s' % error)
        except pymongo.errors.ConnectionFailure as error:
            print('Error en la conexion a MongoDB: %s' % error)