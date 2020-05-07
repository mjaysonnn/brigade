import grpc
from concurrent import futures
from protocol import example_pb2
from protocol import example_pb2_grpc
import time
import datetime
import sys
def client(question):
    channel = grpc.insecure_channel('[::]:50055')
    stub = example_pb2_grpc.ExampleServiceStub(channel)
    resp = stub.Compute(example_pb2.ComputeRequest(question=question))
#    print(("request finished at", resp.answer))

arrivals = []
def main():
    #executor = futures.ThreadPoolExecutor(max_workers=10)
    print("batch start time",time.time())
    for i in range((int(sys.argv[1]) * int(sys.argv[2]))):
        time.sleep(1/float(sys.argv[2]))
        #print("request ",i," submitted at time ",time.time(), datetime.time)
	arrivals.append(time.time())
	cmd="brig exec deis/empty-testbed -f asyncjob.js > job%s.log"%(i)
        #executor.submit(client, str(cmd))
    print("batch end time ", i ," ",time.time(),cmd)
    print arrivals;
    #executor.shutdown()
    print('Exit')
    # input()


if __name__ == '__main__':
    main()
