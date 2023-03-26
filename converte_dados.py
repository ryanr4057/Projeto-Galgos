import funções_ as f
import f_banco_avbs as fbd
import f_busca
import cria_bd_avb as avb

# avb.criar_tabela_AvBs()

avbs = fbd.buscar_todos_avb()
print(avbs[0])
for i in range(0,len(avbs)):
    if (avbs[i][7] >= 7 and avbs[i][8] < 2) or (avbs[i][8] >= 7 and avbs[i][7] < 2):
        race_id = f_busca.buscar_dog_rid(avbs[i][3])
        r_dist = f_busca.buscar_race_dist(race_id)
        d_a, d_b, venc = f.compara_av(race_id,avbs[i][3], avbs[i][4])
        if (d_a[15] >=2 and d_b[15] >=2):
            avb.inserir_Avb(r_dist[0],d_a[0], d_a[2], d_a[3], d_a[4] ,d_a[5], d_a[6], d_a[7], d_a[8], d_a[9], d_a[10], d_a[11], d_a[12], d_a[13], d_a[14], venc[11], d_b[0], d_b[2], d_b[3], d_b[4] ,d_b[5], d_b[6], d_b[7], d_b[8], d_b[9], d_b[10], d_b[11], d_b[12], d_b[13],d_b[14], venc[12], avbs[i][10] )


# race_id = f_busca.buscar_dog_rid(avbs[0][3])
