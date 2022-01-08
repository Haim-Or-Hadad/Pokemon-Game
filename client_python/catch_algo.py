import math

from client_python.client import Client
from src.GraphAlgo import GraphAlgo
from agent import *


class catch_algo:
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
        # self.load_pokemons(pokemon_list)
        flag = 1
        # self.load_curr_pokemons(pokemon_list)

        for ag in agent_list:
            priority_poke = self.load_PriorityQueue(pokemon_list, ag)
            while not priority_poke.empty():
                # for po in priority_poke.get()[1]:
                po = priority_poke.get()[1]
                if po.status == 0:
                    if ag.dest == -1:
                        positions = self.pos_dict()
                        close_pokemon_id = self.closest_node(po.pos, positions)
                        print(close_pokemon_id)
                        edge = self.on_edge(close_pokemon_id, po.pos)
                        po.pokemon_edge(edge)
                        s_path = self.game_graph.shortest_path(ag.last_item(), edge[0])[1]
                        print("shortest_path", s_path)
                        print("agent list:", ag.agent_path)
                        if ag.src == ag.last_item() or ag.path_size() == 1:
                            ag.update_path(s_path, po)  # add the new path to queue
                            # self.pokemon_curr_list.pop(0)
                        next_node = ag.show_path()
                        if next_node == ag.src:
                            ag.remove_element()
                            next_node = ag.show_path()
                            self.client.choose_next_edge(
                                '{"agent_id":' + str(ag.id) + ', "next_node_id":' + str(next_node) + '}')
                        print("next node:", next_node)
                        po.update_poke_status(1)
                        print("src:", ag.src)
                        print("dest:", ag.dest)
                        ttl = self.client.time_to_end()
                        print(ttl, self.client.get_info())
        self.client.move()

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

    def on_edge(self, src, poke):
        poke = list(poke.split(","))
        src = self.game_graph.graph.nodes.get(src)
        shortest = {}
        src_poke_dist = self.game_graph.distance(src.get_pos(), poke)
        edge_list = self.game_graph.graph.all_out_edges_of_node(src.id)
        for dest in edge_list:
            dest = self.game_graph.graph.nodes.get(dest)
            curr_dist = self.game_graph.distance(poke, dest.get_pos())
            total_dist = self.game_graph.distance(src.get_pos(), dest.get_pos())
            shortest[dest] = total_dist - (src_poke_dist + curr_dist)
            # if total_dist >= (src_poke_dist + curr_dist - 0.01):
        min = -9999
        dest_id = 0
        for n in shortest:
            if shortest.get(n) > min:
                min = shortest.get(n)
                dest_id = n.id

        return src.id, dest_id

    def pos_dict(self):
        pos_dict = {}
        for node in self.game_graph.get_graph().nodes.values():
            pos_dict[node.id] = node.pos
        return pos_dict
