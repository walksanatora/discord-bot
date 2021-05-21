import json
class db:
    def __init__(self,file):
        self.file=file
        with open(file,'+r') as f:
            self.data = json.load(f)
    def saveDB(self):
        with open(self.file,'+w') as f:
            json.dump(self.data,f)
    
    def reloadData(self):
        with open(self.file,'+r') as f:
            self.data = json.load(f)

    file=''
    data={}