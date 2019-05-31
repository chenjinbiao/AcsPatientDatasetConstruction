"""
用python从orcale数据库中提取特征项并整合输出的
xml_test:用正则提取表达式提取xml中的特征项
ppt:test
select1:少于30%的数据丢弃
select2:数据值二值化处理（血型，性别等）
select3:数据处理
"""




import pandas as pd
import numpy as np
import xlwt
import time
import cx_Oracle as oracle
import sys

import os
import importlib
from xml.dom.minidom import parse
import xml.dom.minidom

def coding(patientId, visitId):
    theId = patientId.__str__() + "&" + visitId.__str__()
    return theId


def decoding(theId):
    patientId = ''
    visitId = ''
    flag = 0
    for i in theId:
        if i == '&':
            flag = 1
            continue
        if flag == 0:
            patientId = patientId + i
        else:
            visitId = visitId + i
    return patientId, visitId


def datetime2age(date):
    t = time.localtime(time.time())
    sum = 0
    year = ''
    month = ''
    day = ''
    for i in date:
        if i == '-':
            sum = sum + 1
            continue
        if i == ' ':
            break
        if sum == 0:
            year = year + i
        elif sum == 1:
            month = month + i
        elif sum == 2:
            day = day + i
    year = int(year)
    month = int(month)
    day = int(day)
    age = (t.tm_year - year) + (t.tm_mon - month) / 12 + (t.tm_mday - day) / 365
    age = int(age)
    return age.__str__()


