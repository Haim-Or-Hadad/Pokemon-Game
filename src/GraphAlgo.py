import random
import sys
from queue import PriorityQueue
from src.DiGraph import DiGraph


WIDTH, HEIGHT = 1080, 720

class GraphAlgo():

    def __init__(self, graph: DiGraph = DiGraph()):
        self.graph = graph

    def get_graph(self) -> DiGraph:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: dict):
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        my_graph = DiGraph()
        try:
            # with open(file_name, 'r') as file:
            g_dict = file_name
            for node in g_dict['Nodes']:
                if "pos" in node:
                    my_graph.add_node(node['id'], node['pos'])
                else:
                    x = random.uniform(32, 33)
                    y = random.uniform(34, 36)
                    my_graph.add_node(node['id'], (x, y, 0))

            for edge in g_dict['Edges']:
                my_graph.add_edge(edge["src"], edge["dest"], edge["w"])
            self.graph = my_graph
            return self
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        This function using Dijkstra algorithm for finding the dist of id1 from all the nodes in the graph
        then going over the tags in id2 node back to id1 node adding the node id to the path
        """
        if id1 not in self.graph.nodes or id2 not in self.graph.nodes:
            return float('inf'), []
        self.dijkstra(id1)
        curr_node = self.graph.nodes[id2]
        weight = self.graph.nodes[id2].weight
        if weight == float('inf'):
            return float('inf'), []
        path = []
        while curr_node.id is not id1:
            path.append(curr_node.id)
            tag = curr_node.tag
            curr_node = self.graph.nodes.get(tag)

        # path.append(curr_node.id)
        path.reverse()
        return weight,path


    def distance(self, pos1, pos2):

        dist = ((float(pos1[0]) - float(pos2[0])) ** 2 + (
                float(pos1[1]) - float(pos2[1])) ** 2) ** 0.5
        return dist


    def rest_tag_weight(self):
        for node in self.graph.nodes.values():
            node.weight = float('inf')
            node.tag = -1
            node.info = "White"

    def dijkstra(self, src: int) -> (float, list):
        self.rest_tag_weight()
        self.graph.nodes.get(src).weight = 0
        node_queue = PriorityQueue()
        node_queue.put((self.graph.nodes.get(src).weight, self.graph.nodes.get(src)))
        while not node_queue.empty():
            node = node_queue.get()[1]
            node.info = "Black"
            for neigh in node.connect_out:
                if node.weight + node.connect_out[neigh] < self.graph.nodes[neigh].weight:
                    self.graph.nodes.get(neigh).weight = node.weight + node.connect_out[neigh]
                    self.graph.nodes.get(neigh).tag = node.id
                if self.graph.nodes.get(neigh).info == "White":
                    node_queue.put((self.graph.nodes.get(neigh).weight, self.graph.nodes.get(neigh)))

        for node in self.graph.nodes.values():
            if node.weight > self.graph.nodes.get(src).max_weight:
                self.graph.nodes.get(src).max_weight = node.weight



    def min_x(self):
        min_x = sys.maxsize
        for node in self.graph.nodes.values():
            if float(node.x()) < min_x:
                min_x = float(node.x())
        return min_x

    def max_x(self):
        max_x = 0
        for node in self.graph.nodes.values():
            if node.x() > max_x:
                max_x = node.x()
        return max_x

    def min_y(self):
        min_y = sys.maxsize
        for node in self.graph.nodes.values():
            if node.y() < min_y:
                min_y = node.y()
        return min_y

    def max_y(self):
        max_y = 0
        for node in self.graph.nodes.values():
            if node.y() > max_y:
                max_y = node.y()
        return max_y
