#nation states api wrapper (which is absoulute garbage)

import requests
import time
import xml.etree.ElementTree as ET
import logs

class api:
    def __init__(self,UseAutologin,Username,Password):
        self.state.Nation=Username
        request = self.functions.query('ping',Password)
        try:
            if bool(UseAutologin):
                self.state.Auth=request.headers['X-Autologin']
            else:
                self.state.Auth=request.headers['X-Pin']
            self.state.UseAutologin = UseAutologin
        except KeyError:
            logs.log('exception',request.content,request.headers)
    #sub classes
    class state:
        UseAutologin = False
        Auth = ''
        Nation = ''
        UserAgent = 'Nationstates.py, the Nationstates api wrapper written by walksanator email:walkerffo22@hotmail.com'

    class functions:
        def query(option, *args):
            #set the headers
            if api.state.Auth == '':
                headers = {'X-Password' : args[0], 'user-agent' : api.state.UserAgent}
            else:
                if api.state.UseAutologin:
                    headers = {'X-AutoLogin' : api.state.Auth, 'user-agent' : api.state.UserAgent}
                else:
                    headers = {'X-Pin' : api.state.Auth, 'user-agent' : api.state.UserAgent}
            #make the request
            r = requests.get(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={api.state.Nation}&q={option}', headers=headers)
            if r.status_code != 200:
                logs.log(headers,"\n\nrequest headers\n\n",r.headers)
                raise api.exception.httpError(r.content)
            return(r)
        
        def canLogin():
            if api.state.Password != "" & api.state.Nation != "" & api.state.UserAgent != "":
                return(True)
            return(False)

        def validateIssueID(id):#checks if the issue id is a valid one that you can acess
            issues = api.functions.getIssues()
            for issue in issues:
                if issue.id == str(id):
                    return True
            return(False)

        def listValidIssueIDs():
            issues = api.functions.getIssues()
            IDs = []
            for issue in issues:
                IDs.append(issue.id)
            return(IDs)

        def getTimeTillNextIssue():
            curl = api.functions.query('nextissuetime')
            xml = curl.content
            try:
                xmld = ET.fromstring(xml)
            except Exception as e:
                logs.log(f'error occured: {e}')
                logs.log(f'xml content: {xml}')
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

            if api.state.UseAutologin:
                headers = {'X-AutoLogin' : api.state.Auth, 'user-agent' : api.state.UserAgent}
            else:
                headers = {'X-Pin' : api.state.Auth, 'user-agent' : api.state.UserAgent}
            payload={'nation' : f'{api.state.Nation}','c' : 'issue','issue' : f'{issue}','option' : f'{choice}'}
            http = requests.post(f'https://www.nationstates.net/cgi-bin/api.cgi', data=payload, headers=headers)
            xml = http.text
            logs.log(xml)
            pxml = ET.fromstring(xml)
            return(http, pxml)
        
        def reGenKey(UseAutologin,Username,Password):
            api.state.Auth = '' #invaladate auth so it will use password
            api.state.Nation=Username
            request = api.functions.query('ping',Password)
            try:
                if bool(UseAutologin):
                    api.state.Auth=request.headers['X-Autologin']
                else:
                    api.state.Auth=request.headers['X-Pin']
            except KeyError as e:
                logs.log(e,type(e),'keyerror',request.headers)
                pass
            api.state.UseAutologin = UseAutologin

    #exceptions
    class exception:
        class httpError(Exception):
            pass

    #custom types
    class vars:
        class Issue:
            def __init__(self,xml):
                self.rawXML=xml
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
            rawXML = ''
