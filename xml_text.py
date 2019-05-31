from xml.dom.minidom import parse
import xml.dom.minidom
import re
import numpy
import pickle
import time
import pandas as pd
import numpy as np
import xlwt
import os
import cx_Oracle as oracle
import sys
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


def killip_predict(str):
    a = 0
    if bool(re.search(r'(killip.{0,4}?(4|IV|Ⅳ)级)|((心功能|心肌梗死).{0,3}?(4|IV|Ⅳ)级.{0,2}killip)',str,re.IGNORECASE)):
        a = 4
    elif bool(re.search(r'(killip.{0,4}?(3|III|Ⅲ|３)级)|((心功能|心肌梗死).{0,3}?(3|III|Ⅲ|３)级.{0,2}killip)',str,re.IGNORECASE)):
        a = 3
    elif bool(re.search(r'(killip.{0,4}?(2|II|Ⅱ)级)|((心功能|心肌梗死).{0,3}?(2|II|Ⅱ)级.{0,2}killip)',str,re.IGNORECASE)):
        a = 2
    elif bool(re.search(r'(killip.{0,4}?(1|I|Ｉ|Ⅰ|l)级)|((心功能|心肌梗死).{0,3}?(1|I|Ｉ|Ⅰ|l)级.{0,2}killip)', str, re.IGNORECASE)):
        a = 1
    elif bool(re.search(r'(killip.{0,4}?(4|IV|Ⅳ))|((心功能|心肌梗死).{0,3}?(4|IV|Ⅳ).{0,3}killip)',str,re.IGNORECASE)):
        a = 4
    elif bool(re.search(r'(killip.{0,4}?(3|III|Ⅲ|３))|((心功能|心肌梗死).{0,3}?(3|III|Ⅲ|３).{0,3}killip)',str,re.IGNORECASE)):
        a = 3
    elif bool(re.search(r'(killip.{0,4}?(2|II|Ⅱ))|((心功能|心肌梗死).{0,3}?(2|II|Ⅱ).{0,3}killip)',str,re.IGNORECASE)):
        a = 2
    elif bool(re.search(r'(killip.{0,4}?(1|I|Ｉ|Ⅰ|l))|((心功能|心肌梗死).{0,3}?(1|I|Ｉ|Ⅰ|l).{0,3}killip)', str, re.IGNORECASE)):
        a = 1
    else:
        a = 0
    if a == 0:
        if bool(re.search(r'(([未为].{0,1}[及闻见])|(无).{0,2}干.??湿.{0,1}[罗啰]音)|(无[罗啰]音)|(([未为].{0,1}[见及闻])'
                          r'|(双肺罗音基本消失)|(无).{0,2}[湿显室].{0,1}[罗啰]音)|(呼吸音清)',str,re.IGNORECASE)):
            a = 1
        elif bool(re.search(r'((少[量许])|(微)|(细)|(小)|(轻)|(稀).{0,1}?[湿室干].{0,1}[罗啰]音)|(散在.{0,4}[湿室].??[罗|啰]音)'
                            r'|([及有].??[湿干室].{0,2}[罗啰]音)|((少[量许])|(微)|(细)|(小).{0,4}?[罗啰]音)'
                            r'|([及有].??[罗啰]音)'
                            r'|([罗啰]音较前.{0,2}减[轻少弱])|(散在双相干啰音)',str,re.IGNORECASE)):
            a = 2
        elif bool(re.search(r'((较多)|(明显)|(中等)|(响亮).{0,1}[湿室].{0,1}[罗啰]音)|(中量.{0,1}[湿室].{0,1}[罗啰]音)|([湿室].{0,1}[罗啰]音明显)|(明显双相干啰音)|(及中等量粗湿罗音)',
                            str,re.IGNORECASE)):
            a = 3
        elif bool(re.search(r'([满遍布].{0,2}[湿室干].{0,1}[罗啰]音)|((大量)|(广泛)|(弥漫).{0,1}[湿室干].{0,1}[罗啰]音)', str, re.IGNORECASE)):
            a = 4
        elif bool(re.search(r'([满遍布].{0,3}？[罗啰]音)|((大量)|(广泛)|(弥漫).{0,1}[罗啰]音)', str, re.IGNORECASE)):
            a = 4
        elif bool(re.search(r'(散在.{0,5}?[罗|啰]音)'
                            r'|([及有闻见].{0,5}?[湿干室].{0,3}[罗啰]音)|([少些许微细小局限].{0,4}?[罗啰]音)'
                            r'|([及有底].{0,3}?velco[罗啰]音)|([及有闻见].{0,8}?[罗啰]音)'
                            r'|([罗啰]音较前.{0,2}(减[轻少弱])|(改善))|(肺.?湿.??[罗啰]音)|(散在双相干啰音)|(肺.{0,3}[罗啰]音)|([罗啰]音.{0,3}?[减少])',
                            str, re.IGNORECASE)):
            a = 2
        else:
            a = 0
    return a


