from patient import Patient
import helpers as handle
import sofa as sofa
from datetime import datetime
import pandas as pd
import sys

inputSheet = 'input.xlsx'
outputSheet = 'nomerepetidos.xlsx'
outputText = 'nomerepetidos.txt'

df = pd.read_excel(inputSheet, sheet_name='Página 1', engine="openpyxl")

# Make sure all cells are strings
df['Paciente'] = df['Paciente'].astype('str') 
df['Paciente'] = df['Paciente'].str.strip().str.upper() # Clean trailing and preceding spaces // makes all upper case
df['Destino alta'] = df['Destino alta'].astype('str')
# df['Hospital'] = df['Hospital'].astype('str')
df['UTI'] = df['UTI'].astype('str')
# Converting to int first to avoid decimal places from float64
df['Registro'] = df['Registro'].astype('Int64', errors='ignore').astype('str')
df['Prontuário'] = df['Prontuário'].astype('Int64', errors='ignore').astype('str')
# Just in case the dates aren't being infered correctly
df['Data/horário internamento'] = pd.to_datetime(df['Data/horário internamento'], format="%d/%m/%Y %H:%M:%S", errors='coerce')
df['Data alta'] = pd.to_datetime(df['Data alta'], format="%d/%m/%Y %H:%M", errors='coerce')
# Ignores the time from the timestamp
# df['Data/horário internamento'] = df['Data/horário internamento'].dt.date
# df['Data alta'] = df['Data alta'].dt.date

df['Hospital'] = df['UTI'].apply(lambda x: x.split(' ')[0])

dups = df.duplicated(subset=['Paciente', 'Hospital', 'Data/horário internamento', 'Registro', 'Prontuário', 'Data alta', 'Data nascimento'])

onlyDup = df.iloc[dups[dups].index.tolist()]

with open(outputText, "a") as f:
    f.write('x-----x Removendo pacientes duplicados:\n')
    for name in onlyDup['Paciente']:
        f.write(name + '\n')
    f.write('x-----x Pacientes duplicados removidos!\n')

onlyDup.to_excel(outputSheet, sheet_name="Página 1", index=False)
