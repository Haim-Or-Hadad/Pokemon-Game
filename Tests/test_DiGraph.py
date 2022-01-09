import unittest
from src.DiGraph import DiGraph



class Test(unittest.TestCase):
    test_graph = DiGraph()
    test_graph.add_node(3, (5, 6, 0))
    test_graph.add_node(4, (7, 8, 6))
    test_graph.add_node(5, (9, 10, 6))

    def test1_add_node(self):
        self.assertTrue(self.test_graph.add_node(0, (1, 4, 0)))
        self.assertTrue(self.test_graph.add_node(1, (1, 4, 6)))
        self.assertTrue(self.test_graph.add_node(2, (1, 4, 6)))
        self.assertFalse(self.test_graph.add_node(0, (1, 4, 6)))
        pos1 = self.test_graph.nodes.get(1).get_pos()
        pos2 = self.test_graph.nodes.get(2).get_pos()
        self.assertEqual(pos1, pos2)

    def test2_add_edge(self):
        self.assertTrue(self.test_graph.add_edge(3, 4, 22))
        self.assertTrue(self.test_graph.add_edge(4, 5, 3))
        self.assertTrue(self.test_graph.add_edge(5, 3, 6))
        self.assertFalse(self.test_graph.add_edge(10, 1, 3))

    def test3_allDict_allSizes(self):
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
        self.assertEqual(len(test_graph2.get_all_v()), len(self.test_graph.get_all_v()))
        self.assertEqual(test_graph2.get_mc(), self.test_graph.get_mc())
        self.assertEqual(test_graph2.e_size(), self.test_graph.e_size())
        self.assertEqual(test_graph2.v_size(), self.test_graph.v_size())
        for i in self.test_graph.nodes:
            self.assertEqual(len(test_graph2.all_out_edges_of_node(i)), len(self.test_graph.all_out_edges_of_node(i)))
            self.assertEqual(len(test_graph2.all_in_edges_of_node(i)), len(self.test_graph.all_in_edges_of_node(i)))

    def test4_remove_node(self):
        self.assertTrue(self.test_graph.remove_node(1))
        self.assertIsNone(self.test_graph.get_all_v().get(1))

    def test5_remove_edge(self):
        self.assertTrue(self.test_graph.remove_edge(4, 5))
        self.assertIsNone(self.test_graph.all_out_edges_of_node(4).get(5))

    if __name__ == '__main__':
        unittest.main()