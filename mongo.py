import pymongo
import time 
import sys
import datetime
from load_predictor import Predictor
import pandas as pd


myclient = pymongo.MongoClient("mongodb://10.52.3.47:27017/")

mydb = myclient["mydb"]
print(mydb.list_collection_names())
mycol = mydb["job_stats"]
arrivals = []
for x in list(mycol.find()):
    arrivals.append(x['arrivalTime'])
print(arrivals)

predictor = Predictor(init_load=50,model_path='poisson_model_32.h5' , scaler_path='poisson_scaler.save')

df = pd.DataFrame((arrivals),columns=['time'])
print(df)
df.index = pd.to_datetime(df.time, unit='s' )
arrivalRate = df.groupby(df.index.second).count()
#print ("arrivalrate list is " , arrivalRate)
#print("****", df.groupby(df.index.second))
y = arrivalRate.time.tolist()
print(y)
#df.groupby(pd.Grouper(key='time', freq='1s'))
Times = 1.5
#train = df[-60:]
#print train
#	X = train.time.tolist()
#	y = train.req.tolist()
load = max(y)

forecasts = predictor.predict(load * Times)
print(forecasts)
