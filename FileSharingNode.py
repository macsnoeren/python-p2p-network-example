
#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#######################################################################################################################

import time

from p2pnetwork.node import Node

class FileSharingNode (Node):
    # Python class constructor
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(FileSharingNode, self).__init__(host, port, id, callback, max_connections)

        # Store the ids of the discover messages that have been received
        # together with the node that send this message
        self.discover_ids = {}

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

        # Handle the reception of the discover message
        if data["type"] == "discover":
            self.discover_received(connected_node, data)

        # Handle the reception of the discover_answer message
        if data["type"] == "discover_answer":
            self.discover_answer_received(connected_node, data)


    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    # Start discovery of nodes in the network. The depth determines how
    # many times the message should be relayed. Default depth is -1, 
    # which means that it will be infinitely be relayed. Note that nodes
    # will not relay the discovery message when they already received it.
    def discover(self, depth=-1):
        id = self.id + str(int(time.time())) # node_id + timestamp
        self.send_to_nodes({
            "type": "discover",
            "id": id,
            "depth": depth
        })
        self.discover_ids[id] = None

    def discover_received(self, node, data):
        # 1. Drop the discover message has been received previously. Register these id's in an array for example.
        if data["id"] in self.discover_ids.keys():
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
        self.discover_ids[data["id"]] = node

        # 5. Send discover_answer to sender (see discover_answer message)
        self.discover_answer(node, data["id"])

        # 6. If depth is -1 and not 0 send the message to connected nodes
        if data["depth"] == -1 and data["depth"] != 0:
            self.send_to_nodes(data)

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

    def discover_answer_received(self, node, data):
        # 1. Drop the message when the id is not registered, in this case it is a fake message? You could flag this node as possible malicious? But that will not be handled here.
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
