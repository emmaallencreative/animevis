import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
import pydotplus as pydot
import sqlite3
import os

conn = sqlite3.connect(r'C:/Users/em100/Documents/Data/anime_visualisation_project/animevis.db')
cursor = conn.cursor()
os.environ['PATH'] = os.environ['PATH']+';'+os.environ['CONDA_PREFIX']+r"\Library\bin\graphviz"

'''


'''

def sql_pull_score_season_popularity():
    sql_query = '''SELECT animelist.title, animelist.season, mal_jikan_scores.averagescore,
                            mal_jikan_scores.popularityvolume
                            FROM animelist
                            INNER JOIN mal_jikan_scores
                            ON animelist.id = mal_jikan_scores.id
                            WHERE animelist.season IS NOT NULL
                            AND mal_jikan_scores.averagescore IS NOT NULL
                            AND mal_jikan_scores.popularityvolume IS NOT NULL;'''
    data = pd.read_sql_query(sql_query, conn)

    return data

data = sql_pull_score_season_popularity()

targets = ['season']
features = ['averagescore', 'popularityvolume']
data.replace(['WINTER', 'SPRING', 'SUMMER', 'FALL'], [0, 1, 2, 3], inplace=True)
y = data.loc[:, targets]
x = data.loc[:, features]

print(data)

test_idx = [27, 130, 206, 540]

train_target = y.drop(test_idx)
train_data = x.drop(test_idx)

test_target = y.loc[test_idx, :]
test_data = x.loc[test_idx, :]

clf = tree.DecisionTreeClassifier()
clf.fit(train_data, train_target)

print(test_data)
print(clf.predict(test_data))

dot_data = StringIO()
tree.export_graphviz(clf,
                     out_file=dot_data,
                     feature_names=['Average Score', 'Popularity Volume'],
                     class_names=['WINTER', 'SPRING', 'SUMMER', 'FALL'],
                     filled=True, rounded=True,
                     impurity=False)

graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf('Score_Popularity_Season_Graph.pdf')

