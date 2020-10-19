from bs4 import BeautifulSoup
import requests
import student
import pandas as pd
import auth
import json
from urllib.parse import unquote

def main():
    myInitial = input("Insert your initial here (without generation) : ")
    session, phpsessid = auth.login()

    session.post("https://binusmaya.binus.ac.id/services/ci/index.php/login/switchrole/1/201",headers={
        'Referer' : 'https://binusmaya.binus.ac.id/newStaff/',
        'Cookie' : phpsessid,
        'X-Requested-With': 'XMLHttpRequest'
    })
    
    session.get("https://binusmaya.binus.ac.id/newLecturer/",headers={
        'Referer' : 'https://binusmaya.binus.ac.id/newStaff/',
        'Cookie' : phpsessid
    })

    df = student.dataframeInitAst()
    xlsxData = student.DataAst(myInitial)

    resp = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/forum/getCourse",headers={
        'Referer' : 'https://binusmaya.binus.ac.id/newLecturer/#',
        'Cookie' : phpsessid,
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'Content-Type' : 'application/json',
        'Connection':'keep-alive',
        'Accept-Encoding':'gzip,deflate,br'
    },json={
        'Institution' : 'BNS01',
        'acadCareer' : 'RS1',
        'period' : '2010'
    })

    for i in json.loads(resp.json()['rows']):
        print('Course ID :',i['ID'], '-', i['Caption'])
        classes = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/forum/getClass",headers={
            'Referer' : 'https://binusmaya.binus.ac.id/newLecturer/#',
            'Cookie' : phpsessid,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Content-Type' : 'application/json',
            'Connection':'keep-alive',
            'Accept-Encoding':'gzip,deflate,br'
        },json={
            'Institution' : 'BNS01',
            'acadCareer' : 'RS1',
            'course' : i['ID'],
            'period' : '2010'
        })

        for j in json.loads(classes.json()['rows']):
            print('ClassesID :',j['ID'], '-',j['Caption'])
            forumID = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/forum/getThread",headers={
            'Referer' : 'https://binusmaya.binus.ac.id/newLecturer/#',
            'Cookie' : phpsessid,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Content-Type' : 'application/json',
            'Connection':'keep-alive',
            'Accept-Encoding':'gzip,deflate,br'
            },json={
                'Institution' : 'BNS01',
                'acadCareer' : 'RS1',
                'course' : i['ID'],
                'period' : '2010',
                'SESSIONIDNUM' : '',
                'classid' : j['ID'],
                'forumtypeid' : 1,
                'topic' : ""
            })

            # peopleList = getclass.getPeople(session,phpsessid,i['ID'],j['ID'])

            for k in json.loads(forumID.json()['rows']):
                if k['ID'] == -1:
                    print('This forum has no post')
                    continue
                forumPost = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/forum/getReply",headers={
                'Referer' : 'https://binusmaya.binus.ac.id/newLecturer/#',
                'Cookie' : phpsessid,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': '*/*',
                'Content-Type' : 'application/json',
                'Connection':'keep-alive',
                'Accept-Encoding':'gzip,deflate,br'
                },json={
                    'threadid' : k['ID'] + '?=1'
                })
                
                student.formatInit(xlsxData.writer.book)
                
                forumData = json.loads(forumPost.json()['rows'])

                cellNumberIdx = 2

                forumTitle = unquote(k['ForumThreadTitle'])
                
                try:
                    astOneIdx = student.findAssistantWithInitial(forumData,0,len(forumData),myInitial)
                    print(forumData[astOneIdx]['UserID'],'-',forumData[astOneIdx]['Name'],'-',forumData[astOneIdx]['Role'],'-',forumData[astOneIdx]['PostDate'])
                    df = df.append(pd.Series(data={
                        'course':i['Caption'],
                        'class':j['Caption'],
                        'timestamp':forumData[astOneIdx]['PostDate'],
                        'title' : forumTitle,
                        'link' : 'https://binusmaya.binus.ac.id/newLecturer/#/forum/reader.' + k['ID'] + '?=1'
                    },name=cellNumberIdx))
                except ValueError:
                    print('Cannot find assistant in this forum thread')
    
    df.to_excel(xlsxData.writer, sheet_name=myInitial + ' Forum Recap', index=False)
    xlsxData.writer.save()
    xlsxData.writer.close()

main()