import pandas as pd
from itertools import product
import re
from datetime import datetime,timedelta

df = pd.read_excel('takhasosi.xlsx')

cdf = df[df['زمانبندي تشکيل کلاس'].notnull() & df['انتخاب']][['نام درس','زمانبندي تشکيل کلاس','استاد']]

myDict = {}




class Lesson:
    def __init__(self,name:str,teacher:str,detail:str)->None:
        times = re.findall(r'\d+:\d+',detail) #0 => start 1=> end
        self.name = name
        self.day = re.findall(r'^\w+',detail)[0]
        self.start = datetime.strptime(times[0],'%H:%M')
        self.end = datetime.strptime(times[1],'%H:%M')
        self.teacher = teacher
    def conflits(self,other):
        if(self.day != other.day):
            return False
        if(other.start<=self.start<other.end or self.start<=other.start<self.end):
            # print('conflict:')
            # print(self)
            # print(other)
            # print('----------')
            return True
        # print('correct:')
        # print(self)
        # print(other)
        # print('----------')
        return False
    def getDelta(self,other):
        return other - self
    def __str__(self):
        return f'{self.name} {self.teacher} {self.day} {self.start.strftime("%H:%M")}-{self.end.strftime("%H:%M")}'

class Plan:
    def __init__(self,lessons:list[Lesson]) -> None:
        self.days = set()
        self.waste = timedelta()
        self.lessons = lessons
        length = len(lessons)
        for i in range(length):
            self.days.add(lessons[i].day)
            if(0<=i<=length-2 and lessons[i].day == lessons[i+1].day):
                self.waste += lessons[i+1].start - lessons[i].end
        
    def daysCount(self):
        return len(self.days)

    

for index,row in cdf.iterrows():
    myDict.setdefault(row['نام درس'],[])
    myDict[row['نام درس']].append(Lesson(row['نام درس'],row['استاد'],row['زمانبندي تشکيل کلاس']))

validPlans:list[Plan] = []

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
        temp.sort(key=lambda x:(x.day,x.start))
        validPlans.append(Plan(temp))                

validPlans.sort(key=lambda x : (x.daysCount(),x.waste))
for plan in validPlans:
    for lessons in plan.lessons:
        print(lessons)
    print(f'wasted days:{plan.daysCount()} wasted time: {plan.waste}')
    print('-------------------')