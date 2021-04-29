#nation states api wrapper (which is absoulute garbage)

import requests
import time
import xml.etree.ElementTree as ET


class api:
    def __init__(self, *args):
        cnt = 0
        Ivars = ['Password', 'Nation', 'UserAgent']
        for i in args:
            try:
                setattr(self.state, Ivars[cnt], i)
            except Exception as e:
                print(f'error occured: {e}')
            cnt=cnt+1
        if self.functions.canLogin:
            a = self.functions.query('ping')
            self.state.pin = a.headers['X-Pin']
    #sub classes
    class state:
        Password = ''
        Nation = ''
        UserAgent = 'email:walkerffo22@hotmail.com'
        pin = ''

    class functions:
        def query(option):
            if api.state.pin == '':
                headers = {'X-Password' : api.state.Password, 'user-agent' : api.state.UserAgent}
            else:
                headers = {'X-Pin' : api.state.pin, 'user-agent' : api.state.UserAgent}
            r = requests.get(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={api.state.Nation}&q={option}', headers=headers)
            if api.state.pin == '':
                api.state.pin = r.headers['X-Pin']
            if r.status_code != 200:
                raise api.exception.exception.httpError(r.content)
            return(r)
        
        def canLogin():
            if api.state.Password != "" & api.state.Nation != "" & api.state.UserAgent != "":
                return(True)
            return(False)

        def validateIssueID(id):#checks if the issue id is a valid one that you can acess
            issues = api.functions.getIssues()
            for issue in issues:
                if issues[0].attrib['id'] == str(id):
                    return True
            return(False)

        def listValidIssueIDs():
            issues = api.functions.getIssues()
            IDs = []
            for issue in issues:
                IDs.append(issue.attrib['id'])
            return(IDs)

        def getTimeTillNextIssue():
            curl = api.functions.query('nextissuetime')
            xml = curl.content
            try:
                xmld = ET.fromstring(xml)
            except Exception as e:
                print(f'error occured: {e}')
                print(f'xml content: {xml}')
            utime = int(xmld[0].text)
            ctime = time.time()
            rtime = utime - int(ctime)
            times = [rtime,utime]
            return(times)

        def getIssues_OLD():
            curl = api.functions.query('issues')
            xml = curl.content
            xmld = ET.fromstring(xml)
            return(xmld[0])

        def getIssues():
            curl = api.functions.query('issues')
            xml = curl.content
            xmld = ET.fromstring(xml)
            out=[]
            for f in xmld[0]:
                out.append(api.vars.Issue(f))
            return(out)
            
        def submitIssue(issue, choice):
            headers = {'X-Password' : api.state.Password, 'user-agent' : api.state.UserAgent}
            payload={'nation' : f'{api.state.Nation}','c' : 'issue','issue' : f'{issue}','option' : f'{choice}'}
            http = requests.post(f'https://www.nationstates.net/cgi-bin/api.cgi', data=payload, headers=headers)
            xml = http.content
            pxml = ET.fromstring(xml)
            return(http, pxml)

    #exceptions
    class exception:
        class httpError(Exception):
            pass

    #custom types
    class vars:
        class Issue:
            def __init__(self,xml):
                self.id=xml.attrib['id']
                self.title=xml[0].text
                self.background=xml[1].text
                self.options=[]
                for f in xml.findall('OPTION'):
                    self.options.append(f.text)
            def __str__(self):
                return(f'"{self.title}"ID:{self.id}')
            def __repr__(self):
                return(f'<Issue {self.id}, {self.title} with {len(self.options)} options>')
            id = 0
            title = ""
            background = ""
            options = []
