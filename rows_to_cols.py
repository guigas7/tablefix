#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd

# 2 days offset. It starts by the second line (first repeated patient entry)
lines = [{'day':'0', 'quests':[0, 1, 2]}, # linha 0
        {'day':'1', 'quests':[0, 2]}, # linha 1
        {'day':'2', 'quests':[0, 2]}, # linha 2
        {'day':'3', 'quests':[0, 2]},  # linha 3
        {'day':'4', 'quests':[0, 2]},  # linha 4
        {'day':'5', 'quests':[0, 2]},  # linha 5
        {'day':'6', 'quests':[0, 2, 3]},  # linha 6
        {'day':'7', 'quests':[0, 2]},  # linha 7
        {'day':'8', 'quests':[0, 2]},  # linha 8
        {'day':'9', 'quests':[0, 2]},  # linha 9
        {'day':'10', 'quests':[0, 2]},  # linha 10
        {'day':'11', 'quests':[0, 2]},  # linha 11
        {'day':'12', 'quests':[0, 2]},  # linha 12
        {'day':'13', 'quests':[0, 2]},  # linha 13
        {'day':'14', 'quests':[0, 2]},  # linha 14
        {'day':'15', 'quests':[0, 2]},  # linha 15
        {'day':'16', 'quests':[0, 2]},  # linha 16
        {'day':'17', 'quests':[0, 2]},  # linha 17
        {'day':'20', 'quests':[0, 2]},  # linha 18
        {'day':'23', 'quests':[0, 2]},  # linha 19
        {'day':'26', 'quests':[0, 2]},  # linha 20
        {'day':'29', 'quests':[0, 2]},  # linha 21
        {'day':'30', 'quests':[0, 2]},  # linha 22
        {'day':'30', 'quests':[]},  # linha 23 (pós)
]    

# List of questionaries, the destiny has to be filled individually for each line
quests = [{'short':'adcl', 'desc':'Avaliação diária, clínica e laboratorial', 'start_or':0, 'end_or':0,
           'start_loc':'data_da_avalia_o', 'end_loc':'avaliao_diria_clnica_e_laboratorial_complete'}, # quest 0
         {'short':'adip', 'desc':'Avaliação diária de imagem pulmonar', 'start_or':0, 'end_or':0,
          'start_loc':'data_tomo', 'end_loc':'avaliao_diria_de_imagem_pulmonar_complete'}, # quest 1
         {'short':'adpvgf', 'desc':'Avaliação diária de parâmetros ventilatórios, gasométricos e funcionais', 'start_or':0, 'end_or':0,
          'start_loc':'data_da_avalia_o_2', 'end_loc':'avaliao_diria_de_parmetros_ventilatrios_gasomtrico_complete'}, # quest 2
         {'short':'ade', 'desc':'Avaliação diária de eletrocardiograma', 'start_or':0, 'end_or':0,
          'start_loc':'data_eletro', 'end_loc':'avaliao_de_eletrocardiograma_complete'}, # quest 3
]



# Questionaries from last line of each entry, origin and destiny columns are the same
post = [{'desc':'Todos', 'start':0, 'end':0,
         'start_loc':'teste_cov_2', 'end_loc':'desfecho_da_uti_complete'}] # pos uti

# Create dataframe and column list
df = pd.read_csv('input.csv')
cols = df.columns.tolist()

# translate col names for col indexes (indexes can vary per quetionaries, names don't)
for q in quests:
    q['start_or'] = df.columns.get_loc(q['start_loc']);
    q['end_or'] = df.columns.get_loc(q['end_loc']);
# translate col names for col indexes
for p in post:
    p['start'] = df.columns.get_loc(p['start_loc']);
    p['end'] = df.columns.get_loc(p['end_loc']);

names = []
# For each possible line, for each questionary the current line can have, make new columns for all columns this questionary has, with the day in the column label
for l in range(2, len(lines)): # from day 2 to last (there's no day 0 and day 1 stays in place)
    for q in lines[l]['quests']: # for all questionaries in that line that need new columns
        for c in range(quests[q]['start_or'], quests[q]['end_or'] + 1): # for all columns from the questionary q
            name = quests[q]['short'] + ' ' + cols[c] + ' ' + 'dia ' + lines[l]['day']
            names.append(name)

# concatenate all newly created columns with the original dataframe in a new dataframe
new = pd.concat([df, pd.DataFrame(columns=list(names))], sort=False)

# assigns values for first entry so it can skip the "previous post icu" if
orig = 0
lin = 1
# foreach row, if different patient, keep his index. If same patient, copy the daily values to their newly assigned column
dup = df[cols[0]].duplicated() # says if each row is a duplicate or not
for count in new.index.values[1:].tolist(): # removes first patient so it doesn't fill previous entry's post columns
    if (dup[count] == False): # if new patient (not duplicate)
        # fill all post
        for p in post:
            for c in range(p['start'], p['end'] + 1):
                new.iloc[orig, c] = new.iloc[count - 1, c]
        # unable to drop repeated rows here withou messing with future indexes, dropping after all loops
        # new = new.drop(range(orig + 1, count)); # if orig + 1 and count are the same, it doesn't drop anyone
        orig = count # keep index
        lin = 1 # keep lines index aka first line of this entry
    else: # if same patient
        lin += 1 # increment the line index
        for q in lines[lin]['quests']: # for all quests that line lin can have
            start_d = new.columns.get_loc(quests[q]['short'] + ' ' + cols[quests[q]['start_or']] + ' ' + 'dia ' + lines[lin]['day'])
            end_d = new.columns.get_loc(quests[q]['short'] + ' ' + cols[quests[q]['end_or']] + ' ' + 'dia ' + lines[lin]['day'])
            # data goes to correct columns, acording to the day, counted by lin
            aux = quests[q]['start_or'] # aux keeps the origin indexes
            for c in range(start_d, end_d + 1): # c keeps the destiny indexes
                new.iloc[orig, c] = new.iloc[count, aux]
                aux += 1

# Checks duplicity in the first column, Keeps first entry
new = new.drop_duplicates(subset=[cols[0]])
# to export as csv
# new.to_csv('out.csv', index=False)
# pip install openpyxl 
new.to_excel("output.xlsx", sheet_name='Sheet_1', index=False)

# -- NOT USED --
# 
# Currently generating all new columns
# # Append all new daily columns, for all days
# con = pd.read_csv('concat.csv')
# final = pd.concat([df, con], sort=False)

#  Doing all at once since it's all in sequence and have destiny == origin
# # Questionaries that won't need new columns, origin and destiny columns are the same
# post = [{'desc':'Outros testes patogênicos', 'start':210, 'end':289}, # pos uti 0
#          {'desc':'Complicações', 'start':290, 'end':318}, # pos uti 1
#          {'desc':'Tratamentos', 'start':319, 'end':370}, # pos uti 2
#          {'desc':'Desfecho da UTI', 'start':371, 'end':385}, # pos uti 3
# ]
