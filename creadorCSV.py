import pandas as pd
from datetime import datetime, timedelta
import time
import random
 

#df = pd.read_csv('csvTest1.csv', sep=';', index_col=0)
#print(df)

tiempo = datetime.now()
lluvia = []
milimetros = 0
data=[]
b = datetime.now()


for x in range(10):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(0, 2)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(20):
    b +=  timedelta(seconds=10)

    milimetros = random.randint(3, 15)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(40):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(16, 30)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(20):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(31, 59)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(30):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(16, 30)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(50):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(31, 59)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(60):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(60, 90)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(40):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(31, 59)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(30):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(60, 90)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)


for x in range(40):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(31, 59)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(50):
    b +=  timedelta(seconds=10)
    milimetros = random.randint(16, 30)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(30):
    b +=  timedelta(seconds=10)

    milimetros = random.randint(3, 15)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

for x in range(10):
    b +=  timedelta(seconds=10)

    milimetros = random.randint(0, 2)
    data.append(b)
    lluvia.append(milimetros)
    #time.sleep(10)

datos = {'fechas':data, 'lluvia':lluvia}

df = pd.DataFrame(datos, columns = ['fechas','lluvia'])
df.to_csv('csvLluvia.csv')


