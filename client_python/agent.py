from queue import PriorityQueue


class Agent:
    agent_path = [0]
    last_dest = 0

    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: tuple):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

    def last_item(self):
        if len(self.agent_path) > 0:
            return self.agent_path[len(self.agent_path)-1]

    def update_path(self, short_path: list, id2: int):
        for n in short_path:
            if n not in self.agent_path:
                self.agent_path.append(n)
        # if id2 not in self.agent_path:
        # self.agent_path.append(id2)
        print(self.agent_path)

    def show_path(self):
        if len(self.agent_path) > 0:
            return self.agent_path[0]

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
