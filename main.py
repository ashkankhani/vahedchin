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
    def __str__(self):
        return f'{self.day}|{self.start}|{self.end}'


for index,row in cdf.iterrows():
    myDict.setdefault(row['نام درس'],[])
    myDict[row['نام درس']].append(Lesson(row['زمانبندي تشکيل کلاس']))


for key,value in myDict.items():
    print(value[0])