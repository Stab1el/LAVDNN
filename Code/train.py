# -*- coding: utf-8 -*-


from __future__ import print_function
from keras.models import Sequential
from keras import layers
import numpy as np
from six.moves import range
import sys
import os
from keras.models import load_model
import keras
import os
import time
from Vectorization import *   # import one-hot encoding method

from modelB_sigmoid import *  # we build four kinds of models and we use model B with sigmoid.



DIGITS = 50
InputChar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890.- '
ctableInput = CharacterTable(InputChar)

#--------------------------------------para of lstm_dense(could be adjusted) -----------------

lstmunits=240
DenseUnits=150
lstmLayerNum=2
BATCH_SIZE = 64
allround=60
epoch=5
charlenth=len(InputChar)
datalenth=DIGITS

##--------------------------Datasets------------------------
f= open('..\\Data\\training_data\\vulnerable_functions.txt','r')
data=f.read()
rows=data.split('\n')
data_row=[]
full_data=[]
full_kind=[]
for row in rows:
    data=row.replace(';','')
    data_row.append(data)
for row in data_row:
    data=row.split(':')[0]
    full_data.append(data)
f.close()

full_data_2=[]
f= open('..\\Data\\training_data\\benign_functions.txt','r')
data=f.read()
rows=data.split('\n')
for row in rows:
    data=row.replace(';','')
    full_data_2.append(data)   #full_data_2是没有漏洞函数
f.close()


f=open('..\\Data\\training_data\\noise_data.txt','r')
lines=f.readlines()
for line in lines:
       data=line.replace('\n','')
       full_data_2.append(data)
f.close()


# ---------------------add items to array------------------------
questions = []
seen = set()

for q in full_data:
    if q in seen:
        continue
    seen.add(q)
    query = q + ' ' * (DIGITS - len(q))
    questions.append(query)
print('Total items with questions are:', len(questions))

no_questions=[]
seen_2=set()
for q in full_data_2:
    if q in seen_2:
        continue
    seen_2.add(q)
    query = q + ' ' * (DIGITS - len(q))
    no_questions.append(query)
print('Total items without questions are:', len(no_questions))
print('Total items are:', len(questions)+len(no_questions))

##----------------- one-hot code----------------------------------
print('Vectorization...')
x = np.zeros((len(questions), DIGITS, len(InputChar)), dtype=np.bool)
for i, sentence in enumerate(questions):
    x[i] = ctableInput.encode(sentence, DIGITS)
x_2 = np.zeros((len(no_questions), DIGITS, len(InputChar)), dtype=np.bool)
for j, sentence in enumerate(no_questions):
    x_2[j] = ctableInput.encode(sentence, DIGITS)


indices = np.arange(len(x))  # [    0     1     2 ... ]
np.random.shuffle(indices)
x = x[indices]
y= np.zeros((len(questions), 2),dtype=np.bool)
for i in range(len(questions)):
    y[i][0]='true'

indices_2 = np.arange(len(x_2))  # [    0     1     2 ... ]
np.random.shuffle(indices_2)
x_2 = x_2[indices_2]
y_2= np.zeros((len(no_questions), 2),dtype=np.bool)
for j in range(len(no_questions)):
    y_2[j][1]='true'

x_train=np.concatenate((x,x_2),axis=0)
y_train=np.concatenate((y,y_2),axis=0)

indices=np.arange(len(x_train))
np.random.shuffle(indices)
x_train=x_train[indices]
y_train=y_train[indices]


#-------------------------------------Build model and traning-----------------------------
print('Build model...')
modelname='model_'+time.strftime('%Y_%m_%d')
M = SenseModel(lstmunits,lstmLayerNum, DenseUnits, charlenth, datalenth)
M.trainModel(x_train,y_train,allround,epoch,BATCH_SIZE,modelname)

