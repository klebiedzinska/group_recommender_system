# Group recommender system supporting music selection

## What is it?
A system that provides personalised recommendation for a group of users.

## Used technologies
- *MongoDB*
- *Spotify API*
- *Python* (SciPy, NumPy, Pandas, Matplotlib, PyMongo, Flask)

## Methodology
- Clustering (Kmeans)
- Calculating similarity (dot product)
- Calculating distance in multidimensional space (Euclidean distance)

## The files
The repository consists of the following files:
- main - used to launch the app,
- before_recommendation - prepares the data and inserts it to the database,
- recommendation - makes the recommendation for a group of users,
- calculations - implements the functions used for calculating the music taste and the similarity between a user and a track,
- spotify_connection - makes a connection with a Spotify API. Implements a function used for the tracks' features extraction,
- database_connection - makes a connection with a MongoDB. Implements fuctions used to insert and select data,
- elbow - the elbow a method used to determine the optimal number of clusers.

## Stage 1: Preparing the data
### Tracks features extraction
Tracks are represented as data points in 7-dimensional space, with each dimension corresponding to a numeric feature extracted from the Spotify API.

### Music taste
Users' music taste is calculated using weighted arithmetic mean of their most listened tracks. In this way, users are also represented as data points in the same 7-dimensional space and their position can be compared to the tracks.

### K-means clustering
K-means clustering is used to group users by their music taste. To each group, a group leader is assigned - the closest user to a centroid.

### Inserting the data to a database
All of the prepared data is necessary to make recommendations for the end user. It is inserted and stored in the database for a later useage to avoid the repeatition and making the algorithm more optimised.

## Stage 2: Making recommendations
### Calculating the group's music taste
Recommendation is made for a group of users selected by the end user. The group's music taste is calculated by adding the taste of all users in the group with their group leaders. The sum is then divided by two times the number of members in the group. 
<!-- ![an equation used to calculate the group's music taste](./readme_images/groups_taste_equation.png) -->
<p align="center">
<img src="./readme_images/groups_taste_equation.png"  width="20%" height="20%">
<p>
where $n$ is the number of users, $u_i$ is the user's music taste and $l_i$ is a music taste of a group leader, which the $u_i$ user was assigned to during clustering.

### Recommending the most similar tracks
The similarity between all of the tracks in a database and the previously calculated group's music taste is determined using dot product. The tracks are sorted in descending order. The 20 most similar tracks are recommended to the end user.