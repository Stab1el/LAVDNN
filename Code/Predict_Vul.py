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
import datetime
from Vectorization import *

file_name = sys.argv[1]

# Parameters for the model and dataset.
DIGITS = 50
InputChar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890.- '

##--------------------------read data ------------------------
f= open(file_name,'r')   # Read data from txt file, you could select the praograms as you like

data=f.read()
rows=data.split('\n')
full_data_2=[]
for row in rows:
    data=row.replace(';','')
    full_data_2.append(data)

# ---------------------add items to array------------------------
no_questions=[]
seen_2=set()
for q in full_data_2:
    if q in seen_2:
        continue
    seen_2.add(q)
    query = q + ' ' * (DIGITS - len(q))
    no_questions.append(query)

##-----------------Vectorization ----------------------------------
ctableInput = CharacterTable(InputChar)
vec_word = np.zeros((len(no_questions), DIGITS, len(InputChar)), dtype=np.bool)
for j, sentence in enumerate(no_questions):
    vec_word[j] = ctableInput.encode(sentence, DIGITS)

##----------------Prediction with model --------------------------------
model_info='..\\Model\\model_of_LAVDNN'   # The well-trained model we provide
model = load_model(model_info)
print('Predict vulnerable functions...')
#preds_class_no=model.predict_classes(vec_word)
preds=model.predict(vec_word)

## ----------------- output -----------------------------------
count_num=0
for i in range(1,len(preds)):
    if preds[i][0]>0.55:
        print (no_questions[i],preds[i][0])
        count_num=count_num+1
print("------------------------------------------------------------")
print ("The amount of vulnerble functions are",count_num)