def whole_set():
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
    con = oracle.connect('DATA_SOURCE/DATA_SOURCE@172.16.200.24:1521/PLA_ACS')
    mycursor = con.cursor()
    print('connected')
    # mycursor.execute("DROP TABLE ID_SELECTED")
    drop = "DROP TABLE ID_SELECTED "
    create_table = """
        create table ID_SELECTED(
          PATIENT_ID VARCHAR2(10 char),
          VISIT_ID VARCHAR2(2 char)
        )"""
    # mycursor.execute(create_table)
    table = """
        select distinct VISIT.PATIENT_ID,VISIT.VISIT_ID 
        from VISIT ,VITAL_SIGNS,LABTEST_MASTER,LABTEST_RESULT,DIAGNOSIS d 
        where VISIT.PATIENT_ID =VITAL_SIGNS.PATIENT_ID 
        AND VITAL_SIGNS.VISIT_ID =  VISIT.VISIT_ID and LABTEST_MASTER.TEST_NO = LABTEST_RESULT.TEST_NO 
        and LABTEST_MASTER.PATIENT_ID = VISIT.PATIENT_ID and LABTEST_MASTER.VISIT_ID = VISIT.VISIT_ID
        and d.VISIT_ID=VISIT.VISIT_ID and d.PATIENT_ID = VISIT.PATIENT_ID and DIAGNOSIS_TYPE_NAME like :1 AND (DIAGNOSIS_DESC LIKE :2 OR DIAGNOSIS_DESC LIKE :3 OR DIAGNOSIS_DESC LIKE :4 OR DIAGNOSIS_DESC LIKE :5 )
        and (regexp_like(d.DIAGNOSIS_DESC, '不稳.{0,3}心绞痛', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '梗.?后心绞痛', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '变异|恶化|初发', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '急性冠脉综合.[^？]', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '急性冠脉综合.$', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '急性[^冠].{0,12}心.?梗', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '急性心.?梗|MI', 'i'))ORDER BY VISIT.PATIENT_ID,VISIT.VISIT_ID
        """
    # mycursor.execute(table, ('%出院%', '%心绞痛%', '%急性冠脉%', '%心%梗%', '%MI%'))
    # # mycursor.execute(T)
    # myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    # #
    #
    # id = []
    # for x in myresult:
    #     print(x)
    #     id.append([x[0], x[1]])
    #
    # # mycursor.executemany('insert into ID_SELECTED values(:1,:2)', id)
    # # con.commit()
    # database = pd.DataFrame(id)
    # database.columns = ['patient_id', 'visit_id']
    # database.to_csv('f:/r1.csv', index=False, encoding='UTF-8')

    # vital_signs_sql = """
    # select distinct PATIENT_ID,VISIT_ID,RECORDING_DATE,VITAL_SIGNS,VITAL_SIGNS_VALUES,UNITS from VITAL_SIGNS
    # where (VITAL_SIGNS.PATIENT_ID,VITAL_SIGNS.VISIT_ID) in (select  PATIENT_ID,VISIT_ID from ID_SELECTED)
    # ORDER BY PATIENT_ID,VISIT_ID,RECORDING_DATE
    # """
    # vital_signs_item_sql = """
    # select distinct VITAL_SIGNS from VITAL_SIGNS
    # where (PATIENT_ID,VISIT_ID) in (select  PATIENT_ID,VISIT_ID from ID_SELECTED)
    # """
    # database = pd.read_csv("f:/r1.csv")
    # mycursor.execute(vital_signs_item_sql)
    # myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    # for i in myresult:
    #     print(i)
    #     database[i[0]] = 'None'
    # database.to_csv('f:/r2.csv', index=False, encoding='UTF-8')
    # print(database.values[2][0:2])
    # mycursor.execute(vital_signs_sql)
    # vital = mycursor.fetchall()  # fetchall() 获取所有记录
    # database = database.set_index(['patient_id', 'visit_id'])
    # num = 0
    # num1 = 0
    # num2 = 0
    # num3 = 0
    # print('load vital signs')
    #
    # for i in vital:
    #     try:
    #         if database.loc[str(i[0]), int(i[1])][i[3]] == 'None':
    #             database.loc[str(i[0]), int(i[1])][i[3]] = str(i[4])
    #             num1 = num1 + 1
    #             if num1 % 1000 == 0:
    #                 print(num1)
    #         else:
    #             num2 = num2 + 1
    #     except:
    #         num3 = num3 + 1
    #
    #     else:
    #         num = num + 1
    # print('num:', num, 'num1:', num1, 'num2:', num2, 'num3:', num3)
    # # num: 2302076 num1: 147356 num2: 2154720 num3: 0
    #
    # database.to_csv('f:/r3.csv', encoding='UTF-8')
    #
    # labtest_sql = """
    #     select distinct PATIENT_ID,VISIT_ID,REQUESTED_DATE_TIME,REPORT_ITEM_NAME,RESULT,UNITS
    #     from LABTEST_MASTER L1,LABTEST_RESULT L2  where L1.TEST_NO=L2.TEST_NO and (PATIENT_ID,VISIT_ID)
    #     in (select  PATIENT_ID,VISIT_ID from ID_SELECTED)
    #     ORDER BY PATIENT_ID,VISIT_ID,REQUESTED_DATE_TIME
    #     """
    # lab_item_sql = """select distinct REPORT_ITEM_NAME from LABTEST_MASTER L1,LABTEST_RESULT L2
    #  where L1.TEST_NO=L2.TEST_NO and (PATIENT_ID,VISIT_ID)
    #  in (select  PATIENT_ID,VISIT_ID from ID_SELECTED) order by REPORT_ITEM_NAME
    #  """
    #
    # mycursor.execute(lab_item_sql)
    # myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    # for i in myresult:
    #     print(i)
    #     database[i[0]] = 'None'
    # database.to_csv('f:/r4.csv', encoding='UTF-8')
    #
    # mycursor.execute(labtest_sql)
    # lab = mycursor.fetchall()  # fetchall() 获取所有记录
    #
    # num = 0
    # num1 = 0
    # num2 = 0
    # num3 = 0
    # print('load labtest')
    #
    # for i in lab:
    #
    #     try:
    #         if database.loc[str(i[0]), int(i[1])][i[3]] == 'None':
    #             database.loc[str(i[0]), int(i[1])][i[3]] = str(i[4])
    #
    #             num1 = num1 + 1
    #             if num1 % 1000 == 0:
    #                 print(num1)
    #         else:
    #             num2 = num2 + 1
    #     except:
    #         num3 = num3 + 1
    #
    #     else:
    #         num = num + 1
    # print('num:', num, 'num1:', num1, 'num2:', num2, 'num3:', num3)
    # # num: 2213888 num1: 1448711 num2: 765177 num3: 0
    #
    # database.to_csv('f:/r5.csv', encoding='UTF-8')

    dia_sql = """
        select distinct PATIENT_ID,VISIT_ID,DIAGNOSIS_DESC from DIAGNOSIS d 
        where DIAGNOSIS_TYPE_NAME like :1 
        AND (DIAGNOSIS_DESC LIKE :2 OR DIAGNOSIS_DESC LIKE :3 OR DIAGNOSIS_DESC LIKE :4 OR DIAGNOSIS_DESC LIKE :5)
     and (regexp_like(d.DIAGNOSIS_DESC, '不稳.{0,3}心绞痛', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '梗.?后心绞痛', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '变异|恶化|初发', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '急性冠脉综合.[^？]', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '急性冠脉综合.$', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '急性[^冠].{0,12}心.?梗', 'i')
        OR regexp_like(d.DIAGNOSIS_DESC, '急性心.?梗|MI', 'i')) 
        and (PATIENT_ID,VISIT_ID) in (select PATIENT_ID,VISIT_ID from ID_SELECTED)
        """

    database = pd.read_csv("f:/r5.csv")
    database.nrowsow
    # database['text'] = 'None'
    mycursor.execute(dia_sql, ('%出院%', '%心绞痛%', '%急性冠脉%', '%心%梗%', '%MI%'))
    dia = mycursor.fetchall()

    # print(database.loc['A180000', 1]['尿白细胞检查(镜检）'])
    print('load diagnosis')

    num1 = 0
    num2 = 0
    text = []
    for i in dia:
        try:
            text.append([str(i[0]), int(i[1]), i[2]])

            # database.loc[str(i[0]), int(i[1])]['text'] = 'i[2]'
            # print(database.loc[str(i[0]), int(i[1])]['text'])
            # print(i[0],i[1],i[2])
            num1 = num1 + 1
            if num1 % 1000 == 0:
                print(num1)


        except:

            num2 = num2 + 1

        else:
            continue
    print(num1, num2)
    # 11450 0
    text = pd.DataFrame(text)
    text.columns = ['patient_id', 'visit_id', 'text']
    database = pd.merge(text, database, on=['patient_id', 'visit_id'])
    database.to_csv('f:/r6.csv', encoding='UTF-8')

    database = database.set_index(['patient_id', 'visit_id'])

    database = database.reset_index(['patient_id', 'visit_id'])
    database = database.set_index(['patient_id'])
    database['sex'] = 'None'
    database['age'] = 'None'
    sex_sql = """
        select distinct PATIENT_ID,SEX,DATE_OF_BIRTH from PATIENT  where  (PATIENT_ID) in (select  PATIENT_ID from ID_SELECTED)
        """
    mycursor.execute(sex_sql)
    s_a = mycursor.fetchall()
    print('load sex and age')
    num1 = 0
    num2 = 0
    for i in s_a:
        try:
            database.loc[i[0], 'sex'] = i[1]
            database.loc[i[0], 'age'] = datetime2age(str(i[2]))
            num1 = num1 + 1
            if num1 % 1000 == 0:
                print(num1)

        except:

            num2 = num2 + 1

        else:
            continue
    print(num1, num2)
    # 11450 0
    database.to_csv('f:/r7.csv', encoding='UTF-8')
    database = database.reset_index(['patient_id'])
    DOMTree = xml.dom.minidom.parse(r"C:/Users/Chen.Jinbiao/Desktop/xml_recheck1.xml")
    collection = DOMTree.documentElement

    MemoContents = collection.getElementsByTagName("Record")
    a = []
    print('start')
    for MemoContent in MemoContents:
        if MemoContent.hasAttribute("patientId") and MemoContent.hasAttribute("visitId"):
            a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
            # print("patientId: %s " % MemoContent.getAttribute("patientId"))

    a = pd.DataFrame(a)
    a.columns = ['patient_id', 'visit_id']
    print(a)
    # a.to_csv('e:/a', header=False, index=False, encoding='UTF-8')

    r = pd.merge(a, database, on=['patient_id', 'visit_id'])
    print(r)

    r.to_csv('f:/output1.csv', index=False, encoding='UTF-8')
    # vital = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/vital_signs.csv', header=None)
    # lab = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/labtest.csv', header=None)
    # dia = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/diagnosis.csv', header=None)
    # age = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/age.csv', header=None)
    # vitalitem = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/vitalitem.csv', header=None)
    # labitem = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/labitem.csv', header=None)
    # id = pd.read_csv("C:/Users/Chen.Jinbiao/Desktop/id.csv", header=None)
    # # database= pd.read_csv("e:/result4.csv", index_col=0)
    #
    #
    # for i in labitem.values[:, 0]:
    #     database[i] = None
    #
    # for i in vitalitem.values[:, 0]:
    #     database[i] = None
    #
    # database = database.set_index(['patient_id'])
    # print('database built')
    #
    # print('load age and sex')
    # database['age'] = None
    # database['sex'] = None
    #
    # num1 = 0
    # num2 = 0
    #
    # for i in age.values:
    #
    #     try:
    #         database.loc[i[0], 'sex'] = i[1]
    #         database.loc[i[0], 'age'] = datetime2age(i[2])
    #         num1 = num1 + 1
    #         if num1 % 1000 == 0:
    #             print(num1)
    #
    #     except:
    #         print(i[1], datetime2age(i[2]))
    #         num2 = num2 + 1
    #
    #     else:
    #         continue
    # print(num1, num2)
    #
    # print('load diagnosis')
    # database = database.reset_index(['patient_id'])
    # database = database.set_index(['patient_id', 'visit_id'])
    # database['text'] = None
    # num1 = 0
    # num2 = 0
    # for i in dia.values:
    #
    #     try:
    #         database.loc[i[0], i[1]]['text'] = i[2]
    #
    #         num1 = num1 + 1
    #         if num1 % 1000 == 0:
    #             print(num1)
    #
    #     except:
    #
    #         num2 = num2 + 1
    #
    #     else:
    #         continue
    #
    # print(num1, num2)
    #
    # database.to_csv('f:/result.csv', encoding='UTF-8')
    # num = 0
    # num1 = 0
    # num2 = 0
    # num3 = 0
    # print('load labtest')
    #
    # for i in lab.values:
    #
    #     try:
    #         if database.loc[str(i[0]), i[1]][i[3]] == None:
    #             database.loc[str(i[0]), i[1]][i[3]] = i[4]
    #             num1 = num1 + 1
    #             if num1 % 1000 == 0:
    #                 print(num1)
    #         else:
    #             num2 = num2 + 1
    #     except:
    #         num3 = num3 + 1
    #         print(i)
    #     else:
    #         num = num + 1
    #
    # print('num:', num, 'num1:', num1, 'num2:', num2, 'num3:', num3)
    # # num: 2213888 num1: 1448711 num2: 765177 num3: 0
    #
    # num = 0
    # num1 = 0
    # num2 = 0
    # num3 = 0
    # print('load vital signs')
    #
    # for i in vital.values:
    #
    #     try:
    #         if database.loc[str(i[0]), i[1]][i[3]] == None:
    #             database.loc[str(i[0]), i[1]][i[3]] = i[4]
    #             num1 = num1 + 1
    #             if num1 % 1000 == 0:
    #                 print(num1)
    #         else:
    #             num2 = num2 + 1
    #     except:
    #         num3 = num3 + 1
    #
    #     else:
    #         num = num + 1
    # print('num:', num, 'num1:', num1, 'num2:', num2, 'num3:', num3)
    # # num: 2302076 num1: 147356 num2: 2154720 num3: 0
    #
    # database.to_csv('f:/result4.csv', encoding='UTF-8')
    # 12512 rows x 849 columns


