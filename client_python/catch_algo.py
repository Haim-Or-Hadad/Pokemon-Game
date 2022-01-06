import math

from client_python.client import Client
from src.GraphAlgo import GraphAlgo
from agent import *


class Catch_Algo:
    pokemon_curr_list = []
    def __init__(self, game_graph: GraphAlgo, client: Client):
        self.game_graph = game_graph
        self.client = client

        ##save the pokemons that not catch
        def load_PriorityQueue(self, pokemon_list: list, ag: Agent):
            priority_poke = PriorityQueue()
            counter = 0
            positions = self.pos_dict()
            dist_list = []
            for po in pokemon_list:
                close_pokemon_id = self.closest_node(po.pos, positions)
                edge = self.on_edge(close_pokemon_id, po.pos)
                po.pokemon_edge(edge)
                dist = self.game_graph.shortest_path(ag.src, po.dest)[0]
                dist = dist / po.value
                if dist in dist_list:
                    continue
                else:
                    dist_list.append(dist)
                priority_poke.put((dist, po))
            return priority_poke

    ## this function get list of agents and pokemons and allocate agent to catch pokemon
    def send_agent(self, agent_list: list, pokemon_list: list):
        """
        take src and dest of agent and calculate his position.
        then we take the position of the pokemon and check the shortest
        path between the src/dest of agent to src/dest of pokemon.
        """
        for ag in agent_list:
            for po in pokemon_list:
                    if ag.dest == -1:
                        positions = self.pos_dict() # position of the graph nodes
                        close_pokemon_id = self.closest_node(po.pos, positions)
                        edge = self.on_edge(close_pokemon_id, po.pos)
                        s_path = self.game_graph.shortest_path(ag.last_item(), close_pokemon_id)
                        next_node = ag.show_path()
                        if ag.src == ag.last_item():
                            ag.update_path(s_path, edge[1]) # add the new path to queue
                            next_node = ag.show_path()
                        elif next_node == ag.src:
                            ag.remove_element()
                            next_node = ag.show_path()
                            self.client.choose_next_edge(
                                '{"agent_id":' + str(ag.id) +
                                ', "next_node_id":' + str(next_node) + '}')
                        print("path for agent:" , ag.agent_path)
                        print("shortest_path", s_path)
                        print("close_pokemon_id:",close_pokemon_id)
                        print("last item of queue:", ag.last_item())
                        print("next node:", next_node)
                        print("src:", ag.src)
                        print("dest:", ag.dest)
                        ttl = self.client.time_to_end()
                        print(ttl, self.client.get_info())
            self.client.move()
        """
        get pokemon position and all graph nodes positions
        return : the node_id that close to the pokemon
        """
    def closest_node(self, poke_pos, nodes):
        min = math.inf
        min2 = math.inf
        id2 = 99
        id = 99
        poke_pos = list(poke_pos.split(","))
        for n in nodes.keys():
            node_corr = list(nodes.get(n).split(","))
            dist = ((float(poke_pos[0]) - float(node_corr[0])) ** 2 + (
                    float(poke_pos[1]) - float(node_corr[1])) ** 2) ** 0.5
            if dist < min:
                min2 = min
                id2 = id
                min = dist
                id = n
        return id

    def load_curr_pokemons(self, pokemon_list: list):

        for i in pokemon_list:
            flag = 0
            if len(self.pokemon_curr_list) == 0:
                self.pokemon_curr_list.append(pokemon_list.pop())
            else:
                for pokemon in pokemon_list:  # iterate over new pokemon list
                    for curr in self.pokemon_curr_list:  # iterate over current list pokemons
                        if curr == pokemon:
                            flag += 1
                    if flag == 0:
                        self.pokemon_curr_list.append(pokemon)
        for x in self.pokemon_curr_list:
            front = self.pokemon_curr_list.pop(0)
            self.pokemon_curr_list.append(front)



    """
    returns the edge that there is a pokemon 
    return : 2 nodes
    """
    def on_edge(self, src, poke):
        poke = list(poke.split(","))
        src = self.game_graph.graph.nodes.get(src)
        shortest = []
        src_poke_dist = self.game_graph.distance(src.get_pos(), poke)
        edge_list = self.game_graph.graph.all_out_edges_of_node(src.id)
        for dest in edge_list:
            dest = self.game_graph.graph.nodes.get(dest)
            curr_dist = self.game_graph.distance(poke, dest.get_pos())

            total_dist = self.game_graph.distance(src.get_pos(), dest.get_pos())

            if total_dist >= (src_poke_dist + curr_dist - 0.01):
                return src.id, dest.id
        """
        return dict with all the positions of the graph nodes
        """
    def pos_dict(self):
        pos_dict = {}
        for node in self.game_graph.get_graph().nodes.values():
            pos_dict[node.id] = node.pos
        return pos_dict
