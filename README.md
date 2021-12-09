# Getting started with p2pnetwork
This tutorial provides you with a walk through how to use the p2pnetwork framework. If you would like to use this framework, you can use these steps to get familiar with the module. Eventually it is up to you to use and implement your specific details to the p2pnetwork applications.

## Should I use this module?
**If you would like to create peer-to-peer network applications ... the answer is yes!** The module provides you with all the basic details of peer-to-peer network applications. It starts a node that is able to connect to other nodes and is able to receive connections from other nodes. When running a node, you get all the details using an event based structure. When some node is connecting or sending a message, methods are invokes, so you immediatly can react on it. In other words, implementing your application details. 

Note that it is a framework that provide the basics of a peer-to-peer network application. The basic idea is not to implement application specifics, so the developer is really in the lead. For example, a peer-to-peer network application implements most likely a discovery function. This function discovers the nodes that form the network. You need to implement this on your own. Meaning that you need to design a protocol and implement it within your class.

## Example project
In this tutorial we focus on a peer-to-peer file sharing network application. The application forms a peer-to-peer network and is able to discover other nodes. Nodes share a directory on their computer that hold files to be shared within the network. A node is able to search for a specific file and download the file respectively. The following peer-to-peer network functions are going to be implemented:
* Connecting to other nodes
* Discover nodes on the network
* Ping nodes on the network
* Search for a file on the network
* Download a file on the network

