import json
import unittest

from client_python.catch_algo import catch_algo
from client_python.pokemon import pokemon
from client_python.agent import Agent
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):
    with open('../data/A2', 'r') as A2:
        A2 = json.load(A2)
        game_graph = GraphAlgo()
        game_graph.load_from_json(A2)

    def test_Game(self):
        pokemon_dict = {'Pokemons': [
            {'Pokemon': {'value': 5.0, 'type': -1, 'pos': '35.20273974670703,32.10439601193746,0.0'}},
            {'Pokemon': {'value': 8.0, 'type': -1, 'pos': '35.189541903742466,32.10714473742062,0.0'}},
            {'Pokemon': {'value': 13.0, 'type': 1, 'pos': '35.198546018801096,32.10442041371198,0.0'}},
            {'Pokemon': {'value': 5.0, 'type': -1, 'pos': '35.20418622066997,32.10618391544376,0.0'}},
            {'Pokemon': {'value': 9.0, 'type': -1, 'pos': '35.207511563168026,32.10516145234799,0.0'}},
            {'Pokemon': {'value': 12.0, 'type': -1, 'pos': '35.19183431463849,32.106897389061444,0.0'}}]}
        pokemon_dict = pokemon.build_pokemon(pokemon_dict)
        self.assertEqual(6, len(pokemon_dict))
        Agent_dict = {'Agents': [
            {'Agent': {'id': 0, 'value': 0.0, 'src': 0, 'dest': -1, 'speed': 1.0,
                       'pos': '35.19589389346247,32.10152879327731,0.0'}},
            {'Agent': {'id': 1, 'value': 0.0, 'src': 1, 'dest': -1, 'speed': 1.0,
                       'pos': '35.20319591121872,32.10318254621849,0.0'}},
            {'Agent': {'id': 2, 'value': 0.0, 'src': 2, 'dest': -1, 'speed': 1.0,
                       'pos': '35.20752617756255,32.1025646605042,0.0'}}]}
        Agent_dict = Agent.build_agent(Agent_dict)
        self.assertEqual(3, len(Agent_dict))
        Agent1 = Agent_dict[0]
        poke1 = pokemon_dict[0]
        poke2 = pokemon_dict[1]
        tes1=catch_algo(self.game_graph,None)
        edge1 = tes1.on_edge(poke1.pos)
        edge2 = tes1.on_edge(poke2.pos)
        poke1.pokemon_edge(edge1)
        poke2.pokemon_edge(edge2)
        self.assertEqual(2.4899630707924256, self.game_graph.shortest_path(Agent1.src, poke1.src)[0])
        self.assertEqual(5.836343263088861, self.game_graph.shortest_path(Agent1.src, poke2.src)[0])
        self.assertEqual([1, 26], self.game_graph.shortest_path(Agent1.src, poke1.src)[1])
        self.assertEqual([16, 15, 14, 13], self.game_graph.shortest_path(Agent1.src, poke2.src)[1])



if __name__ == '__main__':
    unittest.main()
