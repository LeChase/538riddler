"""
monte carlo simulation for batting streak

https://fivethirtyeight.com/features/can-the-riddler-bros-beat-joe-dimaggios-hitting-streak/
"""

import numpy as np
import time
from multiprocessing import Process


N_sims = 10000000
streak = 57
bats_at_game = 4


class Riddler:

    def __init__(self, ba, career_games):
        self.ba = ba
        self.career_games = career_games
        self.hit_in_game_prob = 1 - (1 - ba)**bats_at_game
        # 'H' is a game with a hit, 'N' is a game with no hits...
        self.prob_dict = {'H': self.hit_in_game_prob, 'N': 1 - self.hit_in_game_prob}
                
    def consecutive_prob(self, streak):
        return sum(''.join(np.random.choice(list(self.prob_dict.keys()), 
                                            size = self.career_games, 
                                            p = list(self.prob_dict.values()))).count('H'*streak) > 0 
                    for _ in range(N_sims))/N_sims

    def solve(self):
        start = time.time()
        str1 = str(round(100*self.consecutive_prob(streak), 2)) + ' %' + ' chance of attaining a %d game \
            hitting streak over %d games, with a %.2f batting average' % (streak, self.career_games, self.ba)
        str2 = 'duration: ' + str(round(time.time() - start, 2)) + ' seconds'

        print(str1)
        print(str2)


def main():

    player_dict = {0.200: 3200,
                    0.250: 3200,
                    0.300: 3200,
                    0.350: 3200,
                    0.400: 3200,
                    0.500: 1600}

    processes = []
    for batting_avg, n_games in player_dict.items():
        player = Riddler(ba = batting_avg, career_games = n_games)
        trial = Process(target = player.solve)
        trial.start()
        processes.append(trial)

    for trial in processes:
        trial.join()



if __name__ == '__main__':

    main()