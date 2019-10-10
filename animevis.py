import requests
import sqlite3
import logging

CONN = sqlite3.connect('test.db')
CURSOR = CONN.cursor()
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
    Check the rate limit - stop for two minutes if hit
    Write code to retrieve request header
    Iterate through pages
    Keep track of scraped pages
    Keep track of anime id
    Validate each missing id once - sends email to verify
    Schedule - run every specific day
    Update database for last scraped page and anime id
    Git
    :return:
    """
    pass

def create_tables():
    sql_create_table = """ CREATE TABLE IF NOT EXISTS pagination (
                                            last_scraped_page integer,
                                            last_scraped_anime_id integer
                                        ); """
    CURSOR.execute(sql_create_table)

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
        logging.error("I'm sending this date {}-{}-{}".format(str(animedate['year']),
                                                              str(animedate['month']),
                                                              str(animedate['day'])))
        return str(animedate['year']) + '-' + str(animedate['month']) + '-' + str(animedate['day'])
    return ""


def insert_anime_data(anilistid, malid, title, startdate, enddate, season):
    CURSOR.execute("""INSERT INTO animelist (id, idmal, title, startdate, enddate, season) 
    VALUES (?,?,?,?,?,?)""",
    (anilistid, malid, title, startdate, enddate, season))

    CONN.commit()


def parse_anime_data(data):
    media = data['data']['Page']['media']
    for anime in media:
        title = anime['title']['userPreferred']
        anilistid = anime['id']
        malid = anime['idMal']
        startdate = has_anime_ended_or_started(anime['startDate'])
        enddate = has_anime_ended_or_started(anime['endDate'])
        season = anime['season']
        insert_anime_data(anilistid, malid, title, startdate, enddate, season)


def database_qc(action):
    if action == 'select':
        CURSOR.execute('''SELECT * FROM animelist''')
        data = CURSOR.fetchall()
        print(data)
    elif action == 'delete':
        CURSOR.execute('''DELETE FROM animelist where id > 0''')


def page_turner():
    ratelimitremaining = 1
    has_next_page = True
    page = 1
    while ratelimitremaining and has_next_page:
        print(ratelimitremaining, has_next_page, page)
        ratelimitremaining, data = get_anime_data(page)
        parse_anime_data(data)
        has_next_page = data['data']['Page']['pageInfo']['hasNextPage']
        page += 1



# database_qc('delete')
# page_turner()

# database_qc('select')
# database_qc('delete')
#
# print('deleted database')

# database_qc('select')


