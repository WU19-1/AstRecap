import requests
import student
import pandas as pd
import auth
import json
import re

def main():
    session, phpsessid = auth.login()

    changeRole = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/login/switchrole/4/4",headers={
        'Referer' : 'https://binusmaya.binus.ac.id/newStaff/',
        'Cookie' : phpsessid,
        'X-Requested-With': 'XMLHttpRequest'
    })

    resp = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/monitoring/forumMonitoring/getTableDetail",headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": phpsessid,
        "Host": "binusmaya.binus.ac.id",
        "Origin":"https://binusmaya.binus.ac.id",
        "Referer":"https://binusmaya.binus.ac.id/newStaff/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    },json={
        "INSTITUTION":"BNS01",
        "ACAD_CAREER":"RS1",
        "STRM":"2010",
        "CAMPUS":"All",
        "ACAD_ORG":"CSCI",
        "DEPARTMENT":"All",
        "CRSE_ID":"All",
        "LECTURERID":"All",
        "CLASS_SECTION":"All",
        "CLASS_TYPE":"All",
        "DELIVERY_MODE":"All",
        "START_DT":"2020-09-14",
        "END_DT":"2021-02-20"
    })

    df = student.dataframeInitAllAst()
    writer = pd.ExcelWriter('AstForumRecap.xlsx',engine='xlsxwriter')
    cellNumberIdx = 2

    for i in resp.json():
        if re.search("D[0-9][0-9][0-9][0-9]", i['KODE_DOSEN']) != None or i['CLASS_SECTION'][0] == 'X' or i['N_DELIVERY_MODE'] == 'VC':
            continue
        if 'LC' in i['KODE_DOSEN']:
            df = df.append(pd.Series(data={
                'initial':i['KODE_DOSEN']
                'course':i['CRSE_CODE'],
                'class':i['CLASS_SECTION'],
                'timestamp':i['ForumPostDate'],
                'meeting type':i['N_DELIVERY_MODE'],
                'title':i['ForumThreadTitle']
            },name=cellNumberIdx))
        else:
            df = df.append(pd.Series(data={
                'initial':i['KODE_DOSEN'][0] + i['KODE_DOSEN'][1],
                'course':i['CRSE_CODE'],
                'class':i['CLASS_SECTION'],
                'timestamp':i['ForumPostDate'],
                'meeting type':i['N_DELIVERY_MODE'],
                'title':i['ForumThreadTitle']
            },name=cellNumberIdx))
        cellNumberIdx = cellNumberIdx + 1
    
    print(df)

    df.to_excel(writer, sheet_name='Recap', index=False)
    writer.save()
    writer.close()

main()