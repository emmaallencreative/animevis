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
targets = [column header of seasons, the numerical one] 
features = [column header of Score, Popularity]
y (answers) = df.columns[targets]
x (data) = df.columns[features]
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

    print(data)

sql_pull_score_season_popularity()

# iris = load_iris()
# test_idx = [0, 50, 100]
#
# train_target = np.delete(iris.target, test_idx)
# train_data = np.delete(iris.data, test_idx, axis=0)
#
# test_target = iris.target[test_idx]
# test_data = iris.data[test_idx]
#
# clf = tree.DecisionTreeClassifier()
# clf.fit(train_data, train_target)
#
# array = np.empty((2,4))


# #['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
# print(test_data)
# #print(clf.predict(array))
#
# dot_data = StringIO()
# tree.export_graphviz(clf,
#                      out_file=dot_data,
#                      feature_names=iris.feature_names,
#                      class_names=iris.target_names,
#                      filled=True, rounded=True,
#                      impurity=False)
#
# graph = pydot.graph_from_dot_data(dot_data.getvalue())
# graph.write_pdf('Graph.pdf')

