import pymongo
import time, sched
import sys
import datetime
from load_predictor import Predictor
import pandas as pd

myclient = pymongo.MongoClient("mongodb://10.52.3.47:27017/")
mydb = myclient["mydb"]
print(mydb.list_collection_names())
jobs =  mydb["job_stats"]
containers = mydb["containers"]
POLICY = int(sys.argv[1])                                                                                                                         
EqualDivision = int(sys.argv[2])                                                                                                                  
if EqualDivision == 1:                                                                                                                            
    batchsize =[6,30,5]                                                                                                                           
else:                                                                                                                                             
    batchsize =[8,8,8]                                                                                                                            
print("&&&&&&&&&&&&&&&& POLICY",POLICY)   

def track_util():                                                                                                                                 
    print("tracking utilization.....")                                                                                                            
    numContainers = []                                                                                                                            
    idleContainers = []                                                                                                                           
    numContainers.append(len(list(containers.find({"type":{"$regex":"^asr"}}))))                                                                  
    numContainers.append(len(list(containers.find({"type":{"$regex":"^nlp"}}))))
    numContainers.append(len(list(containers.find({"type":{"$regex":"^qa"}}))))                                                                   
    i=0                                                                                                                                           
    print("number of existing containers ", numContainers)                                                                                        
    idleContainers.append(len(list(containers.find({"batchsize":"8"}))))                                                                          
    currentTime = time.time()                                                                                                                     
    toWrite = str(currentTime)+ "," + str(sum(numContainers)) + "," + str(sum(idleContainers))                                                    
    cmd = "echo %s >> containers_log"%(toWrite)                                                                                                   
    os.system(cmd)                                                                                                                                
    #return numContainers

def predict_load():
    arrivals = []
    for x in list(jobs.find()):
        arrivals.append(x['arrivalTime'])
#print(arrivals)
    predictor = Predictor(init_load=50,model_path='poisson_model_32.h5' , scaler_path='poisson_scaler.save')
    df = pd.DataFrame((arrivals),columns=['time'])
    print(df)
    df.index = pd.to_datetime(df.time, unit='s' )
    arrivalRate = df.groupby(df.index.second).count()
    print ("arrivalrate list is " , arrivalRate)
    #print("****", df.groupby(df.index.second))
    train = arrivalRate.time[-60:]
    #df.groupby(pd.Grouper(key='time', freq='1s'))
    Times = 1.5
    #train = df[-60:]
    #print train
    #X = train.time.tolist()
    y = train.tolist()
    load = max(y)
    print("*****max arrival rate is: ***** ", load, y)
    forecasts = predictor.predict(load * Times)
    print(forecasts)
    print("number of existing containers ", numContainers)                                                                                        
    idleContainers.append(len(list(containers.find({"batchsize":"8"}))))                                                                          
    currentTime = time.time()                                                                                                                     
    toWrite = str(currentTime)+ "," + str(sum(numContainers)) + "," + str(sum(idleContainers))                                                    
    cmd = "echo %s >> containers_log"%(toWrite)                                                                                                   
    os.system(cmd)  
    for i in range(len(numContainers)):                                                                                                           
        if int(numContainers[i]*batchsize[i]) < forecast:                                                                                         
            containers_needed = int((int(forecast) - int(numContainers[i]))/batchsize[i])                                                         
            print("inserting containers ", containers_needed)                                                                                     
            if (i == 0):                                                                                                                          
                contType = "asr-slackaware"                                                                                                       
            elif (i==1):                                                                                                                          
                contType = "nlp-slackaware"                                                                                                       
            else:                                                                                                                                 
                contType = "qa-slackaware"                                                                                                        
            currentTime = time.time()                                                                                                             
            for j in range (containers_needed):                                                                                                   
                contName = contType + str(currentTime).split(".")[0] + str(i) +str(j)   
                containers.insert_one({"ID":contName ,"idle":"true","type":contType,"lastUsedTime":currentTime,"batchsize":"8"}) 

def baseline_predict():                                                                                                                           
                                                                                                                                                  
    arrivals = []                                                                                                                                 
    for x in list(jobs.find()):                                                                                                                   
        arrivals.append(x['arrivalTime'])                                                                                                         
