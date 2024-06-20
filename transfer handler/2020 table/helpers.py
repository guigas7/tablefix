from patient import Patient

def getPatientByRow(row, df):
    return Patient(
        df.loc[row, 'Hospital'], # Hospital
        df.loc[row, 'UTI'], # UTI
        df.loc[row, 'Paciente'], # Name
        df.loc[row, 'Data/horário internamento'], # Admission Date
        df.loc[row, 'Registro'], # Register
        df.loc[row, 'Prontuário'], # Medical Record
        df.loc[row, 'Data alta'], # Discharge Date
        row # Row
    )

def getFinalParent(row, cameFrom):
    if str(row) not in cameFrom:
        return row
    return getFinalParent(cameFrom[str(row)], cameFrom)
