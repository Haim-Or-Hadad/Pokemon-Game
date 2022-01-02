import math

import distance as distance

from client_python.client import Client
from src.GraphAlgo import GraphAlgo
from agent import *


class catch_algo:
    def __init__(self, game_graph: GraphAlgo, client: Client):
        self.game_graph = game_graph
        self.client = client

    ## this function get list of agents and pokemons and allocate agent to catch pokemon
    def send_agent(self, agent_list: list, pokemon_list: list):
        """
        take src and dest of agent and calculate his position.
        then we take the position of the pokemon and check the shortest
        path between the src/dest of agent to src/dest of pokemon.
        """
        for ag in agent_list:
            if ag.dest == -1:
                for po in pokemon_list:
                    positions = self.pos_dict()
                    closest_nodeID = self.closest_node(po.pos, positions)
                    s_path = self.game_graph.shortest_path(ag.src, closest_nodeID[0])
                    ag.update_path(s_path[1],closest_nodeID[1])
                    next_node = ag.get_path()
                    # next_node = (agent1.src - 1) % len(self.game_graph.get_graph().nodes)
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(ag.id) + ', "next_node_id":' + str(next_node) + '}')
                    ttl = self.client.time_to_end()
                    print(ttl, self.client.get_info())

            self.client.move()


    def closest_node(self, poke_pos, nodes):
        min = math.inf
        min2=math.inf
        id2=99
        id=99
        poke_pos = list(poke_pos.split(","))
        for n in nodes.keys():
            node_corr = list(nodes.get(n).split(","))
            dist = ((float(poke_pos[0]) - float(node_corr[0])) ** 2 + (
                        float(poke_pos[1]) - float(node_corr[1])) ** 2) ** 0.5
            if dist < min:
                min2=min
                id2=id
                min = dist
                id = n
        return (id,id2)

    def pos_dict(self):
        pos_dict = {}
        for node in self.game_graph.get_graph().nodes.values():
            pos_dict[node.id] = node.pos
        return pos_dict
