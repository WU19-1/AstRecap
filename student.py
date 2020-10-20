import numpy
import pandas
import xlsxwriter

redFormat = None

greenFormat = None

def formatInit(workbook):
    global redFormat,greenFormat

    redFormat = workbook.add_format()
    greenFormat = workbook.add_format()

    greenFormat.set_pattern(1)
    greenFormat.set_bg_color('#C6EFCE')
    redFormat.set_pattern(1)
    redFormat.set_bg_color('#FFC7CE')

def dataframeInit():
    df = pandas.DataFrame(data=None,columns=['name','nim','role','timestamp'],index=None)
    return df

def dataframeInitAst():
    df = pandas.DataFrame(data=None,columns=['course','class','timestamp','title','link'],index=None)
    return df

def dataframeInitAllAst():
    df = pandas.DataFrame(data=None,columns=['initial','course','class','timestamp','meeting type','title'],index=None)
    return df

class Data:
    filename = ""
    writer = None

    def __init__(self,courseCode,classCode,initial):
        filename = initial + " - " + courseCode + " - " + classCode + ".xlsx"
        self.writer = pandas.ExcelWriter("./result/" + filename,engine='xlsxwriter')

class DataAst:
    filename = ""
    writer = None

    def __init__(self,initial):
        filename = initial + ' - Forum Recap'+ ".xlsx"
        self.writer = pandas.ExcelWriter("./result/" + filename,engine='xlsxwriter')
        
def convertResultSetToArr(data):
    arr = []
    for i in data:
        try:
            arr.append(i.text)
        except AttributeError:
            continue
    return arr

def findAssistant(listData,startIdx,stopIdx):
    for idx in range(startIdx,stopIdx):
        if listData[idx]['Role'] == 'Assistant':
            return idx
    raise ValueError

def findAssistantWithInitial(listData,startIdx,stopIdx,initial):
    for idx in range(startIdx,stopIdx):
        if listData[idx]['Role'] == 'Assistant' and initial in listData[idx]['UserID']:
            return idx
    raise ValueError

def findStudent(listData,nim):
    for idx, data in enumerate(listData):
        
        if nim in data['UserID']:
            return idx
    raise ValueError

def generateCellsNumbering(rowCount):
    arr = {}
    if rowCount <= 2:
        rowCount = rowCount + 2
    for i in range(2,rowCount+2,1):
        arr[i] = ('E' + str(i))
    return arr
    