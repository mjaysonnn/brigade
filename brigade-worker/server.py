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

main_session = None
sessions = None
input_ph = None
task = None


def get_graph():
    global main_session
    input_ph = tf.placeholder(tf.float64, shape=(1024, 1024))
    x = input_ph
    for i in range(1000):
        x = x * x
    print('get_graph', x.graph)
    sess = tf.Session(
        config=tf.ConfigProto(allow_soft_placement=True,
        #                       inter_op_parallelism_threads=1,
                              intra_op_parallelism_threads=1
                              ),
        graph=x.graph
    )
    sess.run(tf.global_variables_initializer())
    main_session = sess
    return input_ph, x


def new_session():
    sess = tf.Session(
        # config=tf.ConfigProto(allow_soft_placement=True,
        #                       inter_op_parallelism_threads=1,
        #                       intra_op_parallelism_threads=1
        #                       ),
        graph=task.graph,
    )
    # sess.run(tf.global_variables_initializer())
    return sess
import mxnet as mx
import sys 
import time 
import os
import random
path='http://data.mxnet.io/models/imagenet'
[mx.test_utils.download(path+ sys.argv[1]),
 mx.test_utils.download(path+ sys.argv[2]),
 mx.test_utils.download(path+ sys.argv[3])]
ctx = mx.cpu()
sym, arg_params, aux_params = mx.model.load_checkpoint(sys.argv[4], 0)
mod = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
mod.bind(for_training=False, data_shapes=[('data', (1,3,224,224))],
         label_shapes=mod._label_shapes)
mod.set_params(arg_params, aux_params, allow_missing=True)
with open('synset.txt', 'r') as f:
    labels = [l.rstrip() for l in f]
#import matplotlib.pyplot as plt
import numpy as np
# define a simple data batch
from collections import namedtuple
Batch = namedtuple('Batch', ['data'])

def get_image(url, show=False):
    # download and show the image
    fname = mx.test_utils.download(url)
    img = mx.image.imread(fname)
    if img is None:
        return None
    #if show:
     #   plt.imshow(img.asnumpy())
      #  plt.axis('off')
    # convert into format (batch, RGB, width, height)
    img = mx.image.imresize(img, 224, 224) # resize
    img = img.transpose((2, 0, 1)) # Channel first
    img = img.expand_dims(axis=0) # batchify
    return img

def predict(url):
    img = get_image(url, show=True)
    # compute the predict probabilities
    mod.forward(Batch([img]))
    prob = mod.get_outputs()[0].asnumpy()
    # print the top-5
    prob = np.squeeze(prob)
    a = np.argsort(prob)[::-1]
    for i in a[0:5]:
        print('probability=%f, class=%s' %(prob[i], labels[i]))


class ExampleServer(protocol.example_pb2_grpc.ExampleServiceServicer):

    def Compute(self, request, context):
        print("query accept time ", time.time())
        global main_session
        question = request.question
   #     print('accept {}'.format(question))
        # sess = sessions[current_thread().name]
        sess = main_session
        x = np.random.rand(1024, 1024)
        #ret = sess.run(task, feed_dict={input_ph: x})
    #    print("current_thread: {}, question: {}".format(current_thread().name, question))

        #predict(question)
        os.system(question)
        print("query respone time ", time.time())
        return protocol.example_pb2.ComputeResponse(answer=str(time.time()))


def serve():
    global sessions, input_ph, task
    sessions = defaultdict(new_session)
    print('Building graph')
    #input_ph, task = get_graph()
    print('Finish Build graph')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    protocol.example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleServer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
