

# LAVDNN

A lightweight vulnerability discovery method with deep neural networks (LAVDNN) is a tool for discovering vulnerbailities of source code. This tool is designed for assiting code auditing and discovering hidden flaws in open source programs.

## Introduction

LAVDNN is designed based on deep neural networks to classify the benign functions and weak functions. This tool extract function names as judgments to distinguish vulnerable functions from benign functions. It could autocatically extract function names in programs and identify vulnerable functions among them.

## Requirements

- [Keras 2.2.4](https://github.com/keras-team/keras/tree/master/keras)
- Python 3.5.4
- [scikit-learn](https://scikit-learn.org/stable/)

The dependecies could be installed with [`Anaconda`](https://www.anaconda.com/distribution/) (Anaconda3-4.1.6 is recommend). 


## Project Structure

1.  `Code`

The `Code` contains the following files:

   - `train.py`
   
This file introduces training method of LAVDNN. You could use it for train your own model. If you would like just use the model we provide, this file could be ignored.
   - `FunExtractor.py`
    
This file is used to automatically extract functions in target programs.
   - `Vectorazation.py`
   
This file is one-hot encoding method to vectorize the input.
   - `Predict_Vul.py`

This file is used to predict the vulnerable functions, the output is vulnerable function names and related weak probabilities.
   - `modelA_softmax`  `modelA_sigmoid` `modelB_softmax` `modelB_softmax`

These four files are model construction method,  you could leverage any of them to build model. 

2. `Data`

The `Data` folder contains the subolders `test_data`, which contains two files `FFmpeg-0.6.txt` and `LibTIFF-4.0.6.txt`. Which stores the extracted function names of two programs. These two files could be used to test the performance of LAVDNN.

The  `Data` folder also contains `training_data`, which provides sample of training data. But the amount of sample training data is too small to support for training the model. 

3. `Model`

The `Model` folder contains a well-trained model and a detailed description of the model. 

## Usage

This part introduces the usage of LAVDNN. To use LAVDNN, you first need function names of source code to be your dataset, which will be performed by `FunExtractor.py`. 

We provide the validation data for you to verify the performance of LAVDNN in `Data\validation_data\`. We also provide a well-trained model in `Model\model_of_BLSTM`. You could load model and leverage validation_data to verify the accuracy.

### Train 

If you want to build and train the model, you could use `train.py`. But traing data is needed firstly, which is not provided in this project.

### Test

If you want to test the performance of LAVDNN, we provide the test data in `Data\teat_data\`. We select FFmpeg 0.6 and LibTIFF 4.0.6 as test programs for test as they have been tested by many programs. 

We also provide a well-trained model in `Model\model_of_BLSTM`. You could load model and leverage test data to test the accuracy.

For example

```
python Predict_Vul.py  ../Data/test_data/FFmpeg-0.6.txt
```
