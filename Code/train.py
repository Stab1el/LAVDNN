# -*- coding: utf-8 -*-
'''An implementation of sequence to sequence learning for performing addition

Input: "535+61"
Output: "596"
Padding is handled by using a repeated sentinel character (space)

Input may optionally be inverted, shown to increase performance in many tasks in:
"Learning to Execute"
http://arxiv.org/abs/1410.4615
and
"Sequence to Sequence Learning with Neural Networks"
http://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf
Theoretically it introduces shorter term dependencies between source and target.

Two digits inverted:
+ One layer LSTM (128 HN), 5k training examples = 99% train/test accuracy in 55 epochs

Three digits inverted:
+ One layer LSTM (128 HN), 50k training examples = 99% train/test accuracy in 100 epochs

Four digits inverted:
+ One layer LSTM (128 HN), 400k training examples = 99% train/test accuracy in 20 epochs

Five digits inverted:
+ One layer LSTM (128 HN), 550k training examples = 99% train/test accuracy in 30 epochs
'''

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

#from test_dense_lstm import *
#from test_lstm_dense_2 import *
from test_lstm_dense_3 import *
#from test_dense_lstm_4 import *
'''
进行输入的矩阵转换
'''


class CharacterTable(object):
    """Given a set of characters:
    + Encode them to a one hot integer representation
    + Decode the one hot integer representation to their character output
    + Decode a vector of probabilities to their character output
    """

    def __init__(self, chars):
        """Initialize character table.

        # Arguments
            chars: Characters that can appear in the input.
        """
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, C, num_rows):
        """One hot encode given string C.

        # Arguments
            num_rows: Number of rows in the returned one hot encoding. This is
                used to keep the # of rows for each data the same.
        """
        x = np.zeros((num_rows, len(self.chars)))
        for i, c in enumerate(C):
            x[i, self.char_indices[c]] = 1
        return x

    def decode(self, x, calc_argmax=True):
        if calc_argmax:
            x = x.argmax(axis=-1)
        return ''.join(self.indices_char[x] for x in x)

# Parameters for the model and dataset.
DIGITS = 50
InputChar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890.- '
ctableInput = CharacterTable(InputChar)
##--------------------------read data from txt------------------------
f= open('CVE_10-17.txt','r')
data=f.read()
rows=data.split('\n')
data_row=[]
full_data=[]
full_kind=[]
for row in rows:
    data=row.replace(';','')
    data_row.append(data)
for row in data_row:
    if not ':' in row:
        print (row)
    data=row.split(':')[0]
    kind=row.split(':')[1]
    full_data.append(data)
    full_kind.append(kind)     # full_data 是漏洞函数，full_kind是漏洞类型
f.close()


full_data_2=[]
f= open('no_CVE.txt','r')
data=f.read()
rows=data.split('\n')
for row in rows:
    data=row.replace(';','')
    full_data_2.append(data)   #full_data_2是没有漏洞函数
f.close()
'''
f=open('random_data.txt','r')
lines=f.readlines()
for line in lines:
       data=line.replace('\n','')
       full_data_2.append(data)
f.close()
'''
# ---------------------add items to array------------------------

questions = []
seen = set()  #防止重复

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
    x[i] = ctableInput.encode(sentence, DIGITS)  # every x[i] is 54*30
x_2 = np.zeros((len(no_questions), DIGITS, len(InputChar)), dtype=np.bool)
for j, sentence in enumerate(no_questions):
    x_2[j] = ctableInput.encode(sentence, DIGITS)  # every x[i] is 54*30

# Shuffle (x, y) in unison as the later parts of x will almost all be larger
# digits.
indices = np.arange(len(x))  # [    0     1     2 ... ]
np.random.shuffle(indices)
x = x[indices]  #打乱顺序
y= np.zeros((len(questions), 2),dtype=np.bool)
for i in range(len(questions)):
    y[i][0]='true'

indices_2 = np.arange(len(x_2))  # [    0     1     2 ... ]
np.random.shuffle(indices_2)
x_2 = x_2[indices_2]  #打乱顺序


y_2= np.zeros((len(no_questions), 2),dtype=np.bool)
for j in range(len(no_questions)):
    y_2[j][1]='true'


x_train=np.concatenate((x,x_2),axis=0)
y_train=np.concatenate((y,y_2),axis=0)

indices=np.arange(len(x_train))
np.random.shuffle(indices)
print (indices)
x_train=x_train[indices]
y_train=y_train[indices]

print('Training Data:')
print(x_train.shape)
print(y_train.shape)

'''
#分开训练集和验证集
split_at = len(x_train) - len(x_train) // 2
split_at = len(x_train)
(x_train, x_val) = x_train[:split_at], x_train[split_at:]
(y_train, y_val) = y_train[:split_at], y_train[split_at:]

print('Training Data:')
print(x_train.shape)
print(y_train.shape)

print('Validation Data:')
print(x_val.shape)
print(y_val.shape)
'''


## para of lstm_dense

lstmunits=240
DenseUnits=150
lstmLayerNum=2
BATCH_SIZE = 128
allround=60
epoch=5
charlenth=len(InputChar)
datalenth=DIGITS

print('Build model...')
modelname='model_'+time.strftime('%Y_%m_%d')

a = SenseModel(lstmunits,lstmLayerNum, DenseUnits, charlenth, datalenth)
a.trainModel(x_train,y_train,allround,epoch,BATCH_SIZE,modelname)

