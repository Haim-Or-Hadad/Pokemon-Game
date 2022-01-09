from queue import PriorityQueue
from client_python.client import Client
from src.GraphAlgo import GraphAlgo
from client_python.agent import *

EPS = 0.000000001


class catch_algo:

    def __init__(self, game_graph: GraphAlgo, client: Client):
        self.game_graph = game_graph
        self.client = client

    ## save the pokemons that not catch
    def load_PriorityQueue(self, pokemon_list: list, ag: Agent, numofagents):
        priority_poke = PriorityQueue()
        counter = 0
        dist_list = []
        min = 99999
        i = 0
        place = 0
        for po in pokemon_list:
            edge = self.on_edge(po.pos)
            po.pokemon_edge(edge)
            dist = self.game_graph.shortest_path(ag.src, po.dest)[0]
            dist = (dist / po.value)  # * po.value
            if dist < min and po.takenby == 9:
                top_poke = po
                min = dist
                place = i
            if dist in dist_list:
                continue
            else:
                dist_list.append(dist)
            priority_poke.put((dist, po))
            i += 1
        top_poke.takenby = ag.id
        pokemon_list[place] = top_poke
        if numofagents > 1:
            while counter < len(priority_poke.queue):
                if priority_poke.queue[counter][1].takenby == ag.id:
                    break
                if priority_poke.queue[counter][1].takenby == 9:
                    priority_poke.queue[counter][1].takenby = ag.id
                    break
                counter += 1
        else:
            while counter < len(priority_poke.queue):
                priority_poke.queue[counter][1].takenby = ag.id
                counter += 1
        return priority_poke

    ## this function get list of agents and pokemons and allocate agent to catch pokemon
    def send_agent(self, agent_list: list, pokemon_list: list):
        """
        take src and dest of agent and calculate his position.
        then we take the position of the pokemon and check the shortest
        path between the src/dest of agent to src/dest of pokemon.
        """
        flag = 1
        for ag in agent_list:
            numofagents = len(agent_list)
            priority_poke = self.load_PriorityQueue(pokemon_list, ag, numofagents)
            while not priority_poke.empty():
                po = priority_poke.get()[1]
                if ag.dest == -1 and po.takenby == ag.id:
                    edge = self.on_edge(po.pos)
                    po.pokemon_edge(edge)
                    s_path = self.game_graph.shortest_path(ag.last_item(), po.src)[1]
                    if ag.src == ag.last_item() or ag.path_size() == 1:
                        ag.update_path(s_path, po)
                    next_node = ag.show_path()
                    if next_node == ag.src:
                        ag.remove_element()
                        next_node = ag.show_path()
                        self.client.choose_next_edge(
                            '{"agent_id":' + str(ag.id) + ', "next_node_id":' + str(next_node) + '}')
                    po.update_poke_status(1)
                    ttl = self.client.time_to_end()
                    print(ttl, self.client.get_info())

    def on_edge(self, poke):
        """
        return : return the location of the pokemon , on which edge.
        returns : node1.id, node2.id
        """
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
        """
        returns: all the position of the nodes on the graph
        """
        pos_dict = {}
        for node in self.game_graph.get_graph().nodes.values():
            pos_dict[node.id] = node.pos
        return pos_dict
