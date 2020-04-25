import subprocess
import sys,os
import json
workload = open(sys.argv[1], 'r')
line = workload.readline()
with open(sys.argv[1]) as f:
    alist = [line.rstrip() for line in f]
print alist

for line in alist:
    cmd = "kubectl get pod %s -o json"%(line)
    print(line, cmd)
    output = subprocess.check_output(cmd, shell=True)
    y = json.loads(output)
    print y['status']['initContainerStatuses'][0]['state']['terminated']['startedAt']
    print y['status']['initContainerStatuses'][0]['state']['terminated']['finishedAt']
    finishTime =  y['status']['conditions'][3]['lastTransitionTime']
    startTime =  y['status']['conditions'][0]['lastTransitionTime']
    cmd="date -d %s "%(finishTime)
    cmd = cmd+"+%s"
    finishTimestamp = os.system(cmd);
    cmd="date -d %s "%(startTime)
    cmd = cmd+"+%s"
    startTimestamp = os.system(cmd);
    print(startTimestamp, finishTimestamp)

