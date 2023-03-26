import f_banco_avbs as faaa
import cria_bd_avb as fb
import funções_ as f
import f_busca as fbd
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.feature_selection import SelectFromModel


ia = pickle.load(open('IA_81%.sav', 'rb'))

rf = pickle.load(open('forest.sav', 'rb'))


# fb.criar_tabela_AvBs()

def previsao_ia(n_a, n_b, ia, rf):
    race_id = fbd.buscar_dog_rid(n_a)
    r_dist = fbd.buscar_race_dist(race_id)
    d_a, d_b, venc = f.compara_av(race_id,n_a, n_b)
    X = [[r_dist[0], d_a[0], d_a[2],  d_a[3], d_a[4] ,d_a[5], d_a[6], d_a[7], d_a[8], d_a[9], d_a[10], d_a[11], d_a[12], d_a[13], d_a[14], venc[11], d_b[0], d_b[2], d_b[3], d_b[4] ,d_b[5], d_b[6], d_b[7], d_b[8], d_b[9], d_b[10], d_b[11], d_b[12], d_b[13], d_b[14], venc[12]]]

    selector = SelectFromModel(rf, prefit=True)
    X = selector.transform(X)

    res = ia.predict(X)
    return res

pred = previsao_ia('Ballyboss Sim','Merrymeeting Dev', ia, rf )

print(pred)
