

# LAVDNN

A lightweight vulnerability discovery method with deep neural networks (LAVDNN) is a tool for discovering vulnerbailities of source code. This tool is designed for assiting code auditing and discovering hidden flaws in open source programs.

## Introduction

LAVDNN is designed based on deep neural networks to classify the benign functions and weak functions. This tool extract function names as judgments to distinguish vulnerable functions from benign functions. It could autocatically extract function names in programs and identify vulnerable functions among them.

## Requirements

- Keras 2.2.4
- Python 3.5
- scikit-learn

The dependecies could be installed with `Anaconda`. For example:
```
$ bash Anaconda3-5.0.1-Linux-x86_64.sh

```

## Project Structure

1.  `Code`

The `Code` contains the following files:

   - `train.py`
   - `FunExtractor.py`
   - `Vectorazation.py`
   - `Predict_Vul.py`

2. `Data`

The `Data` folder contains two subolders:
   - `validation_data`
   - `test_data`

3. `Model`

The `Model` folder contains a well-trained model and a detailed description of the model. 

## Usage

This part introduces the usage of LAVDNN. To use LAVDNN, you first need function names of source code to be your dataset, which will be performed by `FunExtractor.py`. 

### Verifying

We provide the validation data for you to verify the performance of LAVDNN in `Data\validation_data\`. We also provide a well-trained model in `Model\model_of_BLSTM`. You could load model and leverage validation_data to verify the accuracy.

### Test

If you want to test the performance of LAVDNN, we provide the test data in `Data\teat_data\`. We use FFmpeg 0.6 and LibTIFF 4.0.6 as test programs to 