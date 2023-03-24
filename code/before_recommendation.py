import database_connection, calculations
import pandas as pd
from sklearn.cluster import KMeans

# features used to decribe tracks and users' music taste
FEATURES = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']

database_connection.insert_all_users_data()
USERS_IDS = database_connection.get_all_users_ids()

users_db, top50tracks_db, groups_db = database_connection.get_collections()

database_connection.insert_top_50_tracks_data(FEATURES)

# deretminating music taste of ALL of the users
# inserting music taste of ALL of the users to database
for user_id in USERS_IDS:
        database_connection.set_user_taste(user_id, calculations.cal_user_taste(user_id, FEATURES))

# create a DataFrame containing userID and their music taste
col_names = ['userID'] + FEATURES

df = pd.DataFrame(columns = col_names)

for userID in USERS_IDS:
    taste = database_connection.get_user_taste(userID)
    taste_list = [taste[feature] for feature in FEATURES]
    df.loc[len(df)]= [userID] + taste_list


# using the right number of clusters
N_CLUSTERS = 4

taste_array = df.iloc[:,1:].values

kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=0).fit(taste_array)
labels = kmeans.labels_

centroids = kmeans.cluster_centers_
centroids_labels = kmeans.predict(centroids)

# get a leader of each group
group_leaders = {}

for group_index in range(N_CLUSTERS):
    min_distance = calculations.get_min_distance_from_centroid(group_index, taste_array, labels, centroids)
    
    for point in taste_array[labels == group_index]:
        if(calculations.get_distance_from_centroid(point, group_index, centroids) == min_distance):
            group_leaders[group_index] = point

database_connection.set_group_leaders(group_leaders, FEATURES)

# assign clusters to users in MongoDB
for user_id in USERS_IDS:
    database_connection.set_user_group(user_id, int(labels[user_id - 1]))