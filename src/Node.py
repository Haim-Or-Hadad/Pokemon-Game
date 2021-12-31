import json
import os


class Node:

    def __init__(self, id: int, pos: tuple = None, **kwargs):
        """
        pos: the position of nodes in space.
        id: node's key
        """
        self.pos = pos
        self.id = id
        self.weight = float('inf')
        self.connect_out = {}
        self.connect_in = {}
        self.tag = -1
        self.info = "White"
        self.max_weight = 0

    def x(self):
        """
        :returns x position of node
        :return int
        """
        if type(self.pos) == tuple:
            return float(self.pos[0])
        elif type(self.pos) == list:
            return float(self.pos[0])
        else:
            check = list(self.pos.split(","))
            return float(check[0])

    def y(self):
        """
         :returns y position of node
         :return int
         """
        if type(self.pos) == tuple:
            return float(self.pos[1])
        elif type(self.pos) == list:
            return float(self.pos[1])
        else:
            check = list(self.pos.split(","))
            return float(check[1])

    def get_id(self):
        """
        :returns node's id.
        return:id
        """
        return self.id

    def get_pos(self):
        """
        return node's position
        :return:pos
        """
        return self.pos

    def get_tag(self):
        return self.tag

    def get_out(self):
        """
        all the nodes that this node connect them

        :return: in
        """
        return self.connect_out

    def get_in(self):
        """
        all the edges that arrived to this node
        :return: out
        """
        return self.connect_in

    def add_connect_out(self, id, weight):
        """
        add edge between this node to neighbor node
        :param id: neighbor id
        :param weight: weight id
        """
        self.connect_out[id] = weight

    def add_connect_in(self, id, weight):
        """
        add edge that connect to this node
        :param id: neighbor id
        :param weight: weight id
        """
        self.connect_in[id] = weight

    def __str__(self):
        return f"pos:{str(self.pos)[1:-1]},id:{self.id}"

    def __repr__(self):
        return f"pos:{str(self.pos)[1:-1]}\n"

# root_path = os.path.dirname(os.path.abspath(__file__))
#
#
# with open(root_path+'\A1.JSON', 'r') as file:
#     list_nodes = json.load(file)['Nodes']
#     nodes = [Node(**n) for n in list_nodes]
#
# nodes[0].pos="34,34,123213"
# nodes[3].pos="34,34,123213"
# for n in nodes:
#     print(n.pos , n.id)
