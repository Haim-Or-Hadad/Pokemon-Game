"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import ast
from ctypes.wintypes import RGB

from pygame import display
from pygame.color import Color

from client import Client
import json
import pygame
from pygame import *
import math
from catch_algo import *
from game_display import *
from client_python.pokemon import pokemon
from src.GraphAlgo import GraphAlgo
from client_python.agent import Agent

# init pygame
WIDTH, HEIGHT = 1080, 720

#background
img = pygame.image.load("pokemons_logo/pokemon_sea.jpg")
img = pygame.transform.scale(img,(1080, 720))
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
count = 0
pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
pygame.display.set_caption('Resizable')
clock = pygame.time.Clock()
pygame.font.init()
# screen.fill([0, 100, 210])
screen.blit(img, (1080, 720))
pygame.display.update()
client = Client()
client.start_connection(HOST, PORT)

graph_json = client.get_graph()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
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

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
first_time = 0
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

    # refresh surface
    img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))
    screen.blit(img, (0,0))

    # screen.fill([0, 100, 210])
    game = game_display(screen, graph)
    # draw nodes
    for node in graph.get_graph().nodes.values():
        x = my_scale(node.x(), x=True)
        y = my_scale(node.y(), y=True)
        t = (x, y)
        t1 = (x + 1, y + 1.80)
        id_1 = FONT.render(str(node.id), False, RGB(25, 212, 120))
        screen.blit(id_1, t1)

        pygame.draw.circle(screen, RGB(118, 149, 195), t, 6)
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
            pygame.draw.line(screen, RGB(160, 27, 195), (src_x, src_y), (dest_x, dest_y), 3)
            # rotation = math.degrees(math.atan2(src_y - dest_y, dest_x - src_x)) + 90
            # pygame.draw.polygon(screen, (120, 120, 130), (
            #     (dest_x + 0.5 * math.sin(math.radians(rotation)), dest_y + 0.5 * math.cos(math.radians(rotation))),
            #     (
            #         dest_x + 15 * math.sin(math.radians(rotation - 158)),
            #         dest_y + 15 * math.cos(math.radians(rotation - 158))),
            #     (dest_x + 15 * math.sin(math.radians(rotation + 158)),
            #      dest_y + 15 * math.cos(math.radians(rotation + 158)))))

    # draw agents
    for age in agent_dict:
        pos_x = age.x()
        pos_y = age.y()
        pos_x = my_scale(pos_x, x=True)
        pos_y = my_scale(pos_y, y=True)
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (pos_x, pos_y), 10)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemon_dict:
        pos_x = p.x()
        pos_y = p.y()
        pos_x = my_scale(pos_x, x=True)
        pos_y = my_scale(pos_y, y=True)
        if 0 < p.value < 3:
            pok_image = pygame.image.load("pokemons_logo\weak_pokemon.png")
            pok_image = pygame.transform.scale(pok_image, (50, 30))
            screen.blit(pok_image,(pos_x, pos_y))

        if 3 <= p.value <= 5:
            pok_image = pygame.image.load("pokemons_logo\midium_pokemon.png")
            pok_image = pygame.transform.scale(pok_image, (50, 30))
            screen.blit(pok_image,(pos_x, pos_y))

        if 5 < p.value <= 7:
            pok_image = pygame.image.load("pokemons_logo\pikacho-modified.png")
            pok_image = pygame.transform.scale(pok_image, (50, 30))
            screen.blit(pok_image,(pos_x, pos_y))

        if 8 < p.value :
            pok_image = pygame.image.load("pokemons_logo\mu.png")
            pok_image = pygame.transform.scale(pok_image, (50, 30))
            screen.blit(pok_image,(pos_x, pos_y))

        #pygame.draw.circle(screen, Color(0, 255, 255), (pos_x, pos_y), 10)

    ####Timer and score####
    info=json.loads(client.get_info())
    score=info['GameServer']['grade']
    moves=info['GameServer']['moves']
    time=client.time_to_end()
    score_x=32
    score_y=34
    score_x = my_scale(score_x, x=True)
    score_y = my_scale(score_y, y=True)
    score = FONT.render(str(score), False, RGB(25, 212, 120))
    screen.blit(score,(score_x,score_y))

    # update screen changes
    display.update()
    # refresh rate
    clock.tick(10)
    if count == 335:
        catch = catch_algo(graph, client)
        check = client.get_info()
        catch.send_agent(agent_dict, pokemon_dict)
    # choose next
    else:
        catch = catch_algo(graph, client)
        check = client.get_info()
        catch.send_agent(agent_dict, pokemon_dict)
        client.move()
    count += 1

# game over: