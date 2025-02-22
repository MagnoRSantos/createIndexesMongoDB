# -*- coding: utf-8 -*-

import os
import dotenv
from pymongo import MongoClient
from datetime import datetime
import json

### Variaveis do local do script e log mongodb
dirapp = os.path.dirname(os.path.realpath(__file__))

## Carrega os valores do .env
dotenvFile = os.path.join(dirapp, '.env.dev')
dotenv.load_dotenv(dotenvFile)

def createIndexes():

    try:
       
        USERNAME_MONGODB = os.getenv("USERNAME_MONGODB")
        PASSWORD_MONGODB = os.getenv("PASSWORD_MONGODB")
        SERVER_MONGODB   = os.getenv("SERVER_MONGODB")
        DBAUTHDB_MONGODB = os.getenv("DBAUTHDB_MONGODB")
        DBMODEL_MONGODB  = os.getenv("DBMODEL_MONGODB")
        DBTARGET_MONGODB = os.getenv("DBTARGET_MONGODB")

        resultCreatedIndex = ''


        ## Conectar aos bancos de dados
        connstr = 'mongodb://{0}:{1}@{2}/{3}'.format(USERNAME_MONGODB, PASSWORD_MONGODB, SERVER_MONGODB, DBAUTHDB_MONGODB)
        
        with MongoClient(connstr) as client:

            db_model = client[DBMODEL_MONGODB]
            db_target = client[DBTARGET_MONGODB]
            
            index_model = list(db_model.get_collection('movies').list_indexes())

            index_commands = []
 
            ## Obtem os indices do modelRegras respeitando a ordenacao deles
            ## adiciona os indices em uma lista para uso posterior
            for index in index_model:
                if index['name'] != '_id_': ## ignora o indice padrao _id_
                    
                    sorted_index_key = list(index['key'].items())

                    index_commands.append({
                        "key": dict(sorted_index_key), ## Campos indexados
                        "name": index['name'], ## Nome do indice
                    })

            
            ## Cria os indices no banco de dados target com o comando db_target.command para uso de commitQuorum
            resultCreatedIndex = db_target.command({
                "createIndexes": "movies",
                "indexes": index_commands,
                #"commitQuorum": 1 ## Define o quorum no momento da criacao do indice
            })
            

    except Exception as e:
        msgException = "Error: {0}".format(e)
        msgLog = 'Obter dados MongoDB [ServerStatusMongoDB] [Erro]: {0}'.format(msgException)
        print(msgLog)

    finally:
          
        if resultCreatedIndex is not None:
            return resultCreatedIndex, SERVER_MONGODB, DBTARGET_MONGODB
        else: 
            return None, SERVER_MONGODB, DBTARGET_MONGODB

    
## funcao inicial
def main():
    ## Chamada da funcao de criacao dos indices
    resultCreatedIndex, serverMongoDB, DBDestino = createIndexes()

    ## Exibe o resultado da criacao dos indices em formato json
    json_resultCreatedIndex = json.dumps(resultCreatedIndex, indent=4, default=str)
    msgLog = '\nServidor: {0}\nBanco de dados: {1}\nRetorno do processo de criacao do(s) indice(s):\n{2}\n'.\
        format(serverMongoDB, DBDestino, json_resultCreatedIndex)
    
    print(msgLog)

#inicio da aplicacao
if __name__ == "__main__":
    
    ## chamada da funcao inicial
    main()
