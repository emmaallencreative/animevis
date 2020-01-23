import requests
import doa
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
    Parse returns
    Create database
    Remember where it was an start again
    """
    print("Hello!")
    for idmal in idmal_list:
        stats_tail = get_anime_data(idmal, 'stats')
        recommendations_tail = get_anime_data(idmal, 'recommendations')
        reviews_tail = get_anime_data(idmal, 'reviews')
        break
    return stats_tail

# print(get_anime_data(1, 'stats'))

tups = get_idmal()
print(convert_dict(tups))
idmal_list = convert_list(tups)

#print(binary_search(idmal_list, len(idmal_list)-1, 5))

print(get_anime_tail_data(idmal_list))


