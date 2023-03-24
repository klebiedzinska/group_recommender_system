import database_connection
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

from yellowbrick.cluster.elbow import KElbowVisualizer

FEATURES = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']
USERS_IDS = database_connection.get_all_users_ids()

# create a DataFrame containing userID and their music taste
col_names = ['userID'] + FEATURES

df = pd.DataFrame(columns = col_names)

for userID in USERS_IDS:
    taste = database_connection.get_user_taste(userID)
    taste_list = [taste[feature] for feature in FEATURES]
    df.loc[len(df)]= [userID] + taste_list


taste_array = df.iloc[:,1:].values

nb_clusters = range(1,10)

elbow = []

for i in nb_clusters:
    kmeans = KMeans(n_clusters=i, random_state=0).fit(taste_array)
    elbow.append(kmeans.inertia_)

plt.rc('font', size=15)
plt.figure(figsize=(10,5))
plt.plot(nb_clusters, elbow, 'bx-')
plt.xlabel('Liczba klastrów')
plt.ylabel('Suma kwadratów odległości punktów od najbliższej centroidy')
plt.title('Metoda łokcia')
plt.savefig('elbow.png', bbox_inches='tight')