def cardiac_arrest_predict(str):
    a = -1
    if bool(re.search(r'([无不未].*?((意识.?丧失)|(室.??颤)|(心[跳脏].{0,3}骤停)))',str,re.IGNORECASE)):
        a = 0
    elif bool(re.search(r'((意识.?丧失)|(室.??颤)|(心[跳脏].{0,3}骤停)).{0,6}?((可能)|(趋势|(风险)|(病史)|(危险)))'
                        r'|(((病史)|(可能)|(许)).*?((心源性昏)|(心源性休克)|(意识.?丧失)|(室.??颤)|(心[跳脏].{0,3}骤停)))',str,re.IGNORECASE)):
        a = -1
    elif bool(re.search(r'([伴有发生继反复出现示].*?((心源性昏)|(心源性休克)|(意识.?丧失)|(室.??颤)|(心[跳脏].{0,3}骤停)))',str,re.IGNORECASE)):
        a = 1
    elif bool(re.search(r'(电复律)|(意识.?丧失)|(心源性昏)|(心源性休克)|(室.??颤)|(心[跳脏].{0,3}骤停)',str,re.IGNORECASE)):
        a = 1
    return a


def st_predict(str):
    a = -1
    if bool(re.search(r'非特异性ST.{0,4}((改变)|(变化)|(异常))',str,re.IGNORECASE)):
        a = 1
    elif bool(re.search(r'([非未无].{0,6}st.{0,7}?((改变)|(变化)|(抬高)|(压低)|(下移)|(异常)))|(st.{0,3}?正常)',str,re.IGNORECASE)):
        a = 0
    elif bool(re.search(r'(st.{0,9}?((改变)|(变化)|(抬高)|(压低)|(降低)|(下移)|(上移)|(上升)|(异常)|(倒置)))|(((不正常)|(异常)).{0,3}st)',str,re.IGNORECASE)):
        a = 1
    elif bool(re.search(r'(st.*?((改变)|(变化)|(抬高)|(低)|(下)|(上)|(异常)))',str,re.IGNORECASE)):
        a = 1
    return a


def chf_predict(str):
    a = -1
    if bool(re.search(r'[无未].*?(((外周)|(颈)|(肾)|(下肢)).{0,3}?动脉.{0,5}?((硬化)|(狭窄)|(闭塞)))',str,re.IGNORECASE)):
        a = 0
    elif bool(re.search(r'((外周)|(颈)|(肾)|(下肢)).{0,3}?动脉[^无未]{0,6}?((硬化)|(狭窄)|(闭塞))',str,re.IGNORECASE)):
        a = 1
    return a

def hvd_predict(str):
    a = -1
    if bool(re.search(r'(无.*?下肢{0,3}?水肿)|(充血.{0,2}心.{0,2}衰.*风险)',str,re.IGNORECASE)):
        a = 0
    elif bool(re.search(r'(充血.{0,2}心.{0,2}衰)|(下肢[^无未]{0,5}?水肿)',str,re.IGNORECASE)):
        a = 1
    return a

