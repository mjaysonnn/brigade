import grpc
import time

from concurrent import futures
from threading import current_thread
from collections import defaultdict

#import tensorflow as tf
import numpy as np
import os

import protocol.example_pb2
import protocol.example_pb2_grpc

import mxnet as mx
import sys
import time
import os
import random
class ExampleServer(protocol.example_pb2_grpc.ExampleServiceServicer):

    def Compute(self, request, context):
        print("query accept time ", time.time(), request.question)
 #       global main_session
        question = request.question
   #     print('accept {}'.format(question))
        # sess = sessions[current_thread().name]
        #sess = main_session
        #x = np.random.rand(1024, 1024)
        #ret = sess.run(task, feed_dict={input_ph: x})
    #    print("current_thread: {}, question: {}".format(current_thread().name, question))

        #predict(question)
        os.system(question)
        print("query respone time ", question, time.time())
        return protocol.example_pb2.ComputeResponse(answer=str(time.time()))


def serve():
    global sessions, input_ph, task
    #sessions = defaultdict(new_session)
    print('Building graph')
    #input_ph, task = get_graph()
    print('Finish Build graph')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    protocol.example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleServer(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
