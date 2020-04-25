import sys
import csv
workload = open(sys.argv[1], 'r')
line = workload.readline()
with open(sys.argv[1]) as f:
    alist = [line.rstrip() for line in f]
print alist[0].split(',')[0], alist[0].split(',')[1]
while line:
        #task_type = float(line.split(',')[1])
        #end_time = float(line.split(',')[3])/1000
        #start_time = line.split(',')[5]
        #arrival_time = float(line.split(',')[7])
        #waiting_time = line.split(',')[9]
        #print(arrival_time,start_time,end_time,waiting_time,task_type)
        #print line

        arrival_time = float(line.split(',')[0])
        num_tasks = float(line.split(',')[1])
        print arrival_time, num_tasks
	line = workload.readline()
