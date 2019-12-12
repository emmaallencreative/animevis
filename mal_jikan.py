import requests
import doa
import logging

'''
Get data for one URL (/ - genres, synopsis, overall stats)
Create variable for 'id' in URL
Get idmal from main list, loop through - binary search tree
Get data from other three URLS:
/stats
/recommendations
/reviews
Increment ids and save last id to database
'''

d = doa.DOA('../animevis.db')
CURSOR = d.cursor
CONN = d.conn


def get_idmal():
    CURSOR.execute('''SELECT id,idmal FROM animelist WHERE idmal >= 1''')
    idlist = CURSOR.fetchall()
    return idlist


# Python code to convert into dictionary
def convert_dict(idlist):
    id_dict = {}
    for tup in idlist:
        id_dict[tup[1]] = tup[0]
    return id_dict


def convert_list(idlist):
    idmal_list = []
    for tup in idlist:
        idmal_list.append(tup[1])
    return idmal_list


def binary_search(idmal_list, end, find_idmal, start=0):
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
    url = f'https://api.jikan.moe/v3/anime/{idmal}/{tail}/'
    print(url)
    response = requests.post(url)
    return response.json()


# print(get_anime_data(1, 'stats'))

tups = get_idmal()
print(convert_dict(tups))
idmal_list = convert_list(tups)

print(binary_search(idmal_list, len(idmal_list)-1, 5))
