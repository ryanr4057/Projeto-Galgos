import funções_ as f
import f_busca as fb
import teste as ia

def merge_sort(arr, race_id):
    if len(arr) > 1:
        meio = len(arr) // 2
        esq = arr[:meio]    #cria um array pegando os dados do arr da posição 0 até o meio(incluso o meio).
        dir = arr[meio:]    #cria um array pegando os dados do arr da posição meio + 1(meio não incluso) até o fim.

        merge_sort(esq, race_id)
        merge_sort(dir, race_id)

        i = j = k = 0

        while i < len(esq) and j < len(dir):
            d_a, d_b, venc = f.compara_av(race_id,esq[i][0],dir[j][0])
            p_esq = venc[11]
            p_dir = venc[12]
            # if (ia.previsao_tc(esq[i][0],dir[j][0],venc) == 0):
            #     p_esq = 1
            #     p_dir = 0
            # elif (ia.previsao_tc(esq[i][0],dir[j][0],venc) == 1):
            #     p_esq = 0
            #     p_dir = 1

            if p_esq > p_dir:
                arr[k] = esq[i]
                i += 1
            else:
                arr[k] = dir[j]
                j += 1
            k += 1

        while i < len(esq):
            arr[k] = esq[i]
            i += 1
            k += 1


        while j < len(dir):
            arr[k] = dir[j]
            j += 1
            k += 1

    return arr

def pontos(arr, race_id):
    top_3 = arr[:3]
    lay_3 = arr[3:]
    points = []
    traps = []

    for t in range(0, len(arr)):
        tr = fb.buscar_dog_trap(arr[t][0])
        traps.append(tr[0])

    for i in range(0,len(top_3)):
        for j in range(0, len(lay_3)):
            # print(j)
            d_a, d_b, venc = f.compara_av(race_id, top_3[i][0], lay_3[j][0])
            p_esq = venc[11]
            p_dir = venc[12]
            points.append(p_esq)
            # print(f"{top_3[i][0]} - {p_esq} vs {lay_3[j][0]} - {p_dir}")

    return points, traps

def verifica_pts(arr):
    result = 1
    for i in range(0, len(arr)):
        if arr[i] < 1:
            result = 0

    return result


all_races = fb.buscar_todas_races_id()

for race in all_races:
    dogs = fb.buscar_dogs_por_race(race)

    podium = merge_sort(dogs, race)

    points, traps = pontos(podium, race)

    horario = fb.buscar_race_h(race[0])
    nome = fb.buscar_race_nome(race[0])
    pista_id = fb.buscar_race_pis(race[0])
    pista_nome = fb.buscar_pista_nome(pista_id[0])

    if (verifica_pts(points) == 1):
        print(f"{pista_nome[0]} {nome[0]} {horario[0]} - {traps[:3]}")
        # print(podium)
