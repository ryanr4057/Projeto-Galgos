import func2

pistas_links = func2.coleta_pistas()

# print(pistas_links)
pistas_races = func2.coleta_races(pistas_links)
# print(pistas_races[0])

# print(pistas_races[2])

# pistas_links = ['#meeting-races/track_id=63&r_date=2023-02-14&race_id=1960198&races_ids=1960198,1960199,1960200,1960201,1960202,1960203,1960204,1960205,1960206,1960207&r_time=08:12&tab=card', '#meeting-races/track_id=7&r_date=2023-02-14&race_id=1959996&races_ids=1959996,1959997,1959998,1959999,1960000,1960001,1960002,1960003,1960004,1960005,1960006,1960007&r_time=10:46&tab=card', '#meeting-races/track_id=11&r_date=2023-02-14&race_id=1960298&races_ids=1960298,1960299,1960300,1960301,1960302,1960303,1960304,1960305,1960306,1960307,1960308,1960309&r_time=10:53&tab=card', '#meeting-races/track_id=4&r_date=2023-02-14&race_id=1960284&races_ids=1960284,1960285,1960286,1960287,1960288,1960289,1960290,1960291,1960292,1960293,1960294,1960295,1960296,1960297&r_time=13:49&tab=card', '#meeting-races/track_id=5&r_date=2023-02-14&race_id=1960056&races_ids=1960056,1960057,1960058,1960059,1960060,1960061,1960062,1960063,1960064,1960065,1960066,1960067,1960068,1960069&r_time=13:57&tab=card', '#meeting-races/track_id=98&r_date=2023-02-14&race_id=1959911&races_ids=1959911,1959912,1959913,1959914,1959915,1959916,1959917,1959918,1959919,1959920,1959921,1959922&r_time=18:09&tab=card', '#meeting-races/track_id=1&r_date=2023-02-14&race_id=1960310&races_ids=1960310,1960311,1960312,1960313,1960314,1960315,1960316,1960317,1960318,1960319,1960320&r_time=18:17&tab=card', '#meeting-races/track_id=57&r_date=2023-02-14&race_id=1960261&races_ids=1960261,1960262,1960263,1960264,1960265,1960266,1960267,1960268,1960269,1960270&r_time=18:53&tab=card', '#meeting-races/track_id=62&r_date=2023-02-14&race_id=1960233&races_ids=1960233,1960234,1960235,1960236,1960237,1960238,1960239,1960240,1960241,1960242,1960243,1960244&r_time=11:06&tab=card', '#meeting-races/track_id=70&r_date=2023-02-14&race_id=1960083&races_ids=1960083,1960084,1960085,1960086,1960087,1960088,1960089,1960090,1960091,1960092&r_time=11:43&tab=card', '#meeting-races/track_id=61&r_date=2023-02-14&race_id=1960156&races_ids=1960156,1960157,1960158,1960159,1960160,1960161,1960162,1960163,1960164,1960165,1960166,1960167&r_time=14:04&tab=card', '#meeting-races/track_id=34&r_date=2023-02-14&race_id=1960107&races_ids=1960107,1960108,1960109,1960110,1960111,1960112,1960113,1960114,1960115,1960116,1960117,1960118&r_time=18:19&tab=card', '#meeting-races/track_id=6&r_date=2023-02-14&race_id=1960221&races_ids=1960221,1960222,1960223,1960224,1960225,1960226,1960227,1960228,1960229,1960230,1960231,1960232&r_time=18:26&tab=card', '#meeting-races/track_id=34&r_date=2023-02-14&race_id=1960119&races_ids=1960119,1960120&r_time=21:31&tab=card']
# pista_races = ['#card/track_id=63&race_id=1960198&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960199&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960200&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960201&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960202&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960203&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960204&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960205&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960206&r_date=2023-02-14&tab=form', '#card/track_id=63&race_id=1960207&r_date=2023-02-14&tab=form']


dogs = func2.coleta_dogs_races(pistas_races)

dog = dogs[0][2][3]

dog_dados = func2.coleta_hist_dog_aux(dog)

print(len(dog_dados))

print(dog_dados[1])
