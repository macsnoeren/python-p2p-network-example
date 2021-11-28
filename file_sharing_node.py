#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#######################################################################################################################

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
    print("connect - Connect to another node.")
    print("stop    - Stops the application.")
    print("help    - Prints this help text.")

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

node.stop()
