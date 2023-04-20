import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
import joblib
import pickle

conn = sqlite3.connect('IA_bd.sqlite3')


df = pd.read_sql_query("SELECT * from dados", conn)


X = df.drop(labels=['id', 'vencedor','d_brt_a', 'd_brt_b', 'pontos_a', 'pontos_b', 'dist_race'], axis=1)
y = df.vencedor

# rf = RandomForestClassifier(n_estimators=124, random_state=1, max_depth=3, max_leaf_nodes=5 )
# rf.fit(X, y)

# selector = SelectFromModel(rf, prefit=True)
# X = selector.transform(X.values)

# selected_features = selector.get_support()



# print("Features mais importantes selecionadas:")
# print(selected_features)

X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=2/3, random_state=1)

scaler = MinMaxScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

cls = MLPClassifier(hidden_layer_sizes=(2),
                    # learning_rate_init=0.002,
                    max_iter=10000,
                    random_state=1,
                    # beta_1= 0.84 ,
                    # beta_2= 0.999999,
                    # alpha = 0.0000002943,
                    # verbose= True,

                    )
cls.fit(X_train, y_train)
print(accuracy_score(y_test, cls.predict(X_test)))

print(cls.predict(X_test))
print(y_test.values)
# # print(y_test)
prob = cls.predict_proba(X_test)
print(prob)

# y_t

filename = 'IA_81%.sav'
pickle.dump(cls, open(filename, 'wb'))

# pickle.dump(rf, open('forest.sav', 'wb'))

pickle.dump(scaler, open('scaler.sav', 'wb'))