def diabetes_predict(str):
    a = -1
    if bool(re.search(r'([无未史不否明除].*?糖尿病)|(糖尿病.*?[史可])|(((子)|(配偶)|(老伴)|(爱人)|(弟)|(父)|(母)|(兄)|(姐)|(妹)).*?糖尿病)', str, re.IGNORECASE)):
        a = 0
    elif bool(re.search(r'(糖尿病)', str, re.IGNORECASE)):
        a = 1
    return a



def killip_output():
    DOMTree = xml.dom.minidom.parse(r"E:\all_for_AME_detection_big_data1.xml")
    collection = DOMTree.documentElement
    Records = collection.getElementsByTagName("Record")
    sum = 0
    sum1 = 0
    a = []
    empty_record = []
    print('start')
    for Record in Records:
        if Record.hasAttribute("patientId") and Record.hasAttribute("visitId"):
            # a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
            # print("patientId: %s " % MemoContent.getAttribute("patientId"))
            MemoContents = Record.getElementsByTagName("MemoContent")
            # if Record.getAttribute("patientId")=='Y1768089' and Record.getAttribute("visitId")=='1':
            #     print(MemoContents)
            # for m in MemoContents:
            #     print(m.getAttribute("content"))
            #     print(m)
            if MemoContents == []:
                empty_record.append([Record.getAttribute("patientId"), int(Record.getAttribute("visitId"))])
                print(Record.getAttribute("patientId"), Record.getAttribute("visitId"))
            n = 0
            for MemoContent in MemoContents:
                str = ''
                if n == 1:
                    break

                for s in MemoContent.getAttribute("content"):

                    if s == ';' or s == '；' or s == '。' or s == ',' or s == '，':

                        num = killip_predict(str)
                        str2 = str
                        str = ''

                        if bool(re.search(r'([啰罗]音)|(killip)', str2, re.IGNORECASE)):
                            sum1 = sum1 + 1
                            if num > 0:
                                a.append(
                                    [Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), num, str2])
                                n = 1
                                sum = sum + 1

                                break
                            else:
                                print(Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), str2)

                    else:
                        str = str + s
    print(sum1)
    print(sum)

    empty_record = pd.DataFrame(empty_record)
    empty_record.columns = ['patient_id', 'visit_id']

    empty_record.to_excel('E:/emptyRecordId.xlsx', index=False, encoding='UTF-8')
    a = pd.DataFrame(a)
    a.columns = ['patient_id', 'visit_id', 'killip', 'text']
    print(a)
    database = pd.read_excel("e:/id.xlsx")
    r = pd.merge(a, database, how='right', on=['patient_id', 'visit_id'])
    print(r)
    r.to_excel('E:/kp11.xlsx', index=False, encoding='UTF-8')
    # a.to_excel('E:/Killip.xlsx',index=False, encoding='UTF-8')
    # 12512 rows x 849 columns
    DOMTree = xml.dom.minidom.parse(r"E:\all_for_AME_detection_big_data02.xml")
    collection = DOMTree.documentElement

    Records = collection.getElementsByTagName("Record")
    sum = 0
    sum1 = 0
    a = []
    print('start')
    for Record in Records:
        if Record.hasAttribute("patientId") and Record.hasAttribute("visitId"):
            # a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
            # print("patientId: %s " % MemoContent.getAttribute("patientId"))
            MemoContents = Record.getElementsByTagName("MemoContent")
            n = 0
            for MemoContent in MemoContents:
                str = ''
                if n == 1:
                    break
                for s in MemoContent.getAttribute("content"):

                    if s == ';' or s == '；' or s == '。' or s == ',' or s == '，':

                        num = killip_predict(str)
                        str2 = str
                        str = ''
                        if bool(re.search(r'([啰罗]音)|(killip)', str2, re.IGNORECASE)):
                            # sum1 = sum1 + 1
                            # n = 1
                            # a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
                            # break
                            if num > 0:
                                a.append(
                                    [Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), num, str2])
                                # print(MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId")),num)
                                n = 1
                                sum = sum + 1
                                str = ''
                                break
                            else:
                                print(Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), str2)
                                str = ''
                    else:
                        str = str + s

                # print("text: %s " % i.getAttribute("content"))
    print(sum1)
    print(sum)
    a = pd.DataFrame(a)
    a.columns = ['patient_id', 'visit_id', 'killip', 'text']
    print(a)
    print(sum)
    database = pd.read_excel("e:/id.xlsx")

    r = pd.merge(a, database, how='right', on=['patient_id', 'visit_id'])
    print(r)
    r.to_excel('E:/kp2.xlsx', index=False, encoding='UTF-8')

