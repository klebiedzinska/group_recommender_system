import database_connection
from scipy.spatial import distance
import numpy as np

# function determinating user's music taste
def cal_user_taste(userID, features):
    taste = {}
    tracks = database_connection.get_user_tracks(userID)
    nb_tracks = len(tracks)
    
    for track in tracks:
        trackFeatures = database_connection.get_track_features(track['_id'], features)        
        for feature in features:            
            track[feature] = trackFeatures[feature]
            
    dominator = sum(range(1,nb_tracks+1))
    
    for feature in features:
        numerator = sum(track[feature] * (nb_tracks - track['rank']) for track in tracks)
        
        taste[feature] = numerator/dominator
    
    return taste


def get_min_distance_from_centroid(group_index, taste_array, labels, centroids):
    return min(get_distance_from_centroid(point, group_index, centroids) for point in taste_array[labels == group_index])


def get_distance_from_centroid(point, group_index, centroids):
    return distance.euclidean(point, centroids[group_index])


def get_distance_between_points(point_1, point_2):
    return distance.euclidean(point_1, point_2)


def cal_group_taste_vector(user_ids, features, leaders_taste):  
    divisor = 2 * len(user_ids)
    dividend = np.array([0 for _ in features])
    
    for user_id in user_ids:
        user_taste = np.array(list(database_connection.get_user_taste(user_id).values()))
        user_leader_taste = np.array(list(database_connection.get_users_leader_taste(user_id, leaders_taste).values()))
        dividend = dividend + user_taste + user_leader_taste 

    return  dividend / divisor

def cal_group_taste_vector_usrarray(users, features):  
    divisor = 2 * len(users)
    dividend = np.array([0 for _ in features])

    for user in users:
        user_taste = user['music_taste']
        user_leader_taste = user['leader_taste']
        dividend = dividend + user_taste +  np.array(list(user_leader_taste.values()))

    return  dividend / divisor


def convert_taste_vector_to_dict(taste_vector, features):
    return {feature: taste_vector[i]  for i, feature in enumerate(features)}


def cal_simillarity(taste_vector, track, features):
    track_features = np.array([track[feature] for feature in features])
    return np.dot(taste_vector, track_features)