def operate_oracle():

    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
    con = oracle.connect('DATA_SOURCE/DATA_SOURCE@172.16.200.24:1521/PLA_ACS')
    mycursor = con.cursor()
    print('connected')
    # mycursor.execute("DROP TABLE ID_SELECTED")

    # mycursor.execute(create_table)
    table = """
        select distinct ID.PATIENT_ID,ID.VISIT_ID,DIAGNOSIS_DESC
        from ID,DIAGNOSIS d
        where  d.VISIT_ID=ID.VISIT_ID and d.PATIENT_ID = ID.PATIENT_ID
        and (regexp_like(d.DIAGNOSIS_DESC, '((外周)|(颈)|(肾)|(下肢)).{0,3}?动脉.{0,5}?((硬化)|(狭窄)|(闭塞))', 'i')
      )ORDER BY ID.PATIENT_ID,ID.VISIT_ID
        """
    mycursor.execute(table)
    # mycursor.execute(T)
    myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    #
    num = 0
    history = []
    a0 = 0
    a1 = 0
    for x in myresult:
        print(x)
        if a0 == x[0] and a1 == x[1]:
            pass
        else:
            history.append([x[0], int(x[1]), 1, x[2]])
            num = num + 1

        a0 = x[0]
        a1 = x[1]


    # mycursor.executemany('insert into ID_SELECTED values(:1,:2)', id)
    # con.commit()
    print(num)
    history = pd.DataFrame(history)
    history.columns = ['patient_id', 'visit_id','既往血管系统疾病史 ','text']


    database = pd.read_excel("e:/id.xlsx")
    r = pd.merge(history, database, how='right', on=['patient_id', 'visit_id'])
    print(r)
    r.to_excel('E:/history2.xlsx', index=False, encoding='UTF-8')


