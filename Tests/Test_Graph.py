import unittest
import json
from src.DiGraph import DiGraph
from math import inf

from data import *

from src.GraphAlgo import GraphAlgo


class Test(unittest.TestCase):
    graph = DiGraph()
    test_graphAlgo = GraphAlgo(graph)
    test_Digraph = DiGraph()
    test_Digraph.add_node(3, (5, 6, 0))
    test_Digraph.add_node(4, (7, 8, 6))
    test_Digraph.add_node(5, (9, 10, 6))

    def test0_load_from_json(self):
        with open('../data/A0', 'r') as A0:
            A0 = json.load(A0)
        with open('../data/A1', 'r') as A1:
            A1 = json.load(A1)
        with open('../data/A2', 'r') as A2:
            A2 = json.load(A2)
        with open('../data/A3', 'r') as A3:
            A3 = json.load(A3)
        self.assertTrue(self.test_graphAlgo.load_from_json(A0))
        self.assertTrue(self.test_graphAlgo.load_from_json(A1))
        self.assertTrue(self.test_graphAlgo.load_from_json(A2))
        self.assertTrue(self.test_graphAlgo.load_from_json(A3))

    def test1_shortest_path(self):
        with open('../data/A1', 'r') as A1:
            A1 = json.load(A1)
        self.test_graphAlgo.load_from_json(A1)
        self.assertEqual((8.718425478533105, [6, 7, 8, 9, 10, 11]), self.test_graphAlgo.shortest_path(2, 11))
        self.test_graphAlgo.graph.remove_node(0)
        self.test_graphAlgo.graph.remove_node(15)
        self.assertEqual((inf, []), self.test_graphAlgo.shortest_path(16, 4))

    def test2_add_node(self):
        self.assertTrue(self.test_Digraph.add_node(0, (1, 4, 0)))
        self.assertTrue(self.test_Digraph.add_node(1, (1, 4, 6)))
        self.assertTrue(self.test_Digraph.add_node(2, (1, 4, 6)))
        self.assertFalse(self.test_Digraph.add_node(0, (1, 4, 6)))
        pos1 = self.test_Digraph.nodes.get(1).pos
        pos2 = self.test_Digraph.nodes.get(2).pos
        self.assertEqual(pos1, pos2)

    def test3_add_edge(self):
        self.assertTrue(self.test_Digraph.add_edge(3, 4, 22))
        self.assertTrue(self.test_Digraph.add_edge(4, 5, 3))
        self.assertTrue(self.test_Digraph.add_edge(5, 3, 6))
        self.assertFalse(self.test_Digraph.add_edge(10, 1, 3))

    def test4_allDict_allSizes(self):
        test_graph2 = DiGraph()
        test_graph2.add_node(0, (1, 4, 0))
        test_graph2.add_node(1, (1, 4, 6))
        test_graph2.add_node(2, (1, 4, 6))
        test_graph2.add_node(3, (5, 6, 0))
        test_graph2.add_node(4, (7, 8, 6))
        test_graph2.add_node(5, (9, 10, 6))
        test_graph2.add_edge(3, 4, 22)
        test_graph2.add_edge(4, 5, 3)
        test_graph2.add_edge(5, 3, 6)
        self.assertEqual(len(test_graph2.get_all_v()), len(self.test_Digraph.get_all_v()))
        self.assertEqual(test_graph2.get_mc(), self.test_Digraph.get_mc())
        self.assertEqual(test_graph2.e_size(), self.test_Digraph.e_size())
        self.assertEqual(test_graph2.v_size(), self.test_Digraph.v_size())
        for i in self.test_Digraph.nodes:
            self.assertEqual(len(test_graph2.all_out_edges_of_node(i)), len(self.test_Digraph.all_out_edges_of_node(i)))
            self.assertEqual(len(test_graph2.all_in_edges_of_node(i)), len(self.test_Digraph.all_in_edges_of_node(i)))

    def test5_remove_node(self):
        self.assertTrue(self.test_Digraph.remove_node(1))
        self.assertIsNone(self.test_Digraph.get_all_v().get(1))

    def test6_remove_edge(self):
        self.assertTrue(self.test_Digraph.remove_edge(4, 5))
        self.assertIsNone(self.test_Digraph.all_out_edges_of_node(4).get(5))

    if __name__ == '__main__':
        unittest.main()
