#加载预训练的模型
import pandas as pd
import torch
import torch.nn as nn
from torch.nn import functional as F
from torch.nn import Module
from sklearn.preprocessing import StandardScaler
import pickle

excel = 'data.xlsx'
X = pd.read_excel(excel, sheet_name='metals')

f = open('norm_x.pckl', 'rb')
norm_x = pickle.load(f)
f.close()

f = open('norm_y.pckl', 'rb')
norm_y = pickle.load(f)
f.close()

X_ = norm_x.transform(X) #进行x_train的归一化

##预测d带中心
class Model(Module):
    def __init__(self):
        super(Model,self).__init__()
        self.Layer1 = nn.Linear(in_features=5,out_features=512)
        self.Layer2 = nn.Linear(in_features=512,out_features=384)
        self.Layer3 = nn.Linear(in_features=384,out_features=192)
        self.Layer4 = nn.Linear(in_features=192, out_features=5)

    def forward(self,x):
        x = F.relu(self.Layer1(x))
        x = F.relu(self.Layer2(x))
        x = F.relu(self.Layer3(x))
        x = self.Layer4(x)

        return x

premodel=torch.load('premodel.pkl')

premodel.eval()
x_=torch.Tensor(X_) #转为float32类型
y_pred_ = premodel(x_)
y_pred = y_pred_.detach().numpy()
y_pred = norm_y.inverse_transform(y_pred)
y_pred =pd.DataFrame(y_pred,columns=['G','dband_ave_2OH','dband_ave_OH','dband_med_2OH','dband_med_OH'])
y_pred.to_excel('y_predict.xlsx')
