import pandas as pd
import numpy as np
import xlwt

def coding(patientId, visitId):
    theId = patientId.__str__() + "&" + visitId.__str__()
    return theId

def decoding(theId):
    patientId =''
    visitId =''
    flag = 0
    for i in theId:
        if i=='&':
            flag=1
            continue
        if flag == 0:
            patientId = patientId+i
        else:
            visitId = visitId + i
    return patientId,visitId

def main():
    data = pd.read_csv('f:/r7.csv')
    print(len(data))
    c = len(data)

    for i in data.columns:
        num = 0
        for j in range(len(data)):
            if data[i][j] == 'None':
                num = num + 1

        if num > c *0.3:
            data = data.drop(i,axis=1)

    print(data)
    data = data.set_index(['patient_id', 'visit_id'])
    r = len(data.values[0])
    for i in data.index:
        num = 0

        for j in range(r):
            if data.loc[i][j] == 'None':
                num = num + 1

        if num > r *0.3:
            data = data.drop(i)
    print(data)
    data.to_csv('f:/selected.csv')



if __name__ == '__main__':
    main()