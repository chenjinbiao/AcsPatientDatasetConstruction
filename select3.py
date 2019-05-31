import pandas as pd
import numpy as np
import xlwt
import re


data=pd.read_csv('e:/f/ppap3.csv', index_col=0)
num = 0
data['乙型肝炎病毒表面抗体（发光法）'][7870] = 1
data['乙型肝炎病毒表面抗体（发光法）'][11551] = 1
for i in range(len(data)):
    num = num + 1
    data['text'][i] = data['text'][i].replace('[ \n\t]', '/')
    data['text'][i] = data['text'][i].replace(',', ';')
    if num % 300 == 0:
        print(num, '/', len(data))
    if data['age'][i] == 'None':
        data = data.drop(labels= i)




data.to_csv('e:/ppap.csv', index=False,encoding='UTF-8')
data.to_excel('e:/ppap.xlsx', index=False,encoding='UTF-8')