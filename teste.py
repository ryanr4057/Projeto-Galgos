import f_banco_avbs as faaa
import cria_bd_avb as fb
import funções_ as f
import f_busca as fbd
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.feature_selection import SelectFromModel


ia = pickle.load(open('IA_81%.sav', 'rb'))

rf = pickle.load(open('forest.sav', 'rb'))

scaler = pickle.load(open('scaler.sav', 'rb'))




# fb.criar_tabela_AvBs()

def previsao_ia(n_a, n_b):
    race_id = fbd.buscar_dog_rid(n_a)
    r_dist = fbd.buscar_race_dist(race_id)
    d_a, d_b, venc = f.compara_av(race_id,n_a, n_b)
    X = [[r_dist[0], d_a[0], d_a[2], d_a[3], d_a[4] ,d_a[5], d_a[6], d_a[7], d_a[8], d_a[9], d_a[10], d_a[11], d_a[12], d_a[13], venc[11], d_b[0], d_b[2], d_b[3], d_b[4] ,d_b[5], d_b[6], d_b[7], d_b[8], d_b[9], d_b[10], d_b[11], d_b[12], d_b[13], venc[12]]]

    selector = SelectFromModel(rf, prefit=True)
    X = selector.transform(X)

    X = scaler.transform(X)

    res = ia.predict(X)
    prob = ia.predict_proba(X)
    prob_a = prob[0][0]
    prob_b = prob[0][1]

    if prob_a > prob_b:
        # print(prob[0][0])
        pb = prob[0][0]

    elif prob_a < prob_b:
        # print(prob[0][1])
        pb = prob[0][1]

    return res, pb

def previsao_ia_t(n_a, n_b):
    race_id = fbd.buscar_dog_rid(n_a)
    r_dist = fbd.buscar_race_dist(race_id)
    d_a, d_b, venc = f.compara_av(race_id,n_a, n_b)
    stc_a = d_a[12]
    stc_b = d_b[12]
    X = [[r_dist[0], d_a[0], d_a[2], d_a[3], d_a[4] ,d_a[5], d_a[6], d_a[7], d_a[8], d_a[9], d_a[10], d_a[11], d_a[12], d_a[13], venc[11], d_b[0], d_b[2], d_b[3], d_b[4] ,d_b[5], d_b[6], d_b[7], d_b[8], d_b[9], d_b[10], d_b[11], d_b[12], d_b[13], venc[12]]]

    selector = SelectFromModel(rf, prefit=True)
    X = selector.transform(X)

    X = scaler.transform(X)

    res = ia.predict(X)
    prob = ia.predict_proba(X)
    prob_a = prob[0][0]
    prob_b = prob[0][1]


    if prob_a > prob_b:
        # print(prob[0][0])
        pb = prob[0][0]

    elif prob_a < prob_b:
        # print(prob[0][1])
        pb = prob[0][1]

    return res, pb, stc_a, stc_b, venc

def testa_pb():
    all_avbs = faaa.buscar_todos_avb()
    count = 0
    tot = 0
    marg = 0.9
    t =0

    for i in range(1, len(all_avbs) + 1):
        avb = faaa.busca_nomes(i)
        a = avb[3]
        b = avb[4]
        pred, pb, stc_a, stc_b, venc = previsao_ia_t(a,b)

        if pred[0] == avb[10]:
            if pb > marg:
                if venc[11] > venc[12] and pred[0] == 0:
                    count = count + 1
                    t = t + pb
                    print(f"{stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} 1")
                elif venc[11] < venc[12] and pred[0] == 1:
                    count = count + 1
                    t = t + pb
                    print(f"{stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} 2")
                elif venc[11] > 7 and pred[0] == 0:
                    count = count + 1
                    t = t + pb
                    print(f"{stc_a} - {stc_b} - {avb[10]} - {pred[0]} - {venc[11]} - {venc[12]} --{i} 3")
                elif venc[12] > 7 and pred[0] == 1:
                    count = count + 1
                    t = t + pb
                    print(f"{stc_a} - {stc_b} - {avb[10]} - {pred[0]} - {venc[11]} - {venc[12]} --{i} 4")

        if pb > marg:
            # if (pred[0] == avb[10] and (venc[11] > 7 or venc[12] > 7))  or (venc[11] > venc[12] and pred[0] == 0) or (pred[0] != avb[10] and ((pred[0] == 0 and venc[11] > 7 ) or (pred[0] == 1 and venc[12] > 7 ))) :
            #     tot = tot + 1
            #     print(f"{stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} tot1")
            # elif (pred[0] == avb[10] and (venc[11] > 7 or venc[12] > 7))  or (venc[11] < venc[12] and pred[0] == 1) or (pred[0] != avb[10] and ((pred[0] == 0 and venc[11] > 7 ) or (pred[0] == 1 and venc[12] > 7 ))) :
            #     tot = tot + 1
            #     print(f"{stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} tot2")

            # print(f"{stc_a} - {stc_b} - {avb[10]}")
            if venc[11] > venc[12] and pred[0] == 0:
                tot = tot + 1
                print(f"{stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} t1")
            elif venc[11] < venc[12] and pred[0] == 1:
                tot = tot + 1
                print(f"{stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} t2")
            elif venc[11] > 7 and pred[0] == 0:
                tot = tot + 1
                print(f"{stc_a} - {stc_b} - {avb[10]} - {pred[0]} - {venc[11]} - {venc[12]} --{i} t3")
            elif venc[12] > 7 and pred[0] == 1:
                tot = tot + 1
                print(f"{stc_a} - {stc_b} - {avb[10]} - {pred[0]} - {venc[11]} - {venc[12]} --{i} t4")


    print(" ")

    for i in range(1, len(all_avbs) + 1):
        avb = faaa.busca_nomes(i)
        a = avb[3]
        b = avb[4]
        pred, pb, stc_a, stc_b, venc = previsao_ia_t(a,b)

        if pred[0] != avb[10]:
            if pb > marg:
                if ((venc[11] > venc[12] and pred[0] == 0) and (pred[0] == 0 and venc[11] > 7)) :
                    print(f" erros {stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} 1")
                elif (venc[11] < venc[12] and pred[0] == 1) and (pred[0] == 1 and venc[12] > 7):
                    print(f" erros {stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} 2")
                elif (venc[11] > venc[12] and pred[0] == 0):
                    print(f" erros {stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} 3")
                elif (venc[11] < venc[12] and pred[0] == 1):
                    print(f" erros {stc_a} - {stc_b} - {avb[10]} - {venc[11]} - {venc[12]} --{i} 4")

    print(count)
    print(tot)
    print(count/tot)
    print(t/count)

def previsao(a,b,venc):
    marg = 0.9
    vencedor = 3

    pred, pb = previsao_ia(a,b)
    print(pred[0])
    print(pb)

    if pb > marg:
        if venc[11] > venc[12] and pred[0] == 0 and (venc[11] > 5 and venc[12] < 2) :
            vencedor = 0

        elif venc[11] < venc[12] and pred[0] == 1 and (venc[12] > 5 and venc[11] < 2):
            vencedor = 1

        elif venc[11] > 7 and pred[0] == 0:
            vencedor = 0

        elif venc[12] > 7 and pred[0] == 1:
            vencedor = 1

    return vencedor

# testa_pb()

avb = faaa.busca_nomes(18)
a = avb[3]
b = avb[4]

race_id = fbd.buscar_dog_rid(a)
r_dist = fbd.buscar_race_dist(race_id)
d_a, d_b, venc = f.compara_av(race_id,a,b)

print(previsao(a,b, venc))
