import multiprocessing
import threading
import os 
import time
import sys
import csv 
import time
import pandas as pd
def worker(num):
    """thread worker function"""
    print 'Worker:', num
    #cmd= "pwd"
    cmd="brig exec deis/empty-testbed -f %s > 10minjob-%s.log"%(sys.argv[2],num)
    os.system(cmd)
    return
batch=0
if __name__ == '__main__':
    jobs = []
# Create a dataframe from csv
    df = pd.read_csv(sys.argv[1], delimiter=',')
# User list comprehension to create a list of lists from Dataframe rows
    list_of_rows = [list(row) for row in df.values]
# Print list of lists i.e. rows
    print(list_of_rows[1][0])
    for line in list_of_rows:
	if batch <=300:
            #arrival_time = float(line.split(',')[0])
            arrival_time = line[1]
            time.sleep(arrival_time + 1)
            #cmd="pwd"
	    cmd="brig exec deis/empty-testbed -f %s &"%(sys.argv[2])
            os.system(cmd)
          #num_tasks = int(line.split(',')[1])
          #print arrival_time, num_tasks
	#num = int(num_tasks/10)
        #for i in range(num):
            print("request ", batch, " submitted at time ",time.time())
            #p = multiprocessing.Process(target=worker, args=(i*(num+1),))
            #p = threading.Thread(target=worker, args=(i+(num * batch),))
	    jobs.append(line)
        #    p.start()
        #print("batch end time ",batch," ",time.time())
	    batch+=1
	#time.sleep(1)
        #line = workload.readline()"""
