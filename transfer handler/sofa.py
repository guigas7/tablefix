# Initialize sofa column names
sofa = []
sofaLimit = 31

for day in range(0, sofaLimit):
    start = 'Data - Registro SOFA ' + str(day)
    end = 'Creatinina - Registro SOFA ' + str(day)
    sofa.append({'start': start, 'end': end})


def appendSofa(transferRow, parentRow, df, outputText):
    df.loc[parentRow, sofa[1]['start']:sofa[sofaLimit - 1]['end']] = df.loc[transferRow, sofa[1]['start']:sofa[sofaLimit - 1]['end']].values
    return df
