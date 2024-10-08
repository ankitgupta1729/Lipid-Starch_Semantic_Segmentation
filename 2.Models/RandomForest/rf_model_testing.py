#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 23:19:52 2024

@author: ankit
"""

###############################################################
#STEP 7: MAKE PREDICTION ON NEW IMAGES
################################################################ 
import numpy as np
import cv2
import pandas as pd
from skimage.filters import roberts, sobel, scharr, prewitt
import pickle
from matplotlib import pyplot as plt
from scipy import ndimage as nd
import os
 
def feature_extraction(img):
    df = pd.DataFrame()
    # All features generated must match the way features are generated for TRAINING.
    # Feature1 is our original image pixels
    #img = cv2.resize(img, (128,128))
    img2 = img.reshape(-1)
    df['Pixel_Value'] = img2

    #Generate Gabor features
    num = 1
    kernels = []
    for theta in range(2):
        theta = theta / 4. * np.pi
        for sigma in (1, 3):
            for lamda in np.arange(0, np.pi, np.pi / 4):
                for gamma in (0.05, 0.5):
                #print(theta, sigma, , lamda, frequency)
                    gabor_label = 'Gabor' + str(num)
                    # print(gabor_label)
                    ksize=9
                    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)    
                    kernels.append(kernel)
                    #Now filter image and add values to new column
                    fimg = cv2.filter2D(img2, cv2.CV_8UC3, kernel)
                    filtered_img = fimg.reshape(-1)
                    df[gabor_label] = filtered_img  #Modify this to add new column for each gabor
                    num += 1
    ########################################
    #Geerate OTHER FEATURES and add them to the data frame
    #Feature 3 is canny edge
    edges = cv2.Canny(img, 100,200)   #Image, min and max values
    edges1 = edges.reshape(-1)
    df['Canny Edge'] = edges1 #Add column to original dataframe

    #Feature 4 is Roberts edge
    edge_roberts = roberts(img)
    edge_roberts1 = edge_roberts.reshape(-1)
    df['Roberts'] = edge_roberts1

    #Feature 5 is Sobel
    edge_sobel = sobel(img)
    edge_sobel1 = edge_sobel.reshape(-1)
    df['Sobel'] = edge_sobel1

    #Feature 6 is Scharr
    edge_scharr = scharr(img)
    edge_scharr1 = edge_scharr.reshape(-1)
    df['Scharr'] = edge_scharr1

    #Feature 7 is Prewitt
    edge_prewitt = prewitt(img)
    edge_prewitt1 = edge_prewitt.reshape(-1)
    df['Prewitt'] = edge_prewitt1

    #Feature 8 is Gaussian with sigma=3
    gaussian_img = nd.gaussian_filter(img, sigma=3)
    gaussian_img1 = gaussian_img.reshape(-1)
    df['Gaussian s3'] = gaussian_img1

    #Feature 9 is Gaussian with sigma=7
    gaussian_img2 = nd.gaussian_filter(img, sigma=7)
    gaussian_img3 = gaussian_img2.reshape(-1)
    df['Gaussian s7'] = gaussian_img3

    #Feature 10 is Median with sigma=3
    median_img = nd.median_filter(img, size=3)
    median_img1 = median_img.reshape(-1)
    df['Median s3'] = median_img1

    #Feature 11 is Variance with size=3
    variance_img = nd.generic_filter(img, np.var, size=3)
    variance_img1 = variance_img.reshape(-1)
    df['Variance s3'] = variance_img1  #Add column to original dataframe


    return df


#########################################################

#Applying trained model to segment multiple files. 



filename = "2.Models/RandomForest/rf_model"
loaded_model = pickle.load(open(filename, 'rb'))

path = "2.Models/RandomForest/images/test_images/"

for image in os.listdir(path):  #iterate through each file to perform some action
    print(image)
    img1= cv2.imread(path+image)
    img1 = cv2.resize(img1, (128,128))
    img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    #Call the feature extraction function.
    X = feature_extraction(img)
    result = loaded_model.predict(X)
    segmented = result.reshape((img.shape))
    
    plt.imsave('2.Models/RandomForest/images/segmented/'+image, segmented, cmap ='jet')
    
    
    
    
    
    