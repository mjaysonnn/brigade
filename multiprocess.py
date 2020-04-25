import multiprocessing
import os 
import time
import sys
import csv
import time
def worker(num):
    """thread worker function"""
    print 'Worker:', num
    cmd="brig exec deis/empty-testbed -f %s > job-c1-%s.log"%(sys.argv[1],num)
    os.system(cmd)
    return

if __name__ == '__main__':
    jobs = []
    workload = open(sys.argv[1], 'r')
    line = workload.readline()
    while line:
        arrival_time = float(line.split(',')[0])
        num_tasks = int(line.split(',')[1])
        print arrival_time, num_tasks
	num = int(num_tasks/1)
        for i in range(num):
            print("request ",i," submitted at time ",time.time())
            p = multiprocessing.Process(target=worker, args=(i,))
            jobs.append(p)
            p.start()
        print("batch end time ", i ," ",time.time())
	time.sleep(1)
        line = workload.readline()
