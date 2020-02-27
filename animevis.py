import requests
import logging
import time
import uuid
import doa

d = doa.DOA('../animevis.db')
CURSOR = d.cursor
CONN = d.conn

logging.basicConfig(filename='animevis.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def create_query_template():
    logging.info("Creating query template")
    query = '''
    query (
      $page: Int,
      $type: MediaType,
      $format: MediaFormat,
      $startDate: String,
      $endDate: String,
      $season: MediaSeason,
      $genres: [String],
      $genresExclude: [String],
      $isAdult: Boolean = false, # Assign default value if isAdult is not included in our query variables 
      $sort: [MediaSort],
    ) {
      Page (page: $page) {
        pageInfo {
          total
          perPage
          currentPage
          lastPage
          hasNextPage
        }
        media (
          startDate_like: $startDate, # "2017%" will get all media starting in 2017, alternatively you could use the lesser & greater suffixes
          endDate_like: $endDate,
          season: $season,
          type: $type,
          format: $format,
          genre_in: $genres,
          genre_not_in: $genresExclude,
          isAdult: $isAdult,
          sort: $sort,
        ) {
          id
          idMal
          title {
            userPreferred
            romaji
            english
            native
          }
          synonyms
          description
          type
          source
          format
          status
          episodes
          genres
          studios {
              edges {
                  node {
                      id
                      name
                  }
                  id
                  isMain
              }
          }
          averageScore
          popularity
          rankings {
              id
              rank
              type
              format
              year
              season
              context
              allTime
          }
          stats {
              scoreDistribution {
                  score
                  amount
              }
              statusDistribution {
                  status
                  amount
              }
          }
          relations {
              edges {
                  id
                  relationType
                  node {
                      id
                      title {
                          userPreferred
                      }
                  }
              }
          }
          tags {
              id
              name
              rank
          }
          updatedAt
          startDate {
            year
            month
            day
          }
          endDate {
            year
            month
            day
          }
          season
        }
      }
    }
    '''
    return query


def monitor_pagination():
    """
    TODO
    Validate each missing id once - sends email to verify
    Time series rating data
    See Air Master 6da5f9fabcd2450bbf7a0970a1b16ecb for incorrect dates, incorrect idmal and extra number on anilistid
    Need to resolve above
    :return:
    """
    pass


def get_anime_data(page):
    variables = {
        'page': page,
        'perPage': 5
    }
    url = 'https://graphql.anilist.co'
    query = create_query_template()
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    ratelimitremaining = response.headers['X-RateLimit-Remaining']
    return ratelimitremaining, data


def has_anime_ended_or_started(animedate):
    if animedate:
        # logging.error("I'm sending this date {}-{}-{}".format(str(animedate['year']),
        #                                                       str(animedate['month']),
        #                                                       str(animedate['day'])))
        return str(animedate['year']) + '-' + str(animedate['month']) + '-' + str(animedate['day'])
    return ""

def insert_animelist_data(animelist_dict):
    CURSOR.execute("""INSERT INTO animelist (id, idanilist, idmal, title, startdate, enddate, season) 
    VALUES (?,?,?,?,?,?,?)""",
                   (animelist_dict['unique_id'],
                    animelist_dict['idanilist'],
                    animelist_dict['idmal'],
                    animelist_dict['title'],
                    animelist_dict['startdate'],
                    animelist_dict['enddate'],
                    animelist_dict['season']))
    CONN.commit()


def parse_animelist_data(unique_id, anime):
    animelist_dict = {'unique_id': unique_id,
                      'title': anime['title']['userPreferred'],
                      'idanilist': anime['id'],
                      'idmal': anime['idMal'],
                      'startdate': has_anime_ended_or_started(anime['startDate']),
                      'enddate': has_anime_ended_or_started(anime['endDate']),
                      'season': anime['season']}
    insert_animelist_data(animelist_dict)


def insert_details_data(details_dict):
    CURSOR.execute("""INSERT INTO details (id, description, status, format, animesource, episodes, datasource
) 
    VALUES (?,?,?,?,?,?,?)""",
                   (details_dict['unique_id'],
                    details_dict['description'],
                    details_dict['status'],
                    details_dict['format'],
                    details_dict['animesource'],
                    details_dict['episodes'],
                    details_dict['datasource']))
    CONN.commit()


def parse_details_data(unique_id, anime):
    details_dict = {'unique_id': unique_id,
                      'description': anime['description'],
                      'status': anime['status'],
                      'format': anime['format'],
                      'animesource': anime['source'],
                      'episodes': anime['episodes'],
                      'datasource': 1}
    insert_details_data(details_dict)


def parse_anime_data(data):
    media = data['data']['Page']['media']
    for anime in media:
        unique_id = uuid.uuid4().hex
        idanilist = anime['id']
        parse_animelist_data(unique_id, anime)
        parse_details_data(unique_id, anime)
    return idanilist



def page_turner():
    ratelimitremaining = 1
    has_next_page = True
    page = get_last_scrapped_page()
    while has_next_page:
        print(ratelimitremaining, has_next_page, page)
        ratelimitremaining, data = get_anime_data(page)
        last_idanilist = parse_anime_data(data)
        has_next_page = data['data']['Page']['pageInfo']['hasNextPage']
        logging.debug(f"Page has been parsed, data entered for page {page} and last AniList id was {last_idanilist}")
        page += 1
        rate_limit_checker(ratelimitremaining)
        insert_pagination_data(page, last_idanilist)


def insert_pagination_data(page, last_idanilist):
    CURSOR.execute("""INSERT INTO pagination (last_scraped_page, last_scraped_anime_id)
    VALUES (?,?)""",
                   (page, last_idanilist))

    CONN.commit()


def get_last_scrapped_page():
    CURSOR.execute('''SELECT MAX(last_scraped_page) FROM pagination''')
    highest_page = CURSOR.fetchone()
    logging.debug(f"The highest page is {highest_page[0]}")
    if highest_page[0] is None:
        return 1
    else:
        return highest_page[0]


def rate_limit_checker(ratelimitremaining):
    logging.debug(f"Rate limit remaining is {ratelimitremaining}")
    if not ratelimitremaining:
        logging.debug("I've slept for 60 seconds")
        time.sleep(60)


page_turner()



