

class pokemon():
    status=0
    def __init__(self, value: int, type: int, pos : tuple):
        self.value = value
        self.type = type
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