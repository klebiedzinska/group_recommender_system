# connecting to mongoDB
from pymongo import MongoClient
import os
import json

import spotify_connection

cluster = MongoClient("mongodb+srv://admin:PmeRVCdURKCzq5VM@cluster0.gcllvtk.mongodb.net/?retryWrites=true&w=majority")

db = cluster["thesis"]
# connecting to collections
users_db = db["users"]
top50tracks_db = db["top 50 tracks"]
groups_db = db["groups"]

def get_collections():
    return users_db, top50tracks_db, groups_db

def get_groups():
    groups = []

    for group in groups_db.find():
        groups.append({'id': group['_id'], 'leader_taste': group['leaderTaste']})


    return groups


def get_all_users_ids():
    return users_db.distinct('_id')


def get_users_by_groupid(group_id):
    return users_db.find({"group": {"$in": group_id}})


def get_top50_cursor():
    return top50tracks_db.find()


def insert_all_users_data():   
    # assign directory
    directory = '..\\json'

    list_files = sorted(os.listdir(directory), key=lambda name: int(name.split('.')[0]))

    for key, filename in enumerate(list_files):
        key += 1
        
        f = os.path.join(directory, filename)
        
        # open a file with top 50 most listened songs by one user
        with open(f, encoding='utf-8') as file:
            data = json.load(file)
            
            # a list of the top 50 tracks
            tracks_to_db = []
            
            # for every track on the list, add it to the list of tracks
            for rank, track in enumerate(data['items']):        
                
                artists_to_db = []
                
                for artist in track['artists']:
                    artists_to_db.append({"_id": artist['id'], 
                                    "name": artist['name']})
                
                track_to_db = {"_id": track['id'],
                            "name": track['name'],
                            "rank": rank,
                            "artists": artists_to_db}
                
                # add the track to the list of top 50 tracks
                tracks_to_db.append(track_to_db)
                
        #add a user and their top 50 tracks to the database
        users_db.insert_one({"_id": key, 
                        "tracks": tracks_to_db})


def insert_top_50_tracks_data(features):
    distinct_tracks = users_db.distinct("tracks._id")

    for track in distinct_tracks:
        track_info = spotify_connection.get_track_data(track)
    
        while True:
            try:
                features_values = spotify_connection.get_audio_features(track)[0]
                break
            except:
                pass

        result = {feature: features_values[feature] for feature in features}
        result['_id'] = features_values['id']
        result['name'] = track_info['name']
        result['artists'] = [artist['name'] for artist in track_info['artists']]    
        
        top50tracks_db.insert_one(result)


  # get user's top 50 stongs' features
def get_user_tracks(userID):
    return users_db.find_one({"_id": userID})['tracks']


# get track's features
def get_track_features(trackID, features):
    track = top50tracks_db.find_one({"_id": trackID})
    return {feature: track[feature] for feature in features}


# set user's taste
def set_user_taste(user_id, taste):
    users_db.update_one({"_id": user_id}, {"$set": {"taste": taste}})


def get_user_taste(user_id):
    return users_db.find_one({"_id": user_id})['taste']


# add groups and group leaders to MongoDB
def set_group_leaders(group_leaders, features):  
    for key, group_leader_taste in group_leaders.items():
        leader_taste_dict = {feature: group_leader_taste[i] for i, feature in enumerate(features)}
        groups_db.insert_one({"_id": key, 
                        "leaderTaste": leader_taste_dict})


# user_group - a list of users ids (a group made for recommendation)
def get_users_groups_ids(user_group):
    return users_db.distinct('group', 
                              {"_id": {"$in": user_group}})


# user_group - a list of users ids (a group made for recommendation)
def get_leaders_taste(user_group):
    return list(groups_db.find({"_id": {"$in": user_group}}))


def get_user_group(user_id):
    return users_db.find_one({"_id": user_id})['group']

def get_group_leader_taste(group_id, LEADERS_TASTE):
    for leader_taste in LEADERS_TASTE:
        if(leader_taste['_id'] == group_id):
            return leader_taste['leaderTaste']
        
def get_users_leader_taste(user_id, LEADERS_TASTE):
    return get_group_leader_taste(get_user_group(user_id), LEADERS_TASTE)

def set_user_group(user_id, group_number):
    users_db.update_one({"_id": user_id}, {"$set": {"group": group_number}})
