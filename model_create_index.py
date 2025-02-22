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

## funcao que retorna data e hora Y-M-D H:M:S
def obterDataHora():
    """
        OBTEM DATA E HORA
    """
    datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return datahora


## funcao de mensagem inicial da aplicacao
def msgInitialApp():
    """
    FUNCAO QUE IMPRIME E GRAVA EM LOG MSG INICIAL DA APLICACAO
    """
    datahora = obterDataHora()
    msg = '***** List Info ServerStatus MongoDB ***** BEGIN: ' + datahora
    print(msg)


## funcao de mensagem final da aplicacao
def msgFinalApp():
    """
    FUNCAO QUE IMPRIME E GRAVA EM LOG MSG FINAL DA APLICACAO
    """
    datahora = obterDataHora()
    msg = '***** List Info ServerStatus MongoDB ***** END: ' + datahora + '\n'
    print(msg)


## funcao para verificar os valores do dotenv
def getValueEnv(valueEnv):
    """
    OBTEM VALORES DO ARQUIVO .ENV
    """
    v_valueEnv = os.getenv(valueEnv)
    
    if not v_valueEnv:
        msgLog = "Variável de ambiente '{0}' não encontrada.".format(valueEnv)
        print(msgLog)

    return v_valueEnv


def createIndexes():

    try:
       
        USERNAME_MONGODB = getValueEnv("USERNAME_MONGODB")
        PASSWORD_MONGODB = getValueEnv("PASSWORD_MONGODB")
        SERVER_MONGODB   = getValueEnv("SERVER_MONGODB")
        DBAUTHDB_MONGODB = getValueEnv("DBAUTHDB_MONGODB")
        DBMODEL_MONGODB  = getValueEnv("DBMODEL_MONGODB")
        DBTARGET_MONGODB = getValueEnv("DBTARGET_MONGODB")


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

            if resultCreatedIndex['ok'] == 1:
                #notes = resultCreatedIndex['note']
                json_str = json.dumps(resultCreatedIndex, indent=4, default=str)
                msgLog = 'Indices criados com sucesso. \n{0}'.format(json_str)
                print(msgLog)
            else:
                msgLog = 'Erro ao criar indices.'
                print(msgLog)
            

    except Exception as e:
        msgException = "Error: {0}".format(e)
        msgLog = 'Obter dados MongoDB [ServerStatusMongoDB] [Erro]: {0}'.format(msgException)
        print(msgLog)

    
## funcao inicial
def main():
    # grava inicio do log
    msgInitialApp()

    ## Chamada d funcao de criacao dos indices
    createIndexes()

    # grava final do log
    msgFinalApp()

#inicio da aplicacao
if __name__ == "__main__":
    
    ## chamada da funcao inicial
    main()


        
      

