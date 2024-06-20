from patient import Patient
import helpers as handle
import sofa as sofa
from datetime import datetime
import pandas as pd
import sys

inputSheet = 'input.xlsx'
outputSheet = 'output.xlsx'
outputText = 'output.txt'

df = pd.read_excel(inputSheet, sheet_name='Página 1', engine="openpyxl")

with open(outputText, "w") as f:
    f.write('Importação concluída\n')

# Saves the parent row of all transfer rows
cameFrom = {}

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
df['Data/horário internamento'] = df['Data/horário internamento'].dt.date
df['Data alta'] = df['Data alta'].dt.date

df['Hospital'] = df['UTI'].apply(lambda x: x.split(' ')[0])

dups = df.duplicated(subset=['Paciente', 'Hospital', 'Data/horário internamento', 'Registro', 'Prontuário', 'Data alta', 'Data nascimento'])

onlyDup = df.iloc[dups[dups].index.tolist()]

with open(outputText, "a") as f:
    f.write('x-----x Removendo pacientes duplicados:\n')
    for name in onlyDup['Paciente']:
        f.write(name + '\n')
    f.write('x-----x Pacientes duplicados removidos!\n')

# Same name, register, medical record, even if in different ICUs, is likely a mistake
df.drop_duplicates(subset=['Paciente', 'Hospital', 'Data/horário internamento', 'Registro', 'Prontuário', 'Data alta', 'Data nascimento'], keep='first', inplace=True)
# Group patients, hospital and record to group same treatment together, then order by admission date to grab parent row (transfer-wise) first
df.sort_values(by=['Paciente', 'Hospital', 'Registro', 'Data/horário internamento'], ascending=[True, True, True, True], ignore_index=True, inplace=True)

with open(outputText, "a") as f:
    f.write('Tratamento de caracteres, remoção de linhas duplicadas e ordenação concluídos\n')
    f.write('------x------x------x------x------\n')
    f.write('------x------x------x------x------\n')
    f.write('------x------x------x------x------\n')

with open(outputText, "a") as f:
    # Grab only the possible transfers
    rowsWithTransfers = df.loc[df['Destino alta'] == 'Outra UTI'].index.tolist()
    for row in rowsWithTransfers:
        transferPatient = handle.getPatientByRow(row, df)
        possibleTrasnferedRows = (
            df.loc[
                (
                    (df['Hospital'] == transferPatient.hospital) &
                    (df['Paciente'] == transferPatient.name) &
                    (df['Registro'] == transferPatient.register)
                )
            ].drop(row) # So it doesn't consider a row transfering to itself on a 1 day treatment
        )
        for index in possibleTrasnferedRows.index.tolist():
            patientTransferedTo = handle.getPatientByRow(index, df)
            # If is a transfer
            if transferPatient.dischargeDate == patientTransferedTo.admissionDate:
                cameFrom[str(patientTransferedTo.row)] = transferPatient.row
                parentRow = handle.getFinalParent(transferPatient.row, cameFrom)
                # Copy discharge data to parent
                f.write(
                    'Paciente ' + transferPatient.name + ' transferido de ' + transferPatient.uti + ' para ' +
                    patientTransferedTo.uti + ' no dia ' + transferPatient.dischargeDate.strftime('%d/%m/%Y') + '\n'
                )
                df.loc[parentRow, 'Tipo alta':'Resumo alta'] = df.loc[patientTransferedTo.row, 'Tipo alta':'Resumo alta']
                # df = sofa.appendSofa(patientTransferedTo.row, parentRow, df, outputText)
                break

with open(outputText, "a") as f:
    f.write('------x------x------x------x------\n')
    f.write('------x------x------x------x------\n')
    f.write('------x------x------x------x------\n')
    f.write('Cópia de dados de alta de transferências concluída\n')

# Deletes all row that came from another (aka was transfered from another row)
for index in cameFrom:
    df = df.drop(int(index))
with open(outputText, "a") as f:
    f.write('Exclusão de linhas de transferências concluída\n')

df.to_excel(outputSheet, sheet_name="Página 1", index=False)

with open(outputText, "a") as f:
    f.write('Exportação concluída sem erros\n')
