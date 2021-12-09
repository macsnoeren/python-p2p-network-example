#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#######################################################################################################################

import sys

sys.path.insert(0, '../python-p2p-network') # Import the files where the modules are located

from FileSharingNode import FileSharingNode

# setup a network of nodes for the test
node_1 = FileSharingNode("127.0.0.1", 10000, 1)
node_2 = FileSharingNode("127.0.0.1", 10001, 2)
node_3 = FileSharingNode("127.0.0.1", 10002, 3)
node_1.start()
node_2.start()
node_3.start()
node_2.connect_with_node("localhost", 10000)
node_3.connect_with_node("localhost", 10000)

# The port to listen for incoming node connections
port = 9876 # default

# Syntax file_sharing_node.py port
if len(sys.argv) > 1:
    port = int(sys.argv[1])

# Instantiate the node FileSharingNode, it creates a thread to handle all functionality
node = FileSharingNode("127.0.0.1", port, 4)
#node.debug = True

# Start the node, if not started it shall not handle any requests!
node.start()

# The method prints the help commands text to the console
def print_help():
    print("connect  - Connect to another node.")
    print("discover - Discover the nodes in the network.")
    print("stop     - Stops the application.")
    print("help     - Prints this help text.")

def connect_to_node(node:FileSharingNode):
    host = input("host or ip of node? ")
    port = int(input("port? "))
    node.connect_with_node(host, port)

def discover(node:FileSharingNode):
    node.discover()

# Implement a console application
command = input("? ")
while ( command != "stop" ):
    if ( command == "help" ):
        print_help()
    elif ( command == "connect"):
        connect_to_node(node)
    elif ( command == "discover"):
        discover(node)

    command = input("? ")

node.stop()
node_1.stop()
node_2.stop()
node_3.stop()
