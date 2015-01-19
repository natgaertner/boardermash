from collections import defaultdict
import csv
import skills
import random
from skills import elo
from sorted_collection import SortedCollection

STARTING_WIDTH = 20
ENDING_WIDTH = 20
MUTATION_CHANCE = 0.3
CONTROL_MUTATION_CHANCE = 1
REFRESH_RATE = 5
ec = elo.EloCalculator(k_factor=.01)
opposites = {skills.WIN:skills.LOSE,skills.LOSE:skills.WIN,skills.DRAW:skills.DRAW}
def median(l):
    if len(l) % 2 == 0:
        return (l[len(l)/2] + l[len(l)/2+1])/2.
    else:
        return l[len(l)/2]

def random_slice(lst, slice_len, min_slice_len):
    r = random.randint(-slice_len+min_slice_len ,len(lst)-min_slice_len)
    return lst[max(r,0):min(len(lst),r+slice_len)]

def calc_rating(winner_rating, loser_rating):
    return ec.new_rating(winner_rating, loser_rating, skills.WIN).mean, ec.new_rating(loser_rating, winner_rating, skills.LOSE).mean

def new_ratings(idx1,idx2, player_scores,outcome):
    (player1, rating1) = player_scores[idx1]
    (player2, rating2) = player_scores[idx2]
    new_rating1 = ec.new_rating(rating1,rating2, outcome)
    new_rating2 = ec.new_rating(rating2,rating1, opposites[outcome])
    player_scores.remove((player1,rating1))
    player_scores.remove((player2,rating2))
    player_scores.insert((player1,new_rating1.mean))
    player_scores.insert((player2,new_rating2.mean))
    return player_scores

def select_random_pair(players):
    return random.sample(players,2)

def select_close_pair(players, num_to_select):
    return random.sample(random_slice(players,num_to_select,2),2)

if __name__ == '__main__':
    players = range(2500)
    player_scores = SortedCollection([(i,10) for i in players],key=lambda (p,s):s)
    player_scores_copy = player_scores.copy()
    control_player_scores = SortedCollection([(i,10) for i in players],key=lambda (p,s):s)
    player_power = [(p,p) for p in players]
    feeling = dict(player_power)
    player_ranks = dict((p,i) for i,(p,s) in enumerate(player_power))
    player_pairings = dict((_,0) for _ in players)
    #voter_feelings = eval(open('voter_feelings').read())
    for _ in range(200000):
        if random.random() < MUTATION_CHANCE:
            (idx1,idx2) = select_random_pair(players)
        else:
            (idx1,idx2) = select_close_pair(players, max(ENDING_WIDTH, STARTING_WIDTH - _/1000))
        (player1,r) = player_scores[idx1]
        (player2,r) = player_scores[idx2]
        #(control_idx1,control_idx2) = select_random_pair(players)
        if random.random() < CONTROL_MUTATION_CHANCE:
            (control_idx1, control_idx2) = select_random_pair(players)
        else:
            (control_idx1,control_idx2) = select_close_pair(players, max(ENDING_WIDTH, STARTING_WIDTH - _/1000))
        (control_player1,r) = control_player_scores[control_idx1]
        (control_player2,r) = control_player_scores[control_idx2]
        player_scores_copy = new_ratings(idx1,idx2,player_scores_copy,skills.WIN if feeling[player1] > feeling[player2] else skills.LOSE)
        control_player_scores = new_ratings(control_idx1,control_idx2,control_player_scores,skills.WIN if feeling[control_player1] > feeling[control_player2] else skills.LOSE)
        if _ % REFRESH_RATE == REFRESH_RATE-1:
            player_scores = player_scores_copy.copy()
        if _ % 10000 == 10000-1:
            print "iterations: {i}".format(i=_)
            player_result_ranks = dict((p,i) for i,(p,s) in enumerate(player_scores))
            errors = sorted([abs(player_result_ranks[i] - player_ranks[i]) for i in players])
            control_player_result_ranks = dict((p,i) for i,(p,s) in enumerate(control_player_scores))
            control_errors = sorted([abs(control_player_result_ranks[i] - player_ranks[i]) for i in players])
            print 'experimental avg: {avg}, median: {median}'.format(avg=float(sum(errors))/len(errors), median=median(errors))
            print 'control avg: {avg}, median: {median}'.format(avg=float(sum(control_errors))/len(control_errors), median=median(control_errors))
    #print player_scores
