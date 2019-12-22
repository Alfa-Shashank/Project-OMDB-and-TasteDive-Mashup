# Project-OMDB-and-TasteDive-Mashup


import requests_with_caching
import json

#fetches the results of the passed movies  
def get_movies_from_tastedive(name):
    parameters = {"q": name, "type": "movies", "limit": 5}
    tastedive_response = requests_with_caching.get("https://tastedive.com/api/similar", params=parameters)
    py_data = json.loads(tastedive_response.text)
    return py_data
#this function extracts the list of titles of the movies from the dictionary recieved from get_movies_from_tastedive
def extract_movie_titles(dic):
    title = list()
    info = dic["Similar"]["Results"]
    for movie in info:
        title.append(movie["Name"])
    return title
# It gets five related movies for each from TasteDive, extracts the titles for all of them, and combines them all into a single list.
def get_related_titles(list_of_movie_title):
    print(list_of_movie_title)
    li = []
    for title in list_of_movie_title:
        a = get_movies_from_tastedive(title)
        b = extract_movie_titles(a)
        for movie in b:
            if movie not in li:
                li.append(movie)
    return li

#retrives data of the movie from the given api adn returns a dictionary
def get_movie_data(movie_name):
    parameters = {'t': movie_name, 'r': 'json'} #json is the pre-defined value for 'r', refer documentation provided
    omdbapi_response = requests_with_caching.get('http://www.omdbapi.com/', params=parameters)
    a = json.loads(omdbapi_response.text)
    return a
#gets the movie rating called rotten tomatoes
def get_movie_rating(dic):
    if len(dic['Ratings']) > 1:
        if dic['Ratings'][1]['Source'] == 'Rotten Tomatoes':
            rating = dic['Ratings'][1]['Value'][:2]
            rating = int(rating)
    else:        
        rating = 0
    return rating

def getkey(item):
    return item[1]


def get_sorted_recommendations(list_of_movies):
    related_movies = get_related_titles(list_of_movies)
    ratings = list()
    sorted_list = list()
    for movie in related_movies:
        a = get_movie_data(movie)
        ratings.append(get_movie_rating(a))
        
    temp_tuple1 = zip(related_movies, ratings)
    temp_tuple2 = sorted(temp_tuple1, key=getkey, reverse=True)
    print(temp_tuple2)
    for i in range(len(temp_tuple2) - 1):
        if temp_tuple2[i][0] not in sorted_list:
            if temp_tuple2[i][1] == temp_tuple2[i + 1][1]:
                if temp_tuple2[i][0] < temp_tuple2[i + 1][0]:
                    sorted_list.append(temp_tuple2[i + 1][0])
                    sorted_list.append(temp_tuple2[i][0])
            else:
                sorted_list.append(temp_tuple2[i][0])

    print(sorted_list)

    return sorted_list
