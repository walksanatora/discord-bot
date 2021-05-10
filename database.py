import json
class db:
    def __init__(self,file):
        self.file=file
        with open(file,'r') as f:
            self.data = json.load(f)
            print(f'opened json {self.data} with type {type(self.data)}')
    def saveDB(self):
        with open(self.file,'w') as f:
            json.dump(self.data,f)

    file=''
    data={}