from keras.models import Sequential
from keras import layers
import numpy as np
from six.moves import range
import sys
import os
from keras.models import load_model
import keras
from keras.layers import LSTM
from keras.layers import Dense,Dropout,Activation
from keras.layers import TimeDistributed
from keras.layers import Bidirectional
import time
import matplotlib.pyplot as plt
from keras.utils import plot_model
from keras.layers.embeddings import Embedding

class SenseModel(object):
    def __init__(self,lstmunits,lstmLayerNum,DenseUnits,charlenth,datalenth):
        self.lstmunits =lstmunits
        self.lstmLayerNum = lstmLayerNum
        self.DenseUnits = DenseUnits
        self.charlenth = charlenth
        self.datalenth = datalenth
        self.buildmodel()


    def buildmodel(self):
        self.model = Sequential()
        self.model.add(layers.LSTM(self.lstmunits,input_shape=(self.datalenth,self.charlenth),return_sequences=True,activation="elu"))
        for i in range(self.lstmLayerNum):
            self.model.add(Bidirectional(layers.LSTM(self.lstmunits, return_sequences=True,activation="elu",dropout=0.25)))
        self.model.add(Bidirectional(layers.LSTM(self.lstmunits)))
        self.model.add(Dense(2,activation='sigmoid'))
      #  self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.summary()



    def trainModel(self,x,y,allround,epoch,batchsize,savename):

        for cur in range(0,allround):
            print ('------------------------------current round is  ',cur+1,'--------------------------------------------------')
            self.model.fit(x, y,batch_size=batchsize,epochs=epoch)
            mdname=savename+'_round_'+str(cur+1)
            self.model.save('..\\Model\\'+mdname)


if __name__ =="__main__":
    a = SenseModel(20,1,20,100,20)