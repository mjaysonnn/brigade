import time 
import sys
import datetime
from load_predictor import Predictor
import pandas as pd

arrivals = []
for i in range((int(sys.argv[1]) * int(sys.argv[2]))):
    time.sleep(1/float(sys.argv[2]))
    arrivals.append([i,time.time()])
    cmd="brig exec deis/empty-testbed -f asyncjob.js > job%s.log"%(i)
 

predictor = Predictor(init_load=50,model_path='poisson_model_32.h5' , scaler_path='poisson_scaler.save')
print(arrivals)
df = pd.DataFrame((arrivals),columns=['pos','time'])
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
