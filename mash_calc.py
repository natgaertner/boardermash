import skills
import random
from skills import elo
from sorted_collection import SortedCollection

WINDOW_WIDTH = 40
MUTATION_RATE = 0.3
ec = elo.EloCalculator(k_factor=1)

def random_slice(lst, slice_len, min_slice_len):
    r = random.randint(-slice_len+min_slice_len ,len(lst)-min_slice_len)
    return lst[max(r,0):min(len(lst),r+slice_len)]

def calc_rating(winner_rating, loser_rating):
    return ec.new_rating(winner_rating, loser_rating, skills.WIN).mean, ec.new_rating(loser_rating, winner_rating, skills.LOSE).mean

def select_random_pair(players):
    return random.sample(players,2)

def select_close_pair(players, num_to_select):
    return random.sample(random_slice(players,num_to_select,2),2)

def select_pair(players):
    if random.random() < MUTATION_RATE:
        return select_random_pair(range(len(players)))
    else:
        return select_close_pair(range(len(players)), WINDOW_WIDTH)
