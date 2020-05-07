import subprocess,commands
import sys,os
import json
workload = open(sys.argv[1], 'r')
line = workload.readline()
with open(sys.argv[1]) as f:
    alist = [line.rstrip() for line in f]
#print alist
running_time = []
job_running_time = []
coldstarts = 0
for line in alist:
    cmd = "kubectl get pod %s -o json"%(line)
    print(line, cmd)
    output = subprocess.check_output(cmd, shell=True)
    y = json.loads(output)
    jobStart = y['status']['startTime']
    if "terminated" in y['status']['containerStatuses'][0]['state'].keys():
        jobEnd =  y['status']['containerStatuses'][0]['state']['terminated']['finishedAt']
    startTime =  y['status']['conditions'][1]['lastTransitionTime']
    finishTime =  y['status']['conditions'][0]['lastTransitionTime']
    if y['spec']['containers'][0]['imagePullPolicy'] == "Always":
	coldstarts+=1
    cmd="date -d %s "%(startTime)
    cmd = cmd+"+%s"
    status, startTimestamp = commands.getstatusoutput(cmd)

    cmd="date -d %s "%(finishTime)
    cmd = cmd+"+%s"
    status, finishTimestamp = commands.getstatusoutput(cmd)

    cmd="date -d %s "%(jobStart)
    cmd = cmd+"+%s"
    status, jobStartTimestamp = commands.getstatusoutput(cmd)

    cmd="date -d %s "%(jobEnd)
    cmd = cmd+"+%s"
    status, jobEndTimestamp = commands.getstatusoutput(cmd)

    running_time.append(int(finishTimestamp) - int(startTimestamp))
    job_running_time.append(int(jobEndTimestamp) - int(jobStartTimestamp))
    
    print(int(finishTimestamp) - int(startTimestamp), startTimestamp, finishTimestamp)

count = len([i for i in job_running_time  if i > 10]) 
colds = len([i for i in running_time  if i <= 6]) 
print(running_time)
print("*************************************")
print(job_running_time)
print(coldstarts, count, len(job_running_time), colds, len(running_time))
