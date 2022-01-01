


class agent():

    def __init__(self, id: int, value: float, src : int, dest : int , speed: float, pos : tuple):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

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
            for _,i in a.items():
                curr_agent = agent(i['id'], i['value'] ,
                                 i['src'], i['dest'],
                                 i['speed'],i['pos'])
                agent_list.append(curr_agent)
        return agent_list
