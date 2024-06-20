#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd

def post_uti_index_of(first_index, df, max):
    record_id = df.iloc[first_index, 0]
    for i in range(first_index, first_index + 25):
        if (df.iloc[i,0] != record_id):
            return i - 1
        elif (i == max):
            return i
        
def fill_quests(line, df, quests, origin):
    for q in quests:
        for col in range(q['start'], q['end'] + 1):
            df.iloc[line, col] = df.iloc[origin, col]
    return df
        
# List of questionaries, the destiny has to be filled individually for each line
admiss = [
    {'short':'admiss1', 'start':0, 'end':0, 'start_loc':'inicias_do_paciente',
    'end_loc':'avaliao_diria_de_imagem_pulmonar_complete'}, # first columns of admission

    {'short':'admiss2', 'start':0, 'end':0, 'start_loc':'monitoria_completa',
    'end_loc':'monitoria_complete'}, # last columns of admission
]

# Questionaries from last line of each entry, origin and destiny columns are the same
post = [{'short':'postuti', 'start':0, 'end':0, 'start_loc':'teste_cov_2',
          'end_loc':'desfecho_da_uti_complete'}] # pos uti

# Create dataframe and column list
df = pd.read_csv('input.csv')

# translate col names for col indexes (indexes can vary per quetionaries, names don't)
for q in admiss:
    q['start'] = df.columns.get_loc(q['start_loc'])
    q['end'] = df.columns.get_loc(q['end_loc'])

for p in post:
    p['start'] = df.columns.get_loc(p['start_loc'])
    p['end'] = df.columns.get_loc(p['end_loc'])

dup = df.iloc[:, 0].duplicated() # Says if each row is a duplicate on record_id or not
max = len(dup) - 1 # Last element index
# Initializes lists only with indexes of first entry of each patient
dups = []
for i in range(0, len(dup)):
    if (dup[i] == False): # Keeps only first Entry of each record_id
        dups.append(i) # Insert index of first entry of new patient

# For each new patient, finds his post uti line index, copies its post uti quests in the original line and: In each subsequent line
# of the same patient, copies the content of admiss quests from the original line and copies the content of post quests from post uti line
for orig in dups:
    post_index = post_uti_index_of(orig, df, max)
    # Fill post quests in original line
    df = fill_quests(orig, df, post, post_index)
    # For each subsequent line of the same patient
    for line in range(orig + 1, post_index + 1):
        df = fill_quests(line, df, post, post_index) # Fill post quests
        df = fill_quests(line, df, admiss, orig) # Fill admiss quests

# to export as csv
# df.to_csv('out.csv', index=False)
# pip install openpyxl 
df.to_excel("output.xlsx", sheet_name='Sheet_1', index=False)

