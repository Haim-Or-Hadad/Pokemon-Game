import math

from client_python.client import Client
from src.GraphAlgo import GraphAlgo
from agent import *

EPS = 0.000000001


class catch_algo:
    pokemon_curr_list = []

    def __init__(self, game_graph: GraphAlgo, client: Client):
        self.game_graph = game_graph
        self.client = client

    ##save the pokemons that not catch
    def load_PriorityQueue(self, pokemon_list: list, ag: Agent, numofagents):
        priority_poke = PriorityQueue()
        counter = 0
        positions = self.pos_dict()
        dist_list = []
        for po in pokemon_list:
            edge = self.on_edge(po.pos)
            po.pokemon_edge(edge)
            dist = self.game_graph.shortest_path(ag.src, po.dest)[0]
            dist = (dist / po.value)  # * po.value
            if dist in dist_list:
                continue
            else:
                dist_list.append(dist)
            priority_poke.put((dist, po))
        if numofagents > 1:
            while counter <= len(priority_poke.queue):
                if priority_poke.queue[counter][1].takenby == 9:
                    priority_poke.queue[counter][1].takenby = ag.id
                    break
                counter += 1
        else:
            while counter < len(priority_poke.queue):
                priority_poke.queue[counter][1].takenby = ag.id
                counter+=1
        # elif priority_poke.queue[1][1].takenby==9:
        #     priority_poke.queue[1][1].takenby = ag.id
        # else:
        #     priority_poke.queue[2][1].takenby = ag.id
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
            numofagents = len(agent_list)
            priority_poke = self.load_PriorityQueue(pokemon_list, ag, numofagents)
            while not priority_poke.empty():
                # for po in priority_poke.get()[1]:
                po = priority_poke.get()[1]
                # if po.takenby == ag.id:
                if ag.dest == -1 and po.takenby == ag.id:
                    edge = self.on_edge(po.pos)
                    po.pokemon_edge(edge)
                    s_path = self.game_graph.shortest_path(ag.last_item(), po.src)[1]
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
                    # if flag==1:
            # self.client.move()
            # flag+=1

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

    def on_edge(self, poke):
        poke = list(poke.split(","))
        for node1 in self.game_graph.graph.nodes.values():
            for node2 in self.game_graph.graph.all_out_edges_of_node(node1.id):
                node2 = self.game_graph.graph.nodes.get(node2)
                curr_src_dest = self.game_graph.distance(node1.get_pos(), node2.get_pos())
                src_poke = self.game_graph.distance(node1.get_pos(), poke)
                dest_poke = self.game_graph.distance(node2.get_pos(), poke)
                if abs(curr_src_dest - (src_poke + dest_poke)) <= EPS:
                    return node1.id, node2.id

    def pos_dict(self):
        pos_dict = {}
        for node in self.game_graph.get_graph().nodes.values():
            pos_dict[node.id] = node.pos
        return pos_dict
