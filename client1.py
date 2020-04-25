import grpc
from concurrent import futures
from protocol import example_pb2
from protocol import example_pb2_grpc
import time
import sys
def client(question):
    channel = grpc.insecure_channel('[::]:50056')
    stub = example_pb2_grpc.ExampleServiceStub(channel)
    resp = stub.Compute(example_pb2.ComputeRequest(question=question))
#    print(("request finished at", resp.answer))


def main():
    executor = futures.ThreadPoolExecutor(max_workers=10)
    print("batch start time",time.time())
    for i in range((int(sys.argv[1]) * int(sys.argv[2]))):
        time.sleep(1/float(sys.argv[2]))
        print("request ",i," submitted at time ",time.time())
       # cmd = "aws lambda invoke --invocation-type RequestResponse --function-name %s --region us-east-1 --payload \'{\"url\": \"https://s3.amazonaws.com/mxnet-tests/images/dog3.jpg\"}\' output_file "%(sys.argv[3])
        #cmd = "https://s3.amazonaws.com/mxnet-tests/images/dog3.jpg"
        cmd="brig exec deis/empty-testbed -f asyncjob.js > job-c2-%s.log"%(i)
	#print cmd
        executor.submit(client, str(cmd))
    print("batch end time ", i ," ",time.time(),cmd)
    executor.shutdown()
    print('Exit')
    # input()


if __name__ == '__main__':
    main()