def main():
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
    con = oracle.connect('DATA_SOURCE/DATA_SOURCE@172.16.200.24:1521/PLA_ACS')
    mycursor = con.cursor()
    print('connected')
    #mycursor.execute("DROP TABLE ID_SELECTED")
    drop = "DROP TABLE ID_SELECTED "
    create_table = """
    create table ID_SELECTED(
      PATIENT_ID VARCHAR2(10 char),
      VISIT_ID VARCHAR2(2 char)
    )"""
    # mycursor.execute(create_table)
    table = """
    select distinct VISIT.PATIENT_ID,VISIT.VISIT_ID 
    from VISIT ,VITAL_SIGNS,LABTEST_MASTER,LABTEST_RESULT,DIAGNOSIS d 
    where VISIT.PATIENT_ID =VITAL_SIGNS.PATIENT_ID 
    AND VITAL_SIGNS.VISIT_ID =  VISIT.VISIT_ID and LABTEST_MASTER.TEST_NO = LABTEST_RESULT.TEST_NO 
    and LABTEST_MASTER.PATIENT_ID = VISIT.PATIENT_ID and LABTEST_MASTER.VISIT_ID = VISIT.VISIT_ID
    and d.VISIT_ID=VISIT.VISIT_ID and d.PATIENT_ID = VISIT.PATIENT_ID and DIAGNOSIS_TYPE_NAME like :1 AND (DIAGNOSIS_DESC LIKE :2 OR DIAGNOSIS_DESC LIKE :3 OR DIAGNOSIS_DESC LIKE :4 OR DIAGNOSIS_DESC LIKE :5 )
    and (regexp_like(d.DIAGNOSIS_DESC, '不稳.{0,3}心绞痛', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '梗.?后心绞痛', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '变异|恶化|初发', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '急性冠脉综合.[^？]', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '急性冠脉综合.$', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '急性[^冠].{0,12}心.?梗', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '急性心.?梗|MI', 'i'))ORDER BY VISIT.PATIENT_ID,VISIT.VISIT_ID
    """
    mycursor.execute(table, ('%出院%', '%心绞痛%', '%急性冠脉%', '%心%梗%', '%MI%'))
    # mycursor.execute(T)
    myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    #

    id = []
    for x in myresult:
        print(x)
        id.append([x[0], x[1]])

    # mycursor.executemany('insert into ID_SELECTED values(:1,:2)', id)
    # con.commit()
    database = pd.DataFrame(id)
    database.columns = ['patient_id', 'visit_id']
    database.to_csv('f:/r1.csv', index=False, encoding='UTF-8')

    vital_signs_sql = """
    select distinct PATIENT_ID,VISIT_ID,RECORDING_DATE,VITAL_SIGNS,VITAL_SIGNS_VALUES,UNITS from VITAL_SIGNS
    where (VITAL_SIGNS.PATIENT_ID,VITAL_SIGNS.VISIT_ID) in (select  PATIENT_ID,VISIT_ID from ID_SELECTED)
    ORDER BY PATIENT_ID,VISIT_ID,RECORDING_DATE
    """
    vital_signs_item_sql = """
    select distinct VITAL_SIGNS from VITAL_SIGNS
    where (PATIENT_ID,VISIT_ID) in (select  PATIENT_ID,VISIT_ID from ID_SELECTED)
    """
    database = pd.read_csv("f:/r1.csv")
    mycursor.execute(vital_signs_item_sql)
    myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    for i in myresult:
        print(i)
        database[i[0]] = 'None'
    database.to_csv('f:/r2.csv', index=False, encoding='UTF-8')
    print(database.values[2][0:2])
    mycursor.execute(vital_signs_sql)
    vital = mycursor.fetchall()  # fetchall() 获取所有记录
    database = database.set_index(['patient_id', 'visit_id'])
    num = 0
    num1 = 0
    num2 = 0
    num3 = 0
    print('load vital signs')

    for i in vital:
        try:
            if database.loc[str(i[0]), int(i[1])][i[3]] == 'None':
                database.loc[str(i[0]), int(i[1])][i[3]] = str(i[4])
                num1 = num1 + 1
                if num1 % 1000 == 0:
                    print(num1)
            else:
                num2 = num2 + 1
        except:
            num3 = num3 + 1

        else:
            num = num + 1
    print('num:', num, 'num1:', num1, 'num2:', num2, 'num3:', num3)
    # num: 2302076 num1: 147356 num2: 2154720 num3: 0

    database.to_csv('f:/r3.csv', encoding='UTF-8')

    labtest_sql = """
        select distinct PATIENT_ID,VISIT_ID,REQUESTED_DATE_TIME,REPORT_ITEM_NAME,RESULT,UNITS
        from LABTEST_MASTER L1,LABTEST_RESULT L2  where L1.TEST_NO=L2.TEST_NO and (PATIENT_ID,VISIT_ID)
        in (select  PATIENT_ID,VISIT_ID from ID_SELECTED)
        ORDER BY PATIENT_ID,VISIT_ID,REQUESTED_DATE_TIME
        """
    lab_item_sql = """select distinct REPORT_ITEM_NAME from LABTEST_MASTER L1,LABTEST_RESULT L2
     where L1.TEST_NO=L2.TEST_NO and (PATIENT_ID,VISIT_ID)
     in (select  PATIENT_ID,VISIT_ID from ID_SELECTED) order by REPORT_ITEM_NAME
     """

    mycursor.execute(lab_item_sql)
    myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    for i in myresult:
        print(i)
        database[i[0]] = 'None'
    database.to_csv('f:/r4.csv', encoding='UTF-8')

    mycursor.execute(labtest_sql)
    lab = mycursor.fetchall()  # fetchall() 获取所有记录

    num = 0
    num1 = 0
    num2 = 0
    num3 = 0
    print('load labtest')

    for i in lab:

        try:
            if database.loc[str(i[0]), int(i[1])][i[3]] == 'None':
                database.loc[str(i[0]), int(i[1])][i[3]] = str(i[4])

                num1 = num1 + 1
                if num1 % 1000 == 0:
                    print(num1)
            else:
                num2 = num2 + 1
        except:
            num3 = num3 + 1

        else:
            num = num + 1
    print('num:', num, 'num1:', num1, 'num2:', num2, 'num3:', num3)
    # num: 2213888 num1: 1448711 num2: 765177 num3: 0

    database.to_csv('f:/r5.csv', encoding='UTF-8')

    dia_sql = """
    select distinct PATIENT_ID,VISIT_ID,DIAGNOSIS_DESC from DIAGNOSIS d 
    where DIAGNOSIS_TYPE_NAME like :1 
    AND (DIAGNOSIS_DESC LIKE :2 OR DIAGNOSIS_DESC LIKE :3 OR DIAGNOSIS_DESC LIKE :4 OR DIAGNOSIS_DESC LIKE :5)
 and (regexp_like(d.DIAGNOSIS_DESC, '不稳.{0,3}心绞痛', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '梗.?后心绞痛', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '变异|恶化|初发', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '急性冠脉综合.[^？]', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '急性冠脉综合.$', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '急性[^冠].{0,12}心.?梗', 'i')
    OR regexp_like(d.DIAGNOSIS_DESC, '急性心.?梗|MI', 'i')) 
    and (PATIENT_ID,VISIT_ID) in (select PATIENT_ID,VISIT_ID from ID_SELECTED)
    """

    database = pd.read_csv("f:/r5.csv")
    database.nrowsow
    #database['text'] = 'None'
    mycursor.execute(dia_sql, ('%出院%', '%心绞痛%', '%急性冠脉%', '%心%梗%', '%MI%'))
    dia = mycursor.fetchall()


    # print(database.loc['A180000', 1]['尿白细胞检查(镜检）'])
    print('load diagnosis')

    num1 = 0
    num2 = 0
    text=[]
    for i in dia:
        try:
            text.append([str(i[0]),int(i[1]),i[2]])

            # database.loc[str(i[0]), int(i[1])]['text'] = 'i[2]'
            # print(database.loc[str(i[0]), int(i[1])]['text'])
            # print(i[0],i[1],i[2])
            num1 = num1 + 1
            if num1 % 1000 == 0:
                print(num1)


        except:

            num2 = num2 + 1

        else:
            continue
    print(num1, num2)
    # 11450 0
    text = pd.DataFrame(text)
    text.columns = ['patient_id', 'visit_id','text']
    database = pd.merge(text, database, on=['patient_id', 'visit_id'])
    database.to_csv('f:/r6.csv', encoding='UTF-8')

    database = database.set_index(['patient_id', 'visit_id'])

    database = database.reset_index(['patient_id', 'visit_id'])
    database = database.set_index(['patient_id'])

    database['sex'] = 'None'
    database['age'] = 'None'
    sex_sql="""
    select distinct PATIENT_ID,SEX,DATE_OF_BIRTH from PATIENT  where  (PATIENT_ID) in (select  PATIENT_ID from ID_SELECTED)
    """
    mycursor.execute(sex_sql)
    s_a = mycursor.fetchall()
    print('load sex and age')
    num1 = 0
    num2 = 0
    for i in s_a:
        try:
            database.loc[i[0], 'sex'] = i[1]
            database.loc[i[0], 'age'] = datetime2age(str(i[2]))
            num1 = num1 + 1
            if num1 % 1000 == 0:
                print(num1)

        except:

            num2 = num2 + 1

        else:
            continue
    print(num1, num2)
    #11450 0
    database.to_csv('f:/r7.csv', encoding='UTF-8')
    database = database.reset_index(['patient_id'])
    DOMTree = xml.dom.minidom.parse(r"C:/Users/Chen.Jinbiao/Desktop/xml_recheck1.xml")
    collection = DOMTree.documentElement

    MemoContents = collection.getElementsByTagName("Record")
    a = []
    print('start')
    for MemoContent in MemoContents:
        if MemoContent.hasAttribute("patientId") and MemoContent.hasAttribute("visitId"):
            a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
            #print("patientId: %s " % MemoContent.getAttribute("patientId"))

    a = pd.DataFrame(a)
    a.columns = ['patient_id', 'visit_id']
    print(a)
    # a.to_csv('e:/a', header=False, index=False, encoding='UTF-8')



    r = pd.merge(a, database, on=['patient_id', 'visit_id'])
    print(r)

    r.to_csv('f:/output1.csv', index=False, encoding='UTF-8')
    # vital = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/vital_signs.csv', header=None)
    # lab = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/labtest.csv', header=None)
    # dia = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/diagnosis.csv', header=None)
    # age = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/age.csv', header=None)
    # vitalitem = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/vitalitem.csv', header=None)
    # labitem = pd.read_csv('C:/Users/Chen.Jinbiao/Desktop/labitem.csv', header=None)
    # id = pd.read_csv("C:/Users/Chen.Jinbiao/Desktop/id.csv", header=None)
    # # database= pd.read_csv("e:/result4.csv", index_col=0)
    #
    #
    # for i in labitem.values[:, 0]:
    #     database[i] = None
    #
    # for i in vitalitem.values[:, 0]:
    #     database[i] = None
    #
    # database = database.set_index(['patient_id'])
    # print('database built')
    #
    # print('load age and sex')
    # database['age'] = None
    # database['sex'] = None
    #
    # num1 = 0
    # num2 = 0
    #
    # for i in age.values:
    #
    #     try:
    #         database.loc[i[0], 'sex'] = i[1]
    #         database.loc[i[0], 'age'] = datetime2age(i[2])
    #         num1 = num1 + 1
    #         if num1 % 1000 == 0:
    #             print(num1)
    #
    #     except:
    #         print(i[1], datetime2age(i[2]))
    #         num2 = num2 + 1
    #
    #     else:
    #         continue
    # print(num1, num2)
    #
    # print('load diagnosis')
    # database = database.reset_index(['patient_id'])
    # database = database.set_index(['patient_id', 'visit_id'])
    # database['text'] = None
    # num1 = 0
    # num2 = 0
    # for i in dia.values:
    #
    #     try:
    #         database.loc[i[0], i[1]]['text'] = i[2]
    #
    #         num1 = num1 + 1
    #         if num1 % 1000 == 0:
    #             print(num1)
    #
    #     except:
    #
    #         num2 = num2 + 1
    #
    #     else:
    #         continue
    #
    # print(num1, num2)
    #
    # database.to_csv('f:/result.csv', encoding='UTF-8')
    # num = 0
    # num1 = 0
    # num2 = 0
    # num3 = 0
    # print('load labtest')
    #
    # for i in lab.values:
    #
    #     try:
    #         if database.loc[str(i[0]), i[1]][i[3]] == None:
    #             database.loc[str(i[0]), i[1]][i[3]] = i[4]
    #             num1 = num1 + 1
    #             if num1 % 1000 == 0:
    #                 print(num1)
    #         else:
    #             num2 = num2 + 1
    #     except:
    #         num3 = num3 + 1
    #         print(i)
    #     else:
    #         num = num + 1
    #
    # print('num:', num, 'num1:', num1, 'num2:', num2, 'num3:', num3)
    # # num: 2213888 num1: 1448711 num2: 765177 num3: 0
    #
    # num = 0
    # num1 = 0
    # num2 = 0
    # num3 = 0
    # print('load vital signs')
    #
    # for i in vital.values:
    #
    #     try:
    #         if database.loc[str(i[0]), i[1]][i[3]] == None:
    #             database.loc[str(i[0]), i[1]][i[3]] = i[4]
    #             num1 = num1 + 1
    #             if num1 % 1000 == 0:
    #                 print(num1)
    #         else:
    #             num2 = num2 + 1
    #     except:
    #         num3 = num3 + 1
    #
    #     else:
    #         num = num + 1
    # print('num:', num, 'num1:', num1, 'num2:', num2, 'num3:', num3)
    # # num: 2302076 num1: 147356 num2: 2154720 num3: 0
    #
    # database.to_csv('f:/result4.csv', encoding='UTF-8')
    # 12512 rows x 849 columns


# database = pd.read_csv("f:/result4.csv")
#     r, c = database.shape
#     database = database.fillna('None')
#     dict = []
#     num=0
#
#     print('start')
#     for i in database.columns:
#         sum = 0
#
#         for j in range(r):
#             if database.loc[j,i] == 'None':
#                 sum = sum + 1
#                 num=num+1
#                 if num%1000 == 0:
#                     print(num)
#
#         dict.append([i, sum])
#     print(dict)
#     r = pd.DataFrame(dict)
#     database.to_csv('f:/result2.csv', encoding='UTF-8')
#     r.to_csv('f:/r.csv', header=False, index=False, encoding='UTF-8')
if __name__ == '__main__':
    operate_oracle()