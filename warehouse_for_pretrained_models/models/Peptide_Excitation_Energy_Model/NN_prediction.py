# -*- coding: utf-8 -*-

#使用神经网络方法预测:peptide_tran_E.txt,peptide_trans_Edip.txt

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error   
import numpy as np
from pandas import DataFrame as df
import tensorflow as tf
from sklearn import preprocessing
import sys

#定义特定后缀的文件的个数
def count_num(path,suffix):
    num=0
    for root,dirs,files in os.walk(path):
        for name in files:
            if name.endswith(suffix):
                num=num+1
    return num

#定义NN预测函数
def predict(x,model_dir,model_name):
    with tf.compat.v1.Session() as sess:
        init = tf.compat.v1.global_variables_initializer()
        sess.run(init)
    
       
        saver = tf.compat.v1.train.import_meta_graph(meta_graph_or_file=model_dir+model_name+".meta")
        saver.restore(sess,model_dir+model_name)
        graph = tf.compat.v1.get_default_graph()
    
        xs = graph.get_tensor_by_name("x_inputs:0")
        pred = graph.get_tensor_by_name("pred:0")    
        feed_dict = {xs: x}
        y_test_pred = sess.run(pred,feed_dict=feed_dict)
    
    return y_test_pred

#-----------载入内坐标,预测肽键的跃迁能----------------
#载入内坐标
peptide_gzmat=[]
with open("peptide_gzmat.txt", "r") as f:
    for line in f.readlines():
        peptide_gzmat_single = line.strip().split('\n\t')
        for str in peptide_gzmat_single:
            sub_str = str.split(',')
        if sub_str:
            peptide_gzmat.append(sub_str)
peptide_gzmat=np.array(peptide_gzmat,dtype=np.dtype(float).type).reshape(-1,9)
f.close()
#归一化
scaler= preprocessing.StandardScaler()
peptide_gzmat = scaler.fit_transform(peptide_gzmat)
#预测跃迁能
peptide_trans_Enpi = predict(x=peptide_gzmat,model_dir="./Enpi/",model_name="Enpi_gzmat")
tf.compat.v1.reset_default_graph()
peptide_trans_Epipi = predict(x=peptide_gzmat,model_dir="./Epipi/",model_name="Epipi_gzmat")
tf.compat.v1.reset_default_graph()

#把两个Enpi,Epipi交叉放到一个文件
peptide_trans_E = []
for i in range(peptide_trans_Enpi.shape[0]):
    peptide_trans_E.append(peptide_trans_Enpi[i])
    peptide_trans_E.append(peptide_trans_Epipi[i]+3.6)
peptide_trans_E=df(10000000/np.array(peptide_trans_E).reshape(-1,1))
peptide_trans_E.to_csv('peptide_trans_E_NN.txt',mode='w',header=False,index=False)
