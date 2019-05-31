from xml.dom.minidom import parse
import xml.dom.minidom
import re
import numpy
import pickle
import time
import pandas as pd
import numpy as np
import xlwt


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


def killip_predict(str):
    a = 0

    # p = re.compile('(killip.{0,4}?(4|IV|Ⅳ)级)|(心功能.{0,3}?(4|IV|Ⅳ)级.{0,3}killip)', re.IGNORECASE)
    if bool(re.search(r'(killip.{0,4}?(4|IV|Ⅳ)级)|(心功能.{0,3}?(4|IV|Ⅳ)级.{0,3}killip)', str, re.IGNORECASE)):
        a = 4
    elif bool(re.search(r'(killip.{0,4}?(3|III|Ⅲ)级)|(心功能.{0,3}?(3|III|Ⅲ)级.{0,3}killip)', str, re.IGNORECASE)):
        a = 3
    elif bool(re.search(r'(killip.{0,4}?(2|II|Ⅱ)级)|(心功能.{0,3}?(2|II|Ⅱ)级.{0,3}killip)', str, re.IGNORECASE)):
        a = 2
    elif bool(re.search(r'(killip.{0,4}?(1|I|Ｉ)级)|(心功能.{0,3}?(1|I|Ｉ)级.{0,3}killip)', str, re.IGNORECASE)):
        a = 1
    else:
        a = 0
    return a


# p = re.compile('abc', re.I) #for short11

# r = p.match(text)
# 输出关键字文本和文本数量
def sum_idOfItem():
    DOMTree = xml.dom.minidom.parse(r"E:\all_for_AME_detection_big_data1.xml")
    collection = DOMTree.documentElement

    MemoContents = collection.getElementsByTagName("Record")
    sum = 0
    sum1 = 0
    a = []
    print('start')
    for MemoContent in MemoContents:
        if MemoContent.hasAttribute("patientId") and MemoContent.hasAttribute("visitId"):

            m = MemoContent.getElementsByTagName("MemoContent")
            n = 0
            for i in m:
                str = ''
                if n == 1:
                    break
                for s in i.getAttribute("content"):

                    if s == ';' or s == '；' or s == '。':
                        num = killip_predict(str)
                        if bool(re.search(r'st', str, re.IGNORECASE)):
                            sum1 = sum1 + 1
                            n = 1
                            a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId"))])
                            break
                            # if num > 0:
                            #     a.append([MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId")), num])
                            #     #print(MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId")),num)
                            #     n = 1
                            #     sum = sum + 1
                            #     break
                            # else:
                            #     print(MemoContent.getAttribute("patientId"), int(MemoContent.getAttribute("visitId")),str)
                    else:
                        str = str + s

                # print("text: %s " % i.getAttribute("content"))
    print(sum1)
    a = pd.DataFrame(a)
    a.columns = ['patient_id', 'visit_id']  # ,'killip']
    print(a)
    print(sum)
    database = pd.read_excel("e:/id.xlsx")

    r = pd.merge(a, database, on=['patient_id', 'visit_id'])
    print(r)
    # r.to_excel('E:/kk.xlsx', index=False, encoding='UTF-8')


# 让某些字符串大小写不敏感 如比较和查询不敏感 其他敏感

# 输出关键字文本
def output_itemText():
    DOMTree = xml.dom.minidom.parse(r"E:\all_for_AME_detection_big_data1.xml")
    collection = DOMTree.documentElement
    sum = 0
    a = []
    print('start')
    MemoContents = collection.getElementsByTagName("MemoContent")
    for MemoContent in MemoContents:
        if MemoContent.hasAttribute("content"):
            str = ''
            if bool(re.search(r'(st)', MemoContent.getAttribute("content"), re.IGNORECASE)):
                # if 'Killip' in MemoContent.getAttribute("content") or 'KiLLiP' in MemoContent.getAttribute("content") or 'killip' in MemoContent.getAttribute("content") or 'KILLIP' in MemoContent.getAttribute("content"):
                for s in MemoContent.getAttribute("content"):
                    if s == '.' or s == ';' or s == '：' or s == '。':
                        if bool(re.search(r'(st)', str, re.IGNORECASE)):  # (心跳骤停)|(丧失)|(心肺复苏)|(电复律)|(室颤)
                            a.append([str])
                            print("text: %s " % str)
                        str = ''
                    else:
                        str = str + s
            else:
                continue

    a = pd.DataFrame(a)
    a.columns = ['ST']
    print(a)
    a['num'] = 1
    b = a.groupby('ST').count()

    # print(b)
    # a.to_csv('e:/a', header=False, index=False, encoding='UTF-8')
    #
    # database = pd.read_excel("e:/id.xlsx")
    #
    # r = pd.merge(a, database, on=['patient_id', 'visit_id'])
    # print(r)
    # r.to_excel('E:/kk.xlsx', index=False, encoding='UTF-8')
    b.to_excel('E:/l.xlsx', encoding='UTF-8')


# 方案 封装为类

def item_operate():
    data = pd.read_excel('e:/filled.xlsx')
    num = 0
    data['心脏标志物升高'] = 0
    for i in range(len(data)):
        num = num + 1
        if num % 300 == 0:
            print(num, '/', len(data))
        if data['心脏标志物升高'][i] == 0:
            if data['肌钙蛋白T'][i] > 0.1:
                data['心脏标志物升高'][i] = 1
            elif data['肌酸激酶同工酶定量测定'][i] > 6.5:
                data['心脏标志物升高'][i] = 1
    data.to_excel('e:/filled.xlsx', index=False, encoding='utf-8')


def item_operate2():
    data = pd.read_excel('e:/filled.xlsx')
    num = 0
    data['肌酐清除率'] = None
    for i in range(len(data)):
        num = num + 1
        if num % 300 == 0:
            print(num, '/', len(data))
        if data['sex'][i] == 0:
            data['肌酐清除率'][i] = 0.85 * data['体重'][i] * (140 - data['age'][i]) / (0.818 * data['肌酐'][i])
        else:
            data['肌酐清除率'][i] = data['体重'][i] * (140 - data['age'][i]) / (0.818 * data['肌酐'][i])

    data.to_excel('e:/filled1.xlsx', index=False, encoding='utf-8')


class iStr(str):

    def __init__(self, *args):
        self.lowered = str.lower(self)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, str.__repr__(self))

    def __hash__(self):
        return hash(self.lowered)


def _make_case_insensitive(name):
    str_meth = getattr(str, name)

    def x(self, other, *args):

        try:
            other = other.lower()

        except(TypeError, AttributeError, ValueError):
            pass

        return str_meth(self.lowered, other, *args)

    setattr(iStr, name, x)


# p = re.compile(ptext, re.IGNORECASE)
# #p = re.compile('abc', re.I) #for short
#
# r = p.match(text)


def main():
    # item_operate2()
    # output_itemText()
    r3 = pd.read_csv('c:/Users/dell/Desktop/luyi.xlsx', encoding='UTF-8')
    # r3.to_excel('E:/diabetes.xlsx', index=False, encoding='UTF-8')
    print("start")

    pd['grace'] = 0
    pd['crusade'] = 0

    Sex/Age/脉搏(L)/SBP(L)/心脏骤停(M)/ST3/肌酐(L)/肌酸激酶同工酶(L)/红细胞比积测定(L)/糖尿病及伴发症(M)



     killiP,充血性心衰体征，既往血管系统疾病史




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
    item_operate2()
