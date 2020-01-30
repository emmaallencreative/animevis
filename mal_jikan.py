import requests
from python import doa
import time
import logging

'''
Increment ids and save last id to database
'''

d = doa.DOA('../animevis.db')
CURSOR = d.cursor
CONN = d.conn


def get_idmal():
    """
    Getting our unique ids and available idmals from the anime database
    """
    CURSOR.execute('''SELECT id,idmal FROM animelist WHERE idmal >= 1''')
    idlist = CURSOR.fetchall()
    return idlist


# Python code to convert into dictionary
def convert_dict(idlist):
    """
    Converting tuples into a dictionary and making idmal the key.
    So we can look up idmal to find unique identifier (id)
    """
    id_dict = {}
    for tup in idlist:
        id_dict[tup[1]] = tup[0]
    return id_dict


def convert_list(idlist):
    """
    Get list of just idmals
    """
    idmal_list = []
    for tup in idlist:
        idmal_list.append(tup[1])
    return idmal_list


def binary_search(idmal_list, end, find_idmal, start=0):
    """
    We do not know why we did this. Please send help. We wanted to find idmal or a line in the table.
    """
    idmal_list.sort()
    print(idmal_list)
    while start <= end:
        mid = int(start + (end-start)/2)
        if idmal_list[mid] == find_idmal:
            return mid
        elif idmal_list[mid] < find_idmal:
            start = mid+1
        else:
            end = mid-1
    return -1


def get_anime_data(idmal, tail=''):
    """
    Getting json data from Jikan/My Anime List
    """
    url = f'https://api.jikan.moe/v3/anime/{idmal}/{tail}/'
    print(url)
    response = requests.post(url)
    time.sleep(2)
    return response.json()

def get_anime_tail_data(idmal_list):
    """
    Looping through idmal's and returning data for 3 tails
    TODO:
    Parse returns (add to for loop when adding to database)
    Create database
    Remember where it was an start again
    """
    print("Hello!")
    for idmal in idmal_list:
        stats_tail = get_anime_data(idmal, 'stats')
        recommendations_tail = get_anime_data(idmal, 'recommendations')
        reviews_tail = get_anime_data(idmal, 'reviews')
        break
    return reviews_tail

def parse_stats_tail(stats_tail):
    stats_dict = {'watching': stats_tail['watching'],
                      'completed': stats_tail['completed'],
                      'on_hold': stats_tail['on_hold'],
                      'dropped': stats_tail['dropped'],
                      'plan_to_watch': stats_tail['plan_to_watch'],
                       'total': stats_tail['total'],
                       'scores_1_votes': stats_tail['scores']['1']['votes'],
                       'scores_1_percentage': stats_tail['scores']['1']['percentage'],
                       'scores_2_votes': stats_tail['scores']['2']['votes'],
                       'scores_2_percentage': stats_tail['scores']['2']['percentage'],
                       'scores_3_votes': stats_tail['scores']['3']['votes'],
                       'scores_3_percentage': stats_tail['scores']['3']['percentage'],
                       'scores_4_votes': stats_tail['scores']['4']['votes'],
                       'scores_4_percentage': stats_tail['scores']['4']['percentage'],
                       'scores_5_votes': stats_tail['scores']['5']['votes'],
                       'scores_5_percentage': stats_tail['scores']['5']['percentage'],
                       'scores_6_votes': stats_tail['scores']['6']['votes'],
                       'scores_6_percentage': stats_tail['scores']['6']['percentage'],
                       'scores_7_votes': stats_tail['scores']['7']['votes'],
                       'scores_7_percentage': stats_tail['scores']['7']['percentage'],
                       'scores_8_votes': stats_tail['scores']['8']['votes'],
                       'scores_8_percentage': stats_tail['scores']['8']['percentage'],
                       'scores_9_votes': stats_tail['scores']['9']['votes'],
                       'scores_9_percentage': stats_tail['scores']['9']['percentage'],
                       'scores_10_votes': stats_tail['scores']['10']['votes'],
                       'scores_10_percentage': stats_tail['scores']['10']['percentage'],
                      'datasource': 2}
    return(stats_dict)

def parse_recommendations_tail(recommendations_tail):
    recommendations_list = []
    for recommendation in recommendations_tail['recommendations']:
        del recommendation['recommendation_url']
        recommendations_list.append(recommendation)
    return(recommendations_list)

def parse_reviews_tail(reviews_tail):
    reviews_list = []
    for review in reviews_tail['reviews']:
        del review['mal_id']
        del review['type']
        del review['reviewer']['url']
        del review['reviewer']['image_url']
        del review['reviewer']['username']
        reviews_list.append(review)
    return(reviews_list)

# print(get_anime_data(1, 'stats'))

tups = get_idmal()
print(convert_dict(tups))
idmal_list = convert_list(tups)

#print(binary_search(idmal_list, len(idmal_list)-1, 5))

#print(get_anime_tail_data(idmal_list))

reviews_tail = get_anime_tail_data(idmal_list)

print(parse_reviews_tail(reviews_tail))


