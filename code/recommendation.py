import database_connection
import calculations
import pandas as pd

def make_recommendation(user_group):
    # features used to decribe tracks and users' music taste
    FEATURES = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']

    GROUP_IDS = database_connection.get_users_groups_ids(user_group)
    # get leaders' taste 
    LEADERS_TASTE = database_connection.get_leaders_taste(GROUP_IDS)

    group_taste_vector = calculations.cal_group_taste_vector(user_group, FEATURES, LEADERS_TASTE)
    print(calculations.convert_taste_vector_to_dict(group_taste_vector, FEATURES))

    # setting a curor to all of the top 50 tracks
    top_50_cursor = database_connection.get_top50_cursor()

    recommendation_df = pd.DataFrame(columns=["Name", "Artist", "Similarity"])

    for track in top_50_cursor:
        score = calculations.cal_simillarity(group_taste_vector, track, FEATURES)
        artists_string = ""
        n_artists = len(track['artists'])
        for i, artist in enumerate(track['artists']):
            if n_artists == 1:
                artists_string = artist
            if n_artists > 1 and i < (n_artists - 1):
                artists_string += artist + ', '
            if n_artists > 1 and i == (n_artists - 1):
                artists_string += artist

        recommendation_df.loc[len(recommendation_df)]= [track['name'], artists_string, score]
    # calculating simillarity between group's music taste
    # and a track
    recommendation_df = recommendation_df.sort_values(by=['Similarity'], ascending=False).head(20)
    print("avg simmilarity", recommendation_df["Similarity"].mean())
    print("max simmilarity",recommendation_df["Similarity"].max())
    print("min simmilarity",recommendation_df["Similarity"].min())

    return recommendation_df