## Step 1: Install the module
To install the package for you to use (https://pypi.org/project/p2pnetwork/):
````
pip install p2pnetwork
````

## Step 2: Create your project
Create a directory on your computer and create two files. The first file is the class that implements the file sharing peer-to-peer network application. This class extends from the Node class of the p2pnetwork module. The second file is the python executable file that initiates the class and implements a console interface to interact with our file sharing node. When you are ready the directory should like this:
````
FileSharingNode.py
file_sharing_node.py
````
## Step 3: Setup the file sharing class
Open the file ````FileSharingNode.py```` and create the class FileSharingNode that extends from the Node class of the p2pnetwork modules. The code below shows the example.
````python
from p2pnetwork.node import Node

class FileSharingNode (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(FileSharingNode, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        print("node_message from " + connected_node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

````
## Step 4: Setup console application
Open the file ````file_sharing_node.py```` and create a console application that instantiates the ````FileSharingNode.py````.

````python
import sys

from FileSharingNode import FileSharingNode

# The port to listen for incoming node connections
port = 9876 # default

# Syntax file_sharing_node.py port
if len(sys.argv) > 1:
    port = int(sys.argv[1])

# Instantiate the node FileSharingNode, it creates a thread to handle all functionality
node = FileSharingNode("127.0.0.1", port)

# Start the node, if not started it shall not handle any requests!
node.start()

# The method prints the help commands text to the console
def print_help():
    print("stop - Stops the application.")
    print("help - Prints this help text.")

# Implement a console application
command = input("? ")
while ( command != "stop" ):
    if ( command == "help" ):
        print_help()

    command = input("? ")

node.stop()
````
Running this example code results in the following console output:
````
Initialisation of the Node on port: 9876 on node (e5ab15fdf31dcf6f0c4490d5ebb216f6ee8a6f86fca5a33bcbc8b63d7c963b2caf6c46410d5667bcd792fc02d7652e7cb50475d949c45506c6585f059637a449)
? help
stop - Stops the application.
help - Prints this help text.
? stop
node is requested to stop!
Node stopping...
Node stopped
````

From this moment, you have already a bare minimum application that implements the framework p2pnetwork. No application specifics have been coded yet. The node is already listening to incoming connections and able to connect to other nodes at your command. From this point, we will add the required functionality to the application. In order to test this applications, you need to run the application twice on different ports. In this case you could open two terminals and run the following commands:
1. ````python file_sharing_node.py 9876````
2. ````python file_sharing_node.py 9877````

## Step 5: Connect to another node
We are going to add the functionality to connect with another node. In this case, you should spin off in another terminal the application on port 9877: ````file_sharing_node.py 9877````. When the user wants to connect to another node, you need to provide a host/ip and port number. In order to form a peer-to-peer network, you need to start with a few main nodes that are always available for other nodes to connect to. When connected to these nodes you can discover other nodes and connect to other nodes as well for efficiency or performance. You can advertise these main nodes on the Internet, so the clients know how to start. Add the following code to ````file_sharing_node.py````.

````python
....
def connect_to_node(node:FileSharingNode):
    host = input("host or ip of node? ")
    port = int(input("port? "))
    node.connect_with_node(host, port)

# Implement a console application
command = input("? ")
while ( command != "stop" ):
    if ( command == "help" ):
        print_help()
    if ( command == "connect"):
        connect_to_node(node)

    command = input("? ")
....
````
When you run the application and connect to another node, you immediatly see the invoked message of the methods in the ````FileSharingNode.py````. Below the console output of the application. When you connect to another node, it will be placed in the outbound list, because it is an outgoing connection. 
````
$>file_sharing_node.py 9876
Initialisation of the Node on port: 9876 on node (ceccce67f62d2d067bca76901ba3da2028539754b451afa81b0ffe2fcc64e070386f5573ee6cf4da9223202d363c3aeb035b360ad5bd95985e1797e93cd93b28)
? connect
host or ip of node? localhost
port? 9877
outbound_node_connected: df643d3c0063b40fcb0c185a9f39e4743551ef426c9acc0355cb01b04288dd87909f7d2ca74d594b266ee6dd149d8e2b3a82c4ee9584382ec4e91230aad1118d
````
This application running at port 9877 is receives the connection. Therefore, you see an inbound message. The incoming connection from the node is added to the inbound list, because it is a connection with us.
````
$>file_sharing_node.py 9877
Initialisation of the Node on port: 9877 on node (df643d3c0063b40fcb0c185a9f39e4743551ef426c9acc0355cb01b04288dd87909f7d2ca74d594b266ee6dd149d8e2b3a82c4ee9584382ec4e91230aad1118d)
? inbound_node_connected: ceccce67f62d2d067bca76901ba3da2028539754b451afa81b0ffe2fcc64e070386f5573ee6cf4da9223202d363c3aeb035b360ad5bd95985e1797e93cd93b28
````
You already see that you have a lot of control of what happens. Immediatly, you get notified when nodes are connected. Eventually, how nodes are connected is not really important when messages are send to each other.

## Step 6: Discover nodes on the network
An important functionality is to discover other nodes on the network. It could be used to make your connection to the network stronger. For file sharing you would like to connect to hosts that have a large bandwidth. Then your downloads will progress will be faster. In this case, you would like to exchange this information as well. Based on the discovery information, you could connect to those hosts. For the tutorial it is out of scope.

### Approach
In order to implement this functionality, we need to design the functionality. Within peer-to-peer network application we need to really think how this functionality should work. You need to think how a message is sent to other nodes, but also how other nodes should anser to this message.

Imagine you have a network of thousands nodes running. If you would like to discover the nodes on the network, how should you approach it? In this example we sent a discovery message to all the nodes we are connected to. When a node receives a discovery request, it sends back all the nodes it is connected to AND the node relays the discovery message to the connected nodes. It needs to administer the discovery message it got, while you do not want to relay "old" discovery message. If you do not take care of this, discovery messages could be relayed forever in the network. Therefore, the discovery message should have a unique identifier. We would also control how deep the discovery takes place, so we add a number to the discovery message that is subtracted each time it is relayed. When a node receives a discovery with this number to zero, it will not relay the message anymore. If this number is -1, then the whole network will be discovered. Note that you always only discover connected (alive) nodes.

### Discovery messages
In order to further design the discovery functionality, we should design all the messages that are required to implement the discovery functionality. Several messages are required as discussed in the previous section: discover and discover_answer. Furthermore, we need to design how to send these messages and how to receive these messages.

#### sending discover message
A node is able to discover the connected nodes by sending a discover message to the nodes that are connected. This discover message will have the following elements:

|key  | description |
|:----|:------------|
|type | The type of the message, in this case 'discover'.|
|id   | Unique message id based on requesting node: node_id + timestamp.|
|depth| Number that is used to control how many times the message is relayed, if -1 it will be relayed alway when discovery message have not been relayed previsously|

Register the id of the discover message, so it is possible to check whether the node receives its own discovery message. You can do this with an array.

Add the following code to the ````FileSharingNode.py```` file.
````python
# Start discovery of nodes in the network. The depth determines how
# many times the message should be relayed. Default depth is -1, 
# which means that it will be infinitely be relayed. Note that nodes
# will not relay the discovery message when they already received it.
def discover(self, depth=-1):
    id = self.id + str(int(time.time())) # node_id + timestamp
    self.send_to_nodes({
        type: "discover",
        id: id,
        depth: depth
    })
````

#### receiving discover message
When a discover message is received the following steps needs to be followed:
1. Drop the discover message has been received previously. Register these id's in an array for example.
2. Drop the discover message when depth is zero.
3. If depth is not -1 decrement depth with 1
4. Register the id in an array
5. Send discover_answer to sender (see discover_answer message)
6. If depth is -1 and not 0 send the message to connected nodes

In order to implement the receiving of this message, it is required to change the callback method ````node_message(self, connected_node, data)````. The code below show what is required to add in order to accept the reception of the ````discover```` message.

````python
def node_message(self, connected_node, data):
    print("node_message from " + connected_node.id + ": " + str(data))

    # Handle the reception of the discover message
    if data["type"] == "discover":
        self.discover_received(connected_node, data)
````
Because we need to register the id's of the received discover message, we need to add an array ````discover_ids```` to the class. We do this in the ````__init___```` method. See the following code as example:

````python
def __init__(self, host, port, id=None, callback=None, max_connections=0):
    super(FileSharingNode, self).__init__(host, port, id, callback, max_connections)

    # Store the ids of the discover messages that have been received
    self.discover_ids = []
````

The functionality of the reception will be implemented by the function ````discover_received````. See the code below how the steps have been implemented.

````python
def discover_received(self, connected_node, data):
    # 1. Drop the discover message has been received previously. 
    #    Register these id's in an array for example.
    if data["id"] in self.discover_ids:
        print("discover_received: drop message already received")
        return
    
    # 2. Drop the discover message when depth is zero.
    if data["depth"] == 0:
        print("discover_received: drop message depth is zero")
        return

    # 3. If depth is not -1 decrement depth with 1
    if data["depth"] != -1:
        data["depth"] = data["depth"] - 1

    # 4. Register the id in an array
    self.discover_ids.append(data["id"])

    # 5. Send discover_answer to sender (see discover_answer message)
    self.discover_answer(connected_node, data["ids"])

    # 6. If depth is -1 and not 0 send the message to connected nodes
    if data["depth"] == -1 and data["depth"] != 0:
        self.send_to_nodes(data)
````

#### sending discover_answer message
A node shall send a ````discover_answer```` message when it has received a ````discover```` message. This message returns the answer to the node that has send the discover message. The message contains the connected nodes of this node. The following message can be defined:

|key  | description |
|:----|:------------|
|type | The type of the message, in this case 'discover_answer'.|
|id   | The unique id that has been send initially by the node that send the discover message|
|node_id| The node id that sents the initial discover_answer message|
|outbound_nodes| A list of nodes that are connected with this node containing node_id, ip and port|
|inbound_nodes| A list of nodes that are connected with this node containing node_id, ip and port|

The following code shall be added to the class:
````python
    def discover_answer(self, node, id):
        outbound_nodes = []
        inbound_nodes = []

        for node in self.nodes_outbound:
            outbound_nodes.append({
                "id": node.id,
                "host": node.host,
                "port": node.port
            })

        for node in self.nodes_inbound:
            inbound_nodes.append({
                "id": node.id,
                "host": node.host,
                "port": node.port
            })

        self.send_to_nodes({
            "type": "discover_answer",
            "id": id,
            "node_id": self.id,
            "outbound_nodes": outbound_nodes,
            "inbound_nodes": inbound_nodes
        })        
````

#### receiving discover_answer message
As we have learned before, in decentralized peer-to-peer application, we need also to implement the reception of messages. What should we do when we receive a discover_answer message. In this case, the following steps needs to be followed:
1. Drop the message when the id is not registered, in this case it is a fake message? You could flag this node as possible malicious? But that will not be handled here.
2. When the registration of the id shows that it was send by another node, then relay the message to that node
3. When the registration of the id shows that it is the current node, then process the data within the node by calling another method

In order to implement the receiving of this message, it is required to change the callback method ````node_message(self, connected_node, data)````. The code below show what is required to add in order to accept the reception of the ````discover_answer```` message.

````python
def node_message(self, connected_node, data):
    print("node_message from " + connected_node.id + ": " + str(data))

    # Handle the reception of the discover_answer message
    if data["type"] == "discover_answer":
        self.discover_answer_received(connected_node, data)
````

Note that somethimes at this point you see that you need to register more than only the ids. It is required to register the id together with the node you have received the message. When you send the message, the node can become None, so you know it was you! To add the full functionality of the answer, check the following code:

````python
def discover_answer_received(self, node, data):
    # 1. Drop the message when the id is not registered, in this case it is a fake message? 
    # You could flag this node as possible malicious? But that will not be handled here.
    if data["id"] not in self.discover_ids.keys():
        print("discover_answer_received: drop message fake?")
        return
    
    # 2. When the registration of the id shows that it was send by another node, then relay the message to that node
    if self.discover_ids[data["id"]] != None:
        self.send_to_node(self.discover_ids[data["id"]], data)

    else: # 3. When the registration of the id shows that it is the current node, then process the data within the node by calling another method
        self.discover_answer_process(data)

def discover_answer_process(self, data):
    print("discover_answer_process: process the data: ")
    print(data)
````

#### Discovery test
1. Start two nodes in two terminals with two different ports

_work in progress..._