# p = re.compile(ptext, re.IGNORECASE)
# #p = re.compile('abc', re.I) #for short
#
# r = p.match(text)

def xintiaozhouting_output():
    DOMTree = xml.dom.minidom.parse(r"E:\all_for_AME_detection_big_data1.xml")
    collection = DOMTree.documentElement

    Records = collection.getElementsByTagName("Record")
    sum = 0
    sum1 = 0
    a = []
    empty_record = []
    print('start')
    for Record in Records:
        if Record.hasAttribute("patientId") and Record.hasAttribute("visitId"):
            MemoContents = Record.getElementsByTagName("MemoContent")

            n = 0
            for MemoContent in MemoContents:
                str = ''
                if n == 1:
                    break

                for s in MemoContent.getAttribute("content"):

                    if s == ';' or s == '；' or s == '。' or s == ',' or s == '，':

                        num = cardiac_arrest_predict(str)
                        str2 = str
                        str = ''

                        if bool(re.search(r'(丧失)|(电复律)|(心[跳脏].*停)|(室.??颤)', str2, re.IGNORECASE)):
                            sum1 = sum1 + 1
                            # n = 1
                            # a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
                            # break
                            if num > -1:
                                a.append(
                                    [Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), num, str2])

                                # print(MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId")),num)
                                n = 1
                                sum = sum + 1

                                break
                            else:
                                print(Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), str2, num)

                    else:
                        str = str + s

                # print("text: %s " % i.getAttribute("content"))
    print(sum1)
    print(sum)
    a = pd.DataFrame(a)
    a.columns = ['patient_id', 'visit_id', '心脏骤停', 'text']
    print(a)
    database = pd.read_excel("e:/id.xlsx")

    r = pd.merge(a, database, how='right', on=['patient_id', 'visit_id'])
    print(r)
    r.to_excel('E:/xinzangzhouting1.xlsx', index=False, encoding='UTF-8')

def chf_output():
    DOMTree = xml.dom.minidom.parse(r"E:\all_for_AME_detection_big_data1.xml")
    collection = DOMTree.documentElement

    Records = collection.getElementsByTagName("Record")
    sum = 0
    sum1 = 0
    a = []
    empty_record = []
    print('start')
    for Record in Records:
        if Record.hasAttribute("patientId") and Record.hasAttribute("visitId"):
            # a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
            # print("patientId: %s " % MemoContent.getAttribute("patientId"))
            MemoContents = Record.getElementsByTagName("MemoContent")
            # if Record.getAttribute("patientId")=='Y1768089' and Record.getAttribute("visitId")=='1':
            #     print(MemoContents)
            # for m in MemoContents:
            #     print(m.getAttribute("content"))
            #     print(m)
            # if MemoContents==[]:
            #     empty_record.append([Record.getAttribute("patientId"),int(Record.getAttribute("visitId"))])
            #     print(Record.getAttribute("patientId"),Record.getAttribute("visitId"))
            n = 0
            for MemoContent in MemoContents:
                str = ''
                if n == 1:
                    break

                for s in MemoContent.getAttribute("content"):

                    if s == ';' or s == '；' or s == '。' or s == ',' or s == '，':

                        num = chf_predict(str)
                        str2 = str
                        str = ''

                        if bool(re.search(r'(水肿)|(充血.{0,2}心.{0,2}衰)', str2, re.IGNORECASE)):
                            sum1 = sum1 + 1
                            # n = 1
                            # a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
                            # break
                            if num > 0:
                                a.append(
                                    [Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), num, str2])

                                # print(MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId")),num)
                                n = 1
                                sum = sum + 1

                                break
                            elif num == 0:
                                pass
                            else:
                                print(Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), str2, num)

                    else:
                        str = str + s

                # print("text: %s " % i.getAttribute("content"))
    print(sum1)
    print(sum)

    # empty_record = pd.DataFrame(empty_record)
    # empty_record.columns = ['patient_id','visit_id']
    #
    # empty_record.to_excel('E:/emptyRecordId.xlsx', index=False,encoding='UTF-8')
    a = pd.DataFrame(a)
    a.columns = ['patient_id', 'visit_id', '充血性心衰体征', 'text']
    print(a)

    # a['num'] = 1
    # b = a.groupby('K').count()

    # print(b)

    # for MemoContent in MemoContents:
    #     if MemoContent.hasAttribute("content"):
    #         str=''
    #
    #         if bool(re.search(r'killip.{0,4}级', MemoContent.getAttribute("content"), re.IGNORECASE)):
    #         #if 'Killip' in MemoContent.getAttribute("content") or 'KiLLiP' in MemoContent.getAttribute("content") or 'killip' in MemoContent.getAttribute("content") or 'KILLIP' in MemoContent.getAttribute("content"):
    #             for s in MemoContent.getAttribute("content"):
    #                 if s == '.' or s == ';' or s == '：' or s == '。':
    #                     if bool(re.search(r'心功能.？级.{0,3}killip|killip.{0,4}级', str, re.IGNORECASE)): #'Killip' in str or 'killip' in str or 'KILLIP' in str or 'KiLLiP' in str:
    #                         a.append([str])
    #                         print("text: %s " % str)
    #                     str = ''
    #                 else:
    #                     str =str + s
    #         else:
    #             continue

    #
    # a = pd.DataFrame(a)
    # a.columns = ['K']
    # print(a)
    # a['num'] = 1
    # b = a.groupby('K').count()
    #
    # print(b)
    # a.to_csv('e:/a', header=False, index=False, encoding='UTF-8')

    database = pd.read_excel("e:/id.xlsx")

    r = pd.merge(a, database, how='right', on=['patient_id', 'visit_id'])
    print(r)
    r.to_excel('E:/chf.xlsx', index=False, encoding='UTF-8')

def history_output():
    DOMTree = xml.dom.minidom.parse(r"E:\all_for_AME_detection_big_data1.xml")
    collection = DOMTree.documentElement

    Records = collection.getElementsByTagName("Record")
    sum = 0
    sum1 = 0
    a = []
    empty_record = []
    print('start')
    for Record in Records:
        if Record.hasAttribute("patientId") and Record.hasAttribute("visitId"):
            MemoContents = Record.getElementsByTagName("MemoContent")

            n = 0
            for MemoContent in MemoContents:
                str = ''
                if n == 1:
                    break

                for s in MemoContent.getAttribute("content"):
                    if s == ';' or s == '；' or s == '。' or s == ',' or s == '，':
                        num = chf_predict(str)
                        str2 = str
                        str = ''

                        if bool(re.search(r'((外周)|(颈)|(肾)|(下肢)).*?动脉', str2, re.IGNORECASE)):
                            sum1 = sum1 + 1
                            # n = 1
                            # a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
                            # break
                            if num > 0:
                                a.append(
                                    [Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), num, str2])

                                # print(MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId")),num)
                                n = 1
                                sum = sum + 1

                                break
                            elif num == 0:
                                pass
                            else:
                                print(Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), str2, num)

                    else:
                        str = str + s

                # print("text: %s " % i.getAttribute("content"))
    print(sum1)
    print(sum)
    a = pd.DataFrame(a)
    a.columns = ['patient_id', 'visit_id', '既往血管系统疾病史2', 'text2']
    print(a)
    database = pd.read_excel("e:/id.xlsx")
    r = pd.merge(a, database, how='right', on=['patient_id', 'visit_id'])
    r = r.fillna(0)
    print(r)
    r2 = operate_oracle()
    r3 = pd.merge(r, r2, how='right', on=['patient_id', 'visit_id'])
    r3['既往血管系统疾病史'] = 0
    r3['text'] = 0
    print(r3)
    r3.to_excel('E:/h.xlsx', index=False, encoding='UTF-8')
    num = 0
    del r
    del r2
    for i in range(len(r3)):
        num = num + 1
        if num % 300 == 0:
            print(num, '/', len(r3))

        if r3['既往血管系统疾病史1'][i] == 0 and r3['既往血管系统疾病史2'][i] == 0:
            r3['既往血管系统疾病史'][i] = 0

        else:
            r3['既往血管系统疾病史'][i] = 1

        if r3['text1'][i] != 0:
            r3['text'][i] = r3['text1'][i]
        elif r3['text2'][i] != 0:
            r3['text'][i] = r3['text2'][i]
        else:
            r3['text'][i] = None

    r3.to_excel('E:/history3.xlsx', index=False, encoding='UTF-8')

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
    history.columns = ['patient_id', 'visit_id','既往血管系统疾病史1','text1']


    database = pd.read_excel("e:/id.xlsx")
    r2 = pd.merge(history, database, how='right', on=['patient_id', 'visit_id'])
    r2 = r2.fillna(0)
    return r
    # print(r)
    # r.to_excel('E:/history2.xlsx', index=False, encoding='UTF-8')


def main():
    DOMTree = xml.dom.minidom.parse(r"E:\all_for_AME_detection_big_data1.xml")
    collection = DOMTree.documentElement

    Records = collection.getElementsByTagName("Record")
    sum = 0
    sum1 = 0
    a = []
    empty_record = []
    print('start')
    for Record in Records:
        if Record.hasAttribute("patientId") and Record.hasAttribute("visitId"):
            MemoContents = Record.getElementsByTagName("MemoContent")

            n = 0
            for MemoContent in MemoContents:
                str = ''
                if n == 1:
                    break

                for s in MemoContent.getAttribute("content"):
                    if s ==';' or s=='；' or s == '。'or s==',' or  s == '，':
                        num = diabetes_predict(str)
                        str2 = str
                        str = ''

                        if bool(re.search(r'糖尿病', str2, re.IGNORECASE)):
                            sum1 = sum1 + 1
                            # n = 1
                            # a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
                            # break
                            if num > 0:
                                a.append([Record.getAttribute("patientId"), int(Record.getAttribute("visitId")), num, str2])

                                #print(MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId")),num)
                                n = 1
                                sum = sum + 1

                                break
                            elif num == 0:
                                pass
                            else:
                                print(Record.getAttribute("patientId"), int(Record.getAttribute("visitId")),str2,num)

                    else:
                        str = str + s

                #print("text: %s " % i.getAttribute("content"))
    print(sum1)
    print(sum)
    a = pd.DataFrame(a)
    a.columns = ['patient_id','visit_id','糖尿病2','text2']
    print(a)
    database= pd.read_excel("e:/id.xlsx")
    r = pd.merge(a, database, how='right',on=['patient_id', 'visit_id'])
    r = r.fillna(0)
    print(r)
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
        and (regexp_like(d.DIAGNOSIS_DESC, '糖尿病', 'i')
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
    history.columns = ['patient_id', 'visit_id','糖尿病1','text1']


    database = pd.read_excel("e:/id.xlsx")
    r2 = pd.merge(history, database, how='right', on=['patient_id', 'visit_id'])
    r2 = r2.fillna(0)
    r3 = pd.merge(r, r2, how='right',on=['patient_id', 'visit_id'])
    r3['糖尿病'] = 0
    r3['text'] = 0
    print(r3)
    r3.to_excel('E:/diabetes1.xlsx', index=False, encoding='UTF-8')
    del r
    del r2
    num = 0
    for i in range(len(r3)):
        num = num + 1
        if num % 300 == 0:
            print(num, '/', len(r3))

        if r3['糖尿病1'][i] == 0 and r3['糖尿病2'][i] == 0:
            r3['糖尿病'][i] = 0

        else:
            r3['糖尿病'][i] = 1

        if r3['text1'][i] != 0:
            r3['text'][i] = r3['text1'][i]
        elif r3['text2'][i] != 0:
            r3['text'][i] = r3['text2'][i]
        else:
            r3['text'][i] = None

    r3.to_excel('E:/diabetes.xlsx', index=False, encoding='UTF-8')



if __name__ == '__main__':
    main()