#print(arrivals)                                                                                                                                  
    predictor = Predictor(init_load=50,model_path='poisson_model_32.h5' , scaler_path='poisson_scaler.save')                                      
    df = pd.DataFrame((arrivals),columns=['time'])                                                                                                
    print(df)                                                                                                                                     
    df.index = pd.to_datetime(df.time, unit='s' )                                                                                                 
    arrivalRate = df.groupby(df.index.second).count()                                                                                             
    print ("************************\narrivalrate list is " , arrivalRate)                                                                        
    #print("****"""""", df.groupby(df.index.second))                                                                                              
    train = arrivalRate.time[-60:]                                                                                                                
    #df.groupby(pd.Grouper(key='time', freq='1s'))                                                                                                
    Times = 1.5                                                                                                                                   
    #train = df[-60:]                                                                                                                             
    #print train                                                                                                                                  
    #X = train.time.tolist()                                                                                                                      
    y = train.tolist()                                                                                                                            
    load = max(y)                                                                                                                                 
    print("*****max arrival rate is: ***** ", load, y)                                                                                            
    forecasts = predictor.predict(load * Times)                                                                                                   
    forecast = int(max(forecasts) * 0.2)                                                                                                          
    print("%%%% forecast is ", forecast)                                                                                                          
    numContainers = []                                                                                                                            
    idleContainers = []                                                                                                                           
    numContainers.append(len(list(containers.find({"type":{"$regex":"^asr"}}))))                                                                  
    numContainers.append(len(list(containers.find({"type":{"$regex":"^nlp"}}))))                                                                  
    numContainers.append(len(list(containers.find({"type":{"$regex":"^qa"}}))))                                                                   
    i=0                                                                                                                                           
    print("number of existing containers ", numContainers)                                                                                        
    idleContainers.append(len(list(containers.find({"idle":"true"}))))                                                                            
    currentTime = time.time()                                                                                                                     
    toWrite = str(currentTime)+ "," + str(numContainers) + "," + str(idleContainers)                                                              
    cmd = "echo %s >> containers_log"%(toWrite)                                                                                                   
    os.system(cmd)                                                                                                                                
    for i in range(len(numContainers)):  
        if int(numContainers[i]) < forecast:                                                                                                      
            containers_needed = int(int(forecast) - int(numContainers[i]))                                                                        
            print("inserting containers ", containers_needed)                                                                                     
            if (i == 0):                                                                                                                          
                contType = "asr-slackaware"                                                                                                       
            elif (i==1):                                                                                                                          
                contType = "nlp-slackaware"                                                                                                       
            else:                                                                                                                                 
                contType = "qa-slackaware"                                                                                                        
            currentTime = time.time() 
            for j in range (containers_needed):                                                                                                   
                contName = contType + str(currentTime).split(".")[0] + str(i) +str(j)                                                             
                containers.insert_one({"ID":contName ,"idle":"true","type":contType,"lastUsedTime":currentTime,"batchsize":"8"})
                
def recycle_containers():
    container_list = []
    for x in list(containers.find()):
        container_list.append([x['ID'],x['lastUsedTime'], x['idle']])
    print("list of containers" ,container_list)
    for container in container_list:
        if container[2] == "true" and (time.time() - container[1]) >= 2400:
            print(time.time() - container[1], container[0])
            myquery = {"ID": container[0]}
            containers.delete_one(myquery)

def monitor_event(): 
    if POLICY == 1:                                                                                                                               
        print("Swarm, Predicting load..... .")                                                                                                    
        predict_load()                                                                                                                            
    elif POLICY == 2:                                                                                                                             
        print("Slackaware no prediction.....")                                                                                                    
        track_util()                                                                                                                              
    elif POLICY == 0:                                                                                                                             
        print("baseline with load prediction.....")                                                                                               
        baseline_predict()                                                                                                                        
    print("Checking idle containers.....")                                                                                                        
    recycle_containers();                                                                                                                         
    scheduler.enter(10, 1, monitor_event) 

def container_recycle_event(): 
    print("Checking idle containers.....")
    recycle_containers();
    scheduler.enter(5, 1, container_recycle_event)


scheduler = sched.scheduler(time.time, time.sleep)
#s2 = sched.scheduler(time.time, time.sleep)
s1 = scheduler.enter(10, 1, monitor_event)
#s2 = scheduler.enter(5, 1, container_recycle_event)
#s1.run()
scheduler.run()


