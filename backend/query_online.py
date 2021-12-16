# -*- coding: utf-8 -*-
from 图像检索__1 import VGGNet

import numpy as np
import h5py

#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import argparse

# ap = argparse.ArgumentParser()
# ap.add_argument("-query", required=True,
#                 help="Path to query which contains image to be queried")
# ap.add_argument("-index", required=True,
#                 help="Path to index")
# ap.add_argument("-result", required=True,
#                 help="Path for output retrieved images")
# args = vars(ap.parse_args())

# read in indexed images' feature vectors and corresponding image names
# h5f = h5py.File(r"D:\企查查\图像检索\index11\\images_12683.h5", 'r')
h5f = h5py.File("/home/bi/fandan_predict/download_pic/result_wushi_all.h5", 'r')
feats = h5f['dataset_1'][:]
imgNames = h5f['dataset_2'][:]
h5f.close()

print("--------------------------------------------------")
print("               searching starts")
print("--------------------------------------------------")

# read and show query image
queryDir = '/home/bi/fandan_predict/download_pic/O1CN01ddj8xo1MCmj6pqlQW_!!4046351399.jpg'
#queryImg = mpimg.imread(queryDir)
#plt.title("Query Image")
#plt.imshow(queryImg)
#plt.show()

# init VGGNet16 model
model = VGGNet()

# extract query image's feature, compute simlarity score and sort
queryVec = model.extract_feat(queryDir)
scores = np.dot(queryVec, feats.T)
rank_ID = np.argsort(scores)[::-1]
rank_score = scores[rank_ID]
# print rank_ID
# print rank_score


# number of top retrieved images to show
maxres = 15
imlist = [imgNames[index] for i, index in enumerate(rank_ID[0:maxres])]
print("top %d images in order are: " % maxres, imlist)

# show top #maxres retrieved result one by one
#for i, im in enumerate(imlist):
    # image = mpimg.imread(r'D:\企查查\图像检索\imag_vgg' + "\\" + str(im, encoding='utf-8'))
    # image = mpimg.imread(r'D:\百度入库图片\images' + "\\" + str(im, encoding='utf-8'))
 #   image = mpimg.imread('/home/bi/fandan_predict/download_pic/pic_down_white' + "/" + str(im, encoding='utf-8'))
  #  print(image)
  #  plt.title("search output %d" % (i + 1))
   # plt.imshow(image)
    #plt.show()
