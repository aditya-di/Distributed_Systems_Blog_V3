# Distributed System Blog application 

The goal of this project is to design and develop a scalable distributed system blog application (replication of twitter) using tuplespace and heterogeneous(P2P clustering distributed blog application) .


## Distributed Nodes 

- In version 1.0 of this project, we implemented the adapter pattern in RUBY, which is internally connected to the RInda tuple space.

- This architecture can also be implemented in python tuplespace, While our concerns are:
  - The PyLinda package is not not the same as the pylinda package available on PyPI.
  - PyLinda was written for Python 2.
  - The available code for PyLinda is missing some source files.
  - The original author of the code seems to have disappeared from the Internet.

- Fortunately Ruby, another common scripting language, includes a module named Rinda which implements the Linda distributed computing paradigm.

- In this version we modified the architecture of the project
  - In this architecture, we need to elect a leader. The leader is responsible for all the operations in the cluster. Operations such as READ, WRITE, DELETE, REPLICATION. 
The client application will directly communicate with the leader for data operation when a new data is written in the cluster, the leader will do the active replication in all the TupleSpaces and the log file. After the replication is done in all the nodes/TupleSpaces, the leader will send an Acknowledgement to the client application for the WRITE operation (Similar to Apache Kafka and Cassandra DB). 
The leader node will also check the heartbeat of the follower nodes/TupleSpaces for their active status check. If any node/TupleSpace failed then it will no replicate/WRITE data to it.

## How to run the project:
 Install the dependencies by the following command 
 
 ```
 $ gem install --user-install xmlrpc
 
 ```

 How to run the application
 ```
 1. python3 naming_logging.py
 2. foreman -v start
 3. python3 blog.py (with cmd line arguments)
 ```
 
# The Project Team
## Team Members
- Shekhar Palit
- Aditya Dingre

## Project Technologies
- Programming Language - Python, Ruby 
- Storage_Server - RInda TupleSpace
- RPC modules - XMLRPC(Ruby server, Python Client)
- foreman 
