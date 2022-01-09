

class pokemon():
    status=0
    src=0
    dest=0

    def __init__(self, value: int, type: int, pos : tuple):
        self.value = value
        self.type = type
        self.pos = pos
        self.src = 0
        self.dest = 0
        self.takenby = 9

    def pokemon_edge(self,id1_id2):
        if int(id1_id2[0])>=int(id1_id2[1]):
            src=int(id1_id2[1])
            dest=int(id1_id2[0])
        else:
            src=int(id1_id2[0])
            dest=int(id1_id2[1])
        if self.type>0: #src<dest
            self.src=src
            self.dest=dest
        else:
            self.src=dest
            self.dest=src


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

    def build_pokemon(pokemons: dict):
        pokemons_list = []
        for pok in pokemons['Pokemons']:  # O(1)
            for _,i in pok.items():
                value = i['value']
                type = i['type']
                pos = i['pos']
                curr_pok = pokemon(value , type , pos)
                pokemons_list.append(curr_pok)
        return pokemons_list

    def __str__(self):
        return f"pos:{str(self.pos)[1:-1]}"

    def update_poke_status(self,stat):
        self.status=stat

    def __repr__(self):
        return f"pos:{str(self.pos)[1:-1]}\n"

    def __le__(self,other):
        return self.value == other.value or self.value < other.value