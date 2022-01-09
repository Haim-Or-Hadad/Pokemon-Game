"""
@authors Haim Or Hadad , Ilan Gold
OOP - Ex4
"""
import ast

import json

from pygame import *
from catch_algo import *
from client_python.button import Button
from game_display import *
from client_python.pokemon import pokemon
from src.GraphAlgo import GraphAlgo
from client_python.agent import Agent

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
count = 0
pygame.init()
#background
img = pygame.transform.scale(pygame.image.load("pokemons_logo/pokemon_sea.jpg"),(WIDTH, HEIGHT))
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
pygame.display.set_caption('POKEMON GAME')
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('ebrima', 20, bold=True)
screen.blit(img, (WIDTH, HEIGHT))
pygame.display.update()
client = Client()
client.start_connection(HOST, PORT)

# GET GRAPH FROM SERVER
graph_json = client.get_graph()
graph_json = ast.literal_eval(graph_json)
graph = GraphAlgo()
graph = graph.load_from_json(graph_json)


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, graph.min_x(), graph.max_x())
    if y:
        return scale(data, 50, screen.get_height() - 50, graph.min_y(), graph.max_y())


radius = 15

client.add_agent("{\"id\":0}")
client.add_agent("{\"id\":1}")
client.add_agent("{\"id\":2}")
client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()


######agents into dict####
agent_dict1 = json.loads(client.get_agents())
agent_dict = Agent.build_agent(agent_dict1)
while client.is_running() == 'true':
    agent_dict1 = json.loads(client.get_agents())
    Agent.update_agent_dict(agent_dict, agent_dict1)
    ######pokemons into dict####3
    pokemon_dict = json.loads(client.get_pokemons())
    pokemon_dict = pokemon.build_pokemon(pokemon_dict)
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if WIDTH-110 < pos[0] < WIDTH and HEIGHT-95 < pos[1] < HEIGHT:
                Client.stop()

        # refresh surface
    img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
    screen.blit(img, (0,0))
    game = game_display(screen, graph)

   # draw edges
    for e in graph.get_graph().nodes.values():
        src_x = e.x()
        src_y = e.y()
        list_out = graph.get_graph().all_out_edges_of_node(e.id)
        src_x = my_scale(src_x, x=True)
        src_y = my_scale(src_y, y=True)
        for edge in list_out:
            dest_x = graph.get_graph().nodes.get(edge).x()
            dest_y = graph.get_graph().nodes.get(edge).y()
            dest_x = my_scale(dest_x, x=True)
            dest_y = my_scale(dest_y, y=True)
            pygame.draw.line(screen, RGB(0,0,10), (src_x, src_y), (dest_x, dest_y), 5)

        # draw nodes
    for node in graph.get_graph().nodes.values():
        x = my_scale(node.x(), x=True)
        y = my_scale(node.y(), y=True)
        t = (x, y)
        t1 = (x - 8, y - 10)
        pygame.draw.circle(screen, RGB(60, 60, 60), t, 22)
        pygame.draw.circle(screen, RGB(180, 255, 100), t, 18)
        id_1 = FONT.render(str(node.id), False, RGB(25, 212, 120))
        screen.blit(id_1, t1)

    # draw agents
    for age in agent_dict:
        pos_x = age.x()
        pos_y = age.y()
        pos_x = my_scale(pos_x, x=True)
        pos_y = my_scale(pos_y, y=True)
        ball_image = pygame.image.load("pokemons_logo/ball.png")
        ball_image = pygame.transform.scale(ball_image, (50, 30))
        screen.blit(ball_image, (pos_x-15 , pos_y-15 ))

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemon_dict:
        pos_x = p.x()
        pos_y = p.y()
        pos_x = my_scale(pos_x, x=True)
        pos_y = my_scale(pos_y, y=True)
        if 0 < p.value < 5 and p.type < 0:
            pok_image = pygame.image.load("pokemons_logo/blue_1.png")
            pok_image = pygame.transform.scale(pok_image, (50, 30))
            screen.blit(pok_image,(pos_x-15, pos_y-15))

        if 5 <= p.value and p.type < 0:
            pok_image = pygame.image.load("pokemons_logo/blue_2.png")
            pok_image = pygame.transform.scale(pok_image, (50, 30))
            screen.blit(pok_image,(pos_x-15, pos_y-15))

        if 0 < p.value <= 5 and p.type >= 0:
            pok_image = pygame.image.load("pokemons_logo/red_1.png")
            pok_image = pygame.transform.scale(pok_image, (50, 30))
            screen.blit(pok_image,(pos_x-15, pos_y-15))

        if 5 <= p.value and  p.type >= 0:
            pok_image = pygame.image.load("pokemons_logo/red_2.png")
            pok_image = pygame.transform.scale(pok_image, (50, 30))
            screen.blit(pok_image,(pos_x-15, pos_y-15))


    ####Timer and score####
    info=json.loads(client.get_info())
    ###time###
    time = client.time_to_end()
    time_to_end = Button('TIME TO END:'+str(time),(100, 70))
    time_to_end.render(screen,(55,0))
    ###score###
    score=info['GameServer']['grade']
    score = Button('score:'+str(score), (100, 70))
    score.render(screen, (WIDTH-100, 0))
    ###moves###
    moves=info['GameServer']['moves']
    moves = Button('moves'+str(moves), (100, 70))
    moves.render(screen, (WIDTH-200, 0))
    ###stop###
    stop = Button('STOP',(130,100))
    stop.render(screen,(WIDTH-110,HEIGHT-95))



    # update screen changes
    display.update()
    # refresh rate
    clock.tick(9.5)
    catch = catch_algo(graph, client)
    check = client.get_info()
    catch.send_agent(agent_dict, pokemon_dict)
    client.move()

# game over: