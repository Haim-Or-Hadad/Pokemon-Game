from queue import PriorityQueue


class Agent:

    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: tuple):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
        self.agent_path = [self.src]
        self.last_dest = 0
        self.Direction = None

    def last_item(self):
        if len(self.agent_path) > 0:
            return self.agent_path[len(self.agent_path) - 1]

    def update_der(self, dir):
        self.Direction = dir

    def update_path(self, short_path: list, po):
        for n in short_path:
            #if n not in self.agent_path:
            self.agent_path.append(n)
        # if self.Direction is None:
        #     self.agent_path.append(po.dest)
        # if po.src <= po.dest and po.dest not in self.agent_path and self.Direction == "LEFT":
        #     self.agent_path.append(po.dest)
        # if po.src >= po.dest and po.dest not in self.agent_path and self.Direction == "RIGHT":
        #     self.agent_path.append(po.dest)
        if po.dest not in self.agent_path:
            self.agent_path.append(po.dest)

    def show_path(self):
        if len(self.agent_path) > 0:
            return self.agent_path[0]

    def print_path(self):
        print("Agent path: ", str(self.agent_path)[1:-1])

    def path_size(self):
        return len(self.agent_path)

    def get_path(self):
        if len(self.agent_path) > 0:
            if self.last_dest == self.agent_path[0]:
                self.last_dest = self.agent_path[0]
                self.agent_path.pop(0)
            return self.agent_path.pop(0)

    def remove_element(self):
        self.agent_path.pop(0)

    def x(self):
        if type(self.pos) == tuple:
            return float(self.pos[0])
        elif type(self.pos) == list:
            return float(self.pos[0])
        else:
            check = list(self.pos.split(","))
            return float(check[0])

    def y(self):
        if type(self.pos) == tuple:
            return float(self.pos[1])
        elif type(self.pos) == list:
            return float(self.pos[1])
        else:
            check = list(self.pos.split(","))
            return float(check[1])

    def build_agent(agents: dict):
        agent_list = []
        for a in agents['Agents']:  # O(1)
            for _, i in a.items():
                curr_agent = Agent(i['id'], i['value'],
                                   i['src'], i['dest'],
                                   i['speed'], i['pos'])
                agent_list.append(curr_agent)
        return agent_list

    def update_agent_dict(agent_list: dict, from_server: dict):
        for a in from_server['Agents']:
            for _, i in a.items():
                A_id = int(i['id'])
                agent_list[A_id].value = i['value']
                agent_list[A_id].src = i['src']
                agent_list[A_id].dest = i['dest']
                agent_list[A_id].speed = i['speed']
                agent_list[A_id].pos = i['pos']
