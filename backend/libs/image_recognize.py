from 图像检索__1 import VGGNet
import numpy as np
import h5py

def shibie_image(queryDir_path: str):

    h5f = h5py.File("/home/bi/fandan_predict/download_pic/result_wushi_all.h5", 'r')
    feats = h5f['dataset_1'][:]
    imgNames = h5f['dataset_2'][:]
    h5f.close()

    print("--------------------------------------------------")
    print("               searching starts")
    print("--------------------------------------------------")

    # read and show query image
    # queryDir = r'D:\企查查\图像检索\搜索图片\O1CN01lIA3B11ntpY67O3pE_!!791105148.jpg'
    queryDir = queryDir_path
    # queryImg = mpimg.imread(queryDir)
    # plt.title("Query Image")
    # plt.imshow(queryImg)
    # plt.show()

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

    maxres = 50
    imlist = [imgNames[index] for i, index in enumerate(rank_ID[0:maxres])]
    print("top %d images in order are: " % maxres, imlist)

    # show top #maxres retrieved result one by one
    aa = []
    for i, im in enumerate(imlist):
        # image = mpimg.imread(r'D:\企查查\图像检索\imag_vgg' + "\\" + str(im, encoding='utf-8'))
        # image = mpimg.imread(r'D:\百度入库图片\images' + "\\" + str(im, encoding='utf-8'))
        aa.append(im)
    return aa
   # return [
    #    b"590403990825.jpg",
     #   b"568064600180.jpg",
      #  b"571358200484.jpg",
       # b"565775009019.jpg",
       # b"588109501480.jpg",
       # b"586653210947.jpg",
       # b"590105384561.jpg",
       # b"575817862105.jpg",
       # b"581400694331.jpg",
       # b"574620348146.jpg",
    #]
