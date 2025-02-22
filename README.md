Script de criação de índices em coleções MongoDB em ambiente replicaset usando o recurso de commitQuorum para controlar a confirmação de confirmação de criação do índice.
Isso se fez necessário pois o create_index() do pymongo não dá suporte a uso de commitQuorum, devido a isso poderia ser usado o create_indexes ou db.command().
No processo apresentado optei pelo uso do db_command() devido a facilidade de envio dos índices em uma lista.

A criação de índices é um processo de várias etapas. O processo de criação do índice usa o commit quorum para minimizar o atraso de replicação em nós secundários.

Abaixo informações das opções de commitQuorum existentes:
 - "votingMembers" - todos os membros do conjunto de réplicas votantes portadores de dados (padrão).
   
 - "majority" - uma maioria simples dos membros do conjunto de réplicas de votos com dados.
   
 - <int> - um número específico de membros do conjunto de réplicas de votação com recurso de dados.
   
 - 0 - Desativa o comportamento de votação por quorum. Os membros iniciam a construção do índice simultaneamente, mas não votam nem esperam pelo quorum antes de concluir a construção do índice. 
       Se você iniciar uma construção de índice com um quorum para o commit de 0, não poderá modificar posteriormente o quorum de confirmação usando setIndexCommitQuorum.

 - Um nome de tag do conjunto de réplicas.


Definir commitQuorum pode ser muito útil para criações de índices em ambientes replicaset com membros atrasados, onde por motivo do atraso pode demorar a ter a resposta de confirmação do índice criado.
Para evitar isso podemos definir por exemplo o commitQuorum para 1, que significa que o índice sendo criado por exemplo no primário já terá a confirmação de criação.

O padrão do commitQuorum para o MongoDB a partir da versão 4.4 é "votingMembers".

O script python criado faz o seguinte:

1. Tenho um banco de dados de modelo que uso para criar outros bancos de dados.
2. Esse modelo irá me fornecer o nome da coleção movies e seus índices.
3. Como podem existir na coleção movies vários índices criados e esses índices podem ter ordenações específicas (ASCENDING ou DESCENDING).
   O processo deverá coletar esses índices conforme nome do índice, campos formados do índice e a ordem desses índices.
4. Esses índices coletados serão listados no python respeitando a ordenação dos mesmos.
5. Por fim o comando db.command({}) irá criar os índices com o commitQuorum definido explicitamente, que no caso é 1.

Documentação oficial MongoDB: https://www.mongodb.com/pt-br/docs/manual/reference/method/db.collection.createIndex/

Documentação oficial Pymongo create_index(): https://pymongo.readthedocs.io/en/4.6.1/api/pymongo/collection.html#pymongo.collection.Collection.create_index

Documentação oficial Pymongo create_indexes(): https://pymongo.readthedocs.io/en/4.6.1/api/pymongo/collection.html#pymongo.collection.Collection.create_indexes

