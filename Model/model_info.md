# Model_info

## Introduction

This model is one of best-performance models used in LAVDNN, researchers could load it to predict vulnerable functions in any open source programs. 

## construction method

The model is construced with keras 2.2.4, and it may not useful for old version, so please make sure you have updated your keras to 2.2.4. 

The model is based on LSTM model. The first layer is `LSTM layer`, and two `BLSTM layers` are used as hidden layers. Additionally, a `dense layer` is used as output layer. 

The code of construction is as follows:

```
def buildmodel(self):
    self.model = Sequential()
    self.model.add(layers.LSTM(self.lstmunits,input_shape=(self.datalenth,self.charlenth),return_sequences=True,activation='elu'))
    for i in range(self.lstmLayerNum):
        self.model.add(Bidirectional(layers.LSTM(self.lstmunits, return_sequences=True,activation='elu',dropout=0.25)))
    self.model.add(Bidirectional(layers.LSTM(self.lstmunits)))
    self.model.add(Dense(2,activation='softmax'))
    self.model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
    self.model.summary()
```

The parameters are set as follows:

```
lstmunits=120
datalenth=50
charlenth=66
lstmLayerNum=1
```

## usage

To use this model, you need to load it.
```
model = load_model('model_of_BLSTM')
```