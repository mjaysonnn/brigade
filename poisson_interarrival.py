#generate 10000 events with a mu of 5.0 events per unit time
import sys
import time
import os
import random
import csv
import time
from datetime import datetime
#n is the number of events to generate.
mu=1
#predict('https://github.com/dmlc/web-data/blob/master/mxnet/doc/tutorials/python/predict_image/cat.jpg?raw=true')
n=10000
#time span is n/mu
time_span=n/mu
current = time.time()
dt_object = datetime.fromtimestamp(current)
print current, dt_object
events=[]
#place n events uniformly distributed and place in array events.
for j in range(0,n):
    events.append(random.random())
#sort the array
events.sort()
#print("before events",events)
#at this point the events array contains n events distributed from
#(0.0 to 1.0). The next step is to scale the timing of all events by multiplying
#by n/mu which is the total time span of events.
for j in range(0,n)  :
    events[j]*=time_span
#print events
filename = open(sys.argv[1],"w")
wr = csv.writer(filename)
for i in events:
    filename.write(str(i))
    filename.write("\n")
"""with open(filename) as f:
    content = f.readlines()
print ("contents****",content)
for i in range(0,len(content)-1):
    print (content[i])
#print("after events",events)
for j in range(1,n):
    t = time.time()
    print(t)
    time.sleep(events[j]-events[j-1])
    os.system(content[i])
    print(time.time() - t)
    i+=1
    if(i>=10):
      i=0"""
    #os.system("aws lambda invoke --invocation-type RequestResponse --function-name mxnet-lambda-inception --region us-east-1 --log-type Tail --payload \'{\"url\": \"https://github.com/dmlc/web-data/blob/master/mxnet/doc/tutorials/python/predict_image/cat.jpg?raw=true\"}\' output_file")
#The events array now contains an array of event times which are approximate the #Poisson distribution with a mean arrival rate of mu per time interval.
#This has been tested using a chi squared test and closely approximates the
#Poisson Distribution.
