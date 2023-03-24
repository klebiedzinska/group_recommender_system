import database_connection, calculations
import pandas as pd
from itertools import combinations

distance_df = pd.DataFrame(columns=["Group 1", "Group 2", "Distance"])

groups = database_connection.get_groups()

ids = [group['id'] for group in groups]

combonations = combinations(ids, 2)

for (group_1, group_2) in list(combonations):
    for group in groups:
        if group['id'] == group_1:
            leader_taste_1 = list(group['leader_taste'].values())
        if group['id'] == group_2:
            leader_taste_2 = list(group['leader_taste'].values())

    distance_df.loc[len(distance_df)]= [group_1, group_2, calculations.get_distance_between_points(leader_taste_1, leader_taste_2)]

print(distance_df.sort_values(by=['Distance'], ascending=False))

min_distance = calculations.get_distance_between_points(list(groups[0]['leader_taste'].values()), list(groups[0]['leader_taste'].values())) 
print(f'Minimum distance (between the same group): {min_distance}')
print(f'Maximum distance: {distance_df["Distance"].max()}')
print(f'Average distance: {distance_df["Distance"].mean()}')