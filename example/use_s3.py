import numpy as np
import matplotlib.pyplot as plt
import os, sys

os.environ['LAV_DIR'] = '/home/sabeiro/lav/'
dL = os.listdir(os.environ['LAV_DIR']+'/src/')
sys.path = list(set(sys.path + [os.environ['LAV_DIR']+'/src/'+x for x in dL]))
import sawmill.aws_utils as a_u
import importlib

bucket = a_u.bucket_connect("dauvi")
fL = a_u.listFile(bucket,"pers/heim/h")
a_u.downFile(bucket,fL[0],"/home/sabeiro/tmp/")

importlib.reload(a_u)
img = a_u.readImg(bucket, fL[0])
plt.imshow(img);plt.show()
