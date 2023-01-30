import pandas as pd
from itertools import product
import re
from datetime import datetime

df = pd.read_excel('takhasosi.xlsx')

cdf = df[df['زمانبندي تشکيل کلاس'].notnull() & df['انتخاب']][['نام درس','زمانبندي تشکيل کلاس']]

myDict = {}

class Lesson:
    def __init__(self,detail:str):
        times = re.findall(r'\d+:\d+',detail) #0 => start 1=> end
        self.day = re.findall(r'^\w+',detail)[0]
        self.start = datetime.strptime(times[0],'%H:%M')
        self.end = datetime.strptime(times[1],'%H:%M')
    def conflits(self,other):
        if(other.start<=self.start<other.end or self.start<=other.start<self.end):
            return True
        return False
    def __str__(self):
        return f'{self.day}|{self.start}|{self.end}'


for index,row in cdf.iterrows():
    myDict.setdefault(row['نام درس'],[])
    myDict[row['نام درس']].append(Lesson(row['زمانبندي تشکيل کلاس']))

validPlans = []

for choices in product(*myDict.values()):
    temp = []
    ok = True
    for les in choices:
        if(ok):
            for les2 in temp:
                if(les.conflits(les2)):
                    ok = False
                    break
            if(ok):
                temp.append(les)
    if(ok):
        temp.sort(key=lambda x:x.start)
        validPlans.append(temp)                


print(validPlans)