import database_connection
import calculations
import pandas as pd
import random
from itertools import combinations
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy as np

import time
start_time = time.time()
users = []


# features used to decribe tracks and users' music taste
FEATURES = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']

USERS_IDS = database_connection.get_all_users_ids()

tracks = []
tracks_cursor = database_connection.get_top50_cursor()

for track in tracks_cursor:
    tracks.append(track)

top_50_cursor = database_connection.get_top50_cursor()

def get_similarities(user_group):
    users_in_group = [user for user in users if user['id'] in user_group]

    group_taste_vector = calculations.cal_group_taste_vector_usrarray(users_in_group, FEATURES)

    s = pd.Series()
    for track in tracks:

        score = calculations.cal_simillarity(group_taste_vector, track, FEATURES)
        score_series = pd.Series(data=score)
        s = s.append(score_series)
    s = s.sort_values(ascending=False).head(20)

    min_sim = s.min()
    max_sim = s.max()
    avg_sim = s.mean()
    

    return min_sim, max_sim, avg_sim


def get_similarities_combinations(number_of_users):
    min_similarities = []
    max_similarities = []
    avg_similarities = []
    groups = list(combinations(USERS_IDS, number_of_users))

    if number_of_users == 4:
        groups = random.choices(groups, k=len(groups)//5)
    elif number_of_users == 5:
        groups = random.choices(groups, k=len(groups)//10)

    for group in groups:
        print(group)
        min_sim, max_sim, avg_sim = get_similarities(group)
        min_similarities.append(min_sim)
        max_similarities.append(max_sim)
        avg_similarities.append(avg_sim)


    print(f'Min similarity for {number_of_users} users: {pd.Series(data=min_similarities).min()}')
    print(f'Max similarity for {number_of_users} users: {pd.Series(data=max_similarities).max()}')
    print(f'Avg similarity for {number_of_users} users: {pd.Series(data=max_similarities).mean()}')


if __name__ == '__main__':
    all_groups = database_connection.get_groups()

    for user in USERS_IDS:
        data = {}
        data['id'] = user
        data['group_id'] = database_connection.get_user_group(user)
        for group_in_all_groups in all_groups:
            if data['group_id'] == group_in_all_groups['id']:
                data['leader_taste'] = group_in_all_groups['leader_taste']

        data['music_taste'] = np.array(list(database_connection.get_user_taste(user).values()))
        
        users += [data]

    get_similarities_combinations(2)
    print("--- %s seconds ---" % (time.time() - start_time))