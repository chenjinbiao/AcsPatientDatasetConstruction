import pandas as pd
import numpy as np
import xlwt
import re


def main():
    data = pd.read_csv('f:/selected.csv')
    pattern1 = re.compile(r'[0-9.]+')
    data = data.drop(['粪便性状','粪便颜色','粪便虫卵', '尿浊度','尿液颜色'],axis=1)
    data = data.drop('尿红细胞检查(镜检）', axis=1)
    data = data.drop(['尿白细胞检查(镜检）','尿上皮细胞检查(镜检）'], axis=1)
    num = 0
    for i in data.columns:
        if i == 'ABO血型鉴定'or i == 'patient_id'or i == 'visit_id'or i == 'text' or i == 'sex' or i == 'age':
            continue
        for j in range(len(data)):
            num = num +1
            if num%1000 == 0:
                print(num,'/1176145')

            if data[i][j] == 'None':
                data[i][j] = None
                continue
            try:
                data[i][j] = float(data[i][j])
            except:
                pass
            else:
                if data[i][j] < 0:
                    data[i][j] = None
                continue
            try:
                if '阴' in data[i][j] and '阳' in data[i][j]:
                    data[i][j] = None
                elif '阴' in data[i][j] or '正常' in data[i][j]:
                    data[i][j] = 0
                elif '弱阳' in data[i][j]:
                    data[i][j] = 0.5
                elif '阳' in data[i][j] or 'POS' in data[i][j] or '视野' in data[i][j] or 'msy' in data[i][j]:
                    data[i][j] = 1
                elif '---' in data[i][j] or '*' in data[i][j] or '标本量不足' in data[i][j] or '计价' in data[i][j]:
                    data[i][j] = None
                elif '>' in data[i][j] or '<' in data[i][j]:
                    r1 = pattern1.findall(data[i][j])
                    data[i][j] = float(r1[0])
                elif '/' in data[i][j]:
                    r1 = pattern1.findall(data[i][j])
                    data[i][j] = float(r1[0])/float(r1[-1])
                elif '-' in data[i][j]:
                    continue
                else:
                    try:
                        data[i][j] = float(data[i][j])
                    except:
                        r1 = pattern1.findall(data[i][j])
                        if r1 == []:
                            data[i][j] = None
                        else:
                            data[i][j] = float(r1[0])
                    else:
                        if data[i][j] < 0:
                            data[i][j] = None
            except:
                data[i][j] = None
            else:
                pass
    print(data)
    data.to_csv('f:/data1.csv')
    data = pd.read_csv('f:/data1.csv')
    num = 0
    for i in range(len(data)):
        num = num +1
        if num % 300 == 0:
            print(num,'/',len(data))
        if data['尿红细胞检查'][i] > 25:
            data['尿红细胞检查'][i] = 1
        else:
            data['尿红细胞检查'][i] = 0
        if data['sex'][i] == '男':
            data['sex'][i] = 1
        elif data['sex'][i] == '女':
            data['sex'][i] = 0
        else:
            data['sex'][i] = None

        if data['尿白细胞检查'][i] > 25:
            data['尿白细胞检查'][i] = 1
        else:
            data['尿白细胞检查'][i] = 0
        try:
            if '-'in data['粪便白细胞'][i]:

                r1 = pattern1.findall(data['粪便白细胞'][i])
                n = float(r1[-1])
                print(data['粪便白细胞'][i],n)
                if n <= 3:
                    data['粪便白细胞'][i] = 0
                elif n < 20:
                    data['粪便白细胞'][i] = 0.5
                else:
                    data['粪便白细胞'][i] = 1
        except:
            pass
        else:
            pass
        try:
            if '-'in data['粪便红细胞'][i]:
                r1 = pattern1.findall(data['粪便红细胞'][i])
                n = float(r1[-1])
                if n <= 3:
                    data['粪便红细胞'][i] = 0
                elif n < 20:
                    data['粪便红细胞'][i] = 0.5
                else:
                    data['粪便红细胞'][i] = 1
        except:
            pass
        else:
            pass
        try:
            if data['身高'][i] < 10:
                data['身高'][i] = 100 * data['身高'][i]
                print(data['身高'][i])
            elif data['身高'][i] < 100 and data['身高'][i] > 10:
                if data['身高'][i] < data['体重'][i] and data['体重'][i] > 100:
                    d = data['身高'][i]
                    data['身高'][i] = data['体重'][i]
                    data['体重'][i] = d
            elif data['身高'][i] == data['体重'][i]:
                if data['身高'][i] > 150:
                    data['体重'][i] = None
                else:
                    data['身高'][i] = None
        except:
            pass
        else:
            pass
    print(data)
    data.to_csv('f:/data2.csv',index=False)
    data['A型血'] = None
    data['B型血'] = None
    data['AB型血'] = None
    data['O型血'] = None
    num = 0
    for i in range(len(data)):
        num = num + 1
        if num % 300 == 0:
            print(num, '/', len(data))
        if data['ABO血型鉴定'][i] == 'None':
            continue
        elif 'AB' in data['ABO血型鉴定'][i]:
            data['A型血'][i] = 0
            data['B型血'][i]= 0
            data['AB型血'][i] = 1
            data['O型血'][i] = 0
        elif 'B' in data['ABO血型鉴定'][i]:
            data['A型血'][i] = 0
            data['B型血'][i] = 1
            data['AB型血'][i] = 0
            data['O型血'][i] = 0
        elif 'A' in data['ABO血型鉴定'][i]:
            data['A型血'][i] = 1
            data['B型血'][i] = 0
            data['AB型血'][i] = 0
            data['O型血'][i] = 0
        elif 'O' in data['ABO血型鉴定'][i]:
            data['A型血'][i] = 0
            data['B型血'][i]= 0
            data['AB型血'][i] = 0
            data['O型血'][i] = 1
    data = data.drop('ABO血型鉴定', axis=1)
    num = 0
    for i in range(len(data)):
        num = num + 1
        if num % 300 == 0:
            print(num, '/', len(data))
        data['text'][i] = data['text'][i].strip()

    data.to_csv('f:/data3.csv',index=False)


if __name__ == '__main__':
    main()