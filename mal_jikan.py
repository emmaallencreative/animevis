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
    Remember where it was an start again
    """
    print("Hello!")
    for idmal in idmal_list:
        main_tail = get_anime_data(idmal, '')
        stats_tail = get_anime_data(idmal, 'stats')
        recommendations_tail = get_anime_data(idmal, 'recommendations')
        reviews_tail = get_anime_data(idmal, 'reviews')
        route_tail_data(main_tail, stats_tail, recommendations_tail, reviews_tail, idmal)
        break



def route_tail_data(main_tail, stats_tail, recommendations_tail, reviews_tail, idmal):
    """
    Further work needed on genre and then add here
    Add description db insert
    Add recommendations db insert
    Add reviews text db insert
    Add review scores db insert
    """
    scores_data = parse_stats_tail(stats_tail, main_tail, idmal)
    #insert_scores_data(scores_data, idmal)


def parse_stats_tail(stats_tail, main_tail, idmal):
    scores_dict = {'watching': stats_tail['watching'],
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
                       'averagescore': main_tail['score'],
                       'scoredby': main_tail['scored_by'],
                       'alltimerank': main_tail['rank'],
                       'popularityrank': main_tail['popularity'],
                       'popularityvolume': main_tail['members'],
                       'favorites': main_tail['favorites'],
                  }
    return(scores_dict)

def insert_scores_data(scores_dict, idmal):
    CURSOR.execute("""INSERT INTO mal_jikan_scores (id, watching, completed, on_hold, dropped, plan_to_watch, 
    status_total, scores_1_votes, scores_1_percentage, scores_2_votes, scores_2_percentage, scores_3_votes, 
    scores_3_percentage, scores_4_votes, scores_4_percentage, scores_5_votes, scores_5_percentage, 
    scores_6_votes, scores_6_percentage, scores_7_votes, scores_7_percentage, scores_8_votes, scores_8_percentage,
     scores_9_votes, scores_9_percentage, scores_10_votes, scores_10_percentage, averagescore, scoredby, alltimerank, 
     popularityrank, popularityvolume, favorites) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                   (hex_dict[idmal],
                    scores_dict['watching'],
                    scores_dict['completed'],
                    scores_dict['on_hold'],
                    scores_dict['dropped'],
                    scores_dict['plan_to_watch'],
                    scores_dict['total'],
                    scores_dict['scores_1_votes'],
                    scores_dict['scores_1_percentage'],
                    scores_dict['scores_2_votes'],
                    scores_dict['scores_2_percentage'],
                    scores_dict['scores_3_votes'],
                    scores_dict['scores_3_percentage'],
                    scores_dict['scores_4_votes'],
                    scores_dict['scores_4_percentage'],
                    scores_dict['scores_5_votes'],
                    scores_dict['scores_5_percentage'],
                    scores_dict['scores_6_votes'],
                    scores_dict['scores_6_percentage'],
                    scores_dict['scores_7_votes'],
                    scores_dict['scores_7_percentage'],
                    scores_dict['scores_8_votes'],
                    scores_dict['scores_8_percentage'],
                    scores_dict['scores_9_votes'],
                    scores_dict['scores_9_percentage'],
                    scores_dict['scores_10_votes'],
                    scores_dict['scores_10_percentage'],
                    scores_dict['averagescore'],
                    scores_dict['scoredby'],
                    scores_dict['alltimerank'],
                    scores_dict['popularityrank'],
                    scores_dict['popularityvolume'],
                    scores_dict['favorites'],
                    ))
    CONN.commit()

def parse_genres(main_tail):
    genres_list = []
    for genre in main_tail['genres']:
        genres_list.append(genre['name'])
    return genres_list


def parse_main_tail(main_tail):
    main_dict = {'description': main_tail['synopsis'],
                      'background': main_tail['background'],
                      'genres': parse_genres(main_tail),
                 }
    return(main_dict)

def insert_genres_data(main_dict, idmal):
    for genre in main_dict['genres']:
        CURSOR.execute("""INSERT INTO mal_jikan_genres (id, genre) 
        VALUES (?,?)""",
                       (hex_dict[idmal],
                        main_dict[genre]))
        CONN.commit()


def parse_recommendations_tail(recommendations_tail):
    recommendations_list = []
    for recommendation in recommendations_tail['recommendations']:
        del recommendation['recommendation_url']
        del recommendation['url']
        del recommendation['image_url']
        recommendations_list.append(recommendation)
    return(recommendations_list)


def parse_reviews_tail(reviews_tail):
    reviews_list = []
    for review in reviews_tail['reviews']:
        del review['url']
        del review['type']
        del review['reviewer']['url']
        del review['reviewer']['image_url']
        del review['reviewer']['username']
        reviews_list.append(review)
    return(reviews_list)

# print(get_anime_data(1, 'stats'))

tups = get_idmal()
hex_dict = convert_dict(tups)
idmal_list = convert_list(tups)

#print(binary_search(idmal_list, len(idmal_list)-1, 5))

#print(get_anime_tail_data(idmal_list))

#main_tail = get_anime_tail_data(idmal_list)

#print(parse_main_tail(main_tail))



#recommendations_tail = get_anime_tail_data(idmal_list)

#print(parse_recommendations_tail(recommendations_tail))

#reviews_tail = get_anime_tail_data(idmal_list)

#print(parse_reviews_tail(reviews_tail))


get_anime_tail_data(idmal_list)