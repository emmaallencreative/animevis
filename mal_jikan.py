import requests
import doa
import logging

'''
Get data for one URL (/ - genres, synopsis, overall stats)
Create variable for 'id' in URL
Get data from other three URLS:
/stats
/recommendations
/reviews
Increment ids and save last id to database
'''

def get_anime_data(idmal, tail=''):
    url = f'https://api.jikan.moe/v3/anime/{idmal}/{tail}/'
    print(url)
    response = requests.post(url)
    return response.json()


print(get_anime_data(1, 'stats'))