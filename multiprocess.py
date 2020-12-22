import os
import sys
import threading
import time


def worker(num):
    print("""thread worker function""")
    print
    'Worker:', num
    # cmd= "pwd"
    cmd = "brig run brigadecore/empty-testbed -f %s -n brigade> 10minjob-%s.log" % (sys.argv[2], num)
    os.system(cmd)
    return


batch = 0
if __name__ == '__main__':
    jobs = []
    workload = open(sys.argv[1], 'r')
    line = workload.readline()
    while line:
        arrival_time = float(line.split(',')[0])
        num_tasks = int(line.split(',')[1])
        num = int(math.ceil(num_tasks / 5))
        print
        arrival_time, num_tasks, num
        for i in range(num):
            print("request ", i + (num * batch), " submitted at time ", time.time())
            # p = multiprocessing.Process(target=worker, args=(i*(num+1),))
            p = threading.Thread(target=worker, args=(i + (num * batch),))
            jobs.append(p)
            p.start()
        print("batch end time ", batch, " ", time.time())
        batch += 1
        time.sleep(1)
        line = workload.readline()
