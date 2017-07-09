#coding=utf-8
import cv2
import numpy as np

from matplotlib import pyplot as plt
import scipy.ndimage.filters as f
import scipy

import time
import scipy.signal as l





from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras import backend as K

K.set_image_dim_ordering('tf')


def Getmodel_tensorflow(nb_classes):
    # nb_classes = len(charset)
    img_rows, img_cols = 23, 23
    # number of convolutional filters to use
    nb_filters = 16
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 3
    # x = np.load('x.npy')
    # y = np_utils.to_categorical(range(3062)*45*5*2, nb_classes)
    # weight = ((type_class - np.arange(type_class)) / type_class + 1) ** 3
    # weight = dict(zip(range(3063), weight / weight.mean()))  # 调整权重，高频字优先

    model = Sequential()
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv,
                            border_mode='valid',
                            input_shape=(img_rows, img_cols,1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Flatten())
    model.add(Dense(256))
    model.add(Dropout(0.5))

    model.add(Activation('relu'))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])
    return model



model  = Getmodel_tensorflow(3)
import os
model.load_weights("./model/char_judgement.h5")

def get_median(data):
   data = sorted(data)
   size = len(data)
   # print size

   if size % 2 == 0: # 判断列表长度为偶数
    median = (data[size//2]+data[size//2-1])/2
    data[0] = median
   if size % 2 == 1: # 判断列表长度为奇数
    median = data[(size-1)//2]
    data[0] = median
   return data[0]

def searchOptimalCuttingPoint(rgb,res_map,start,width_boundingbox,interval_range):
    #
    # for x in xrange(10):
    #     res_map = np.vstack((res_map,res_map[-1]))
    length = res_map.shape[0]
    refine_s = -2;

    if width_boundingbox>20:
        refine_s = -9



    score_list = []
    interval_big = int(width_boundingbox * 0.3)  #

    for zero_add in xrange(start,start+50):
        # for interval_small in xrange(-0,width_boundingbox/2):
            for i in xrange(-8,int(width_boundingbox/1)-8):
                for refine in xrange(refine_s,width_boundingbox/2+10):


                    p1 = zero_add# this point is province
                    p2 = p1 + width_boundingbox +refine #
                    p3 = p2 + width_boundingbox + interval_big+i+1
                    p4 = p3 + width_boundingbox +refine
                    p5 = p4 + width_boundingbox +refine
                    p6 = p5 + width_boundingbox +refine
                    p7 = p6 + width_boundingbox +refine

                    list  = [p1,p2,p3,p4,p5,p6,p7]
                    # bak = rgb.copy()
                    #
                    # #
                    # for one in list:
                    #     cv2.line(bak,(one,1),(one,36),255)
                    # cv2.imshow("imag", bak)
                    # cv2.waitKey(0)
                    if p7>=length:

                        # print"break"
                        # print p7
                        continue
                        # score_list = sorted(score_list, key=lambda x: x[0])
                        # return score_list[0]

                    score = res_map[p1][2]*3 -(res_map[p3][1]+res_map[p4][1]+res_map[p5][1]+res_map[p6][1]+res_map[p7][1])+7
                    # print score
                    score_list.append([score,[p1,p2,p3,p4,p5,p6,p7]])

    score_list = sorted(score_list , key=lambda x:x[0])
    # debug = cv2.cvtColor(rgb,cv2.COLOR_GRAY2RGB)
    # for one in score_list[-1][1]:
    #     cv2.line(debug,(one,0),(one,36),(255,0,0),1)
    # #
    # cv2.imshow("one",debug)
    # cv2.waitKey(0)

    return score_list[-1]


import sys

sys.path.append('../')
import recognizer as cRP
from skimage.filters import (threshold_otsu, threshold_niblack,
                             threshold_sauvola)

def refineCrop(sections,width=16):
    new_sections = []
    for section in sections:
        # cv2.imshow("section¡",section)

        cv2.blur(section,(3,3),3)

        sec_center = np.array([section.shape[1]/2,section.shape[0]/2])
        thresh_niblack = threshold_niblack(section, window_size=17, k=-0.2.2)
        binary_niblack = section > thresh_niblack
        binary_niblack = binary_niblack.astype(np.uint8) * 255
        imagex, contours, hierarchy  = cv2.findContours(binary_niblack,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        boxs = []
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)

            ratio = w/float(h)
            if ratio<1 and h>36*0.4 and y<16\
                    :
                box = [x,y,w,h]

                boxs.append([box,np.array([x+w/2,y+h/2])])
                # cv2.rectangle(section,(x,y),(x+w,y+h),255,1)




        # print boxs

        dis_ = np.array([ ((one[1]-sec_center)**2).sum() for one in boxs])
        if len(dis_)==0:
            kernal = [0, 0, section.shape[1], section.shape[0]]
        else:
            kernal = boxs[dis_.argmin()][0]

        center_c  = (kernal[0]+kernal[2]/2,kernal[1]+kernal[3]/2)
        w_2 = int(width/2)
        h_2 = kernal[3]/2

        if center_c[0] - w_2< 0:
            w_2 = center_c[0]
        new_box = [center_c[0] - w_2,kernal[1],width,kernal[3]]
        # print new_box[2]/float(new_box[3])
        if new_box[2]/float(new_box[3])>0.6:
            # print "异常"
            h = int((new_box[2]/0.35 )/2)
            if h>35:
                h = 35
            new_box[1] = center_c[1]- h
            if new_box[1]<0:
                new_box[1] = 1

            new_box[3] = h*2








        section  = section[new_box[1]:new_box[1]+new_box[3],new_box[0]:new_box[0]+new_box[2]]
        # cv2.imshow("section",section)
        # cv2.waitKey(0)
        new_sections.append(section)
        # print new_box


    return new_sections





def slidingWindowsEval(image):
    windows_size = 16;
    stride = 1
    height= image.shape[0]
    # print image.shape[1]
    p = []
    ch_p = []

    gain = []
    pin=[]
    for i in range(0,image.shape[1]-windows_size+1,stride):
        data = image[0:height,i:i+windows_size]
        data = cv2.resize(data,(23,23))
        # cv2.imshow("image",data)
        data = cv2.equalizeHist(data)
        data = data.astype(np.float)/255
        data=  np.expand_dims(data,3)
        res = model.predict(np.array([data]))
        pin.append(res[0])

        p.append(res[0][0]+res[0][2])
        ch_p.append(res[0][2])

        gain.append(res.argmax())

    p =  np.insert(p,0,0);
    p = np.insert(p,len(p),0);
    p = f.gaussian_filter1d(np.array(p,dtype=np.float),3)
    # print p
    sum = image.sum(axis=0)


    lmin = l.argrelmax(np.array(p),order = 3)[0]
    interval = []
    for i in xrange(len(lmin)-1):
        interval.append(lmin[i+1]-lmin[i])

    if(len(interval)>3):
        mid  = get_median(interval)
    else:
        return []

    ch_p = np.array(ch_p)
    pin = np.array(pin)
    res =  searchOptimalCuttingPoint(image,pin,0,mid,3)

    cutting_pts = res[1]
    last =  cutting_pts[-1] + mid
    if last < image.shape[1]:
        cutting_pts.append(last)
    else:
        cutting_pts.append(image.shape[1]-1)


    name = ""
    confidence =0.00;
    seg_block = []
    for x in xrange(1,len(cutting_pts)):
        if x != len(cutting_pts)-1 and x!=1:
            section = image[0:36,cutting_pts[x-1]-2:cutting_pts[x]+2]
        elif  x==1:

            c_head = cutting_pts[x - 1]- 2
            if c_head<0:
                c_head=0
            c_tail = cutting_pts[x] + 2

            section = image[0:36, c_head:c_tail]
        elif x==len(cutting_pts)-1:
            end = cutting_pts[x]
            diff = image.shape[1]-end

            c_head = cutting_pts[x - 1]
            c_tail = cutting_pts[x]

            if diff<7 :
                section = image[0:36, c_head-5:c_tail+5]

            else:
                diff-=1

                section = image[0:36, c_head - diff:c_tail + diff]



        elif  x==2:
            section = image[0:36, cutting_pts[x - 1] - 3:cutting_pts[x-1]+ mid]
        else:
            section = image[0:36,cutting_pts[x-1]:cutting_pts[x]]
        seg_block.append(section)
    refined = refineCrop(seg_block,mid-1)
    for i,one in enumerate(refined):


        res_pre = cRP.SimplePredict(one, i )
        confidence+=res_pre[0]

        name+= res_pre[1]

    return seg_block,name,confidence
