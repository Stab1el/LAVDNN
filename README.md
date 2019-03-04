

# LAVDNN

## Introduction
A lightweight vulnerability discovery method with deep neural networks (LAVDNN) is a tool for discovering vulnerbailities of source code. This tool is designed for assiting code auditing and discovering hidden flaws in open source programs.

LAVDNN is designed based on deep neural networks to classify the benign functions and weak functions. This tool extract function names as judgments to distinguish vulnerable functions from benign functions. It could autocatically extract function names in programs and identify vulnerable functions among them.

## Requirements

- [Keras 2.2.4](https://github.com/keras-team/keras/tree/master/keras)
- Python >= 3.5
- [cntk](https://github.com/Microsoft/CNTK/wiki/CNTK-Binary-Download-and-Configuration)
- matplotlib

The dependecies could be installed with [`Anaconda`](https://www.anaconda.com/distribution/) (Anaconda3 is recommend). You could build the environment with conda virtual environment.

```
conda create --name <your_environment_name> python=3.6
activate <your_environment_name>
```
In virtual environment, you could use `pip` for other installations.

```
pip install keras
```

`cntk` is used as backend of `keras`. We prefer `cntk` rather than `tensorflow` as `cntk` is more effective and simple. You could select proper version of `cntk` according to your python version. For example

```
pip install https://cntk.ai/PythonWheel/GPU/cntk_gpu-2.6-cp36-cp36m-win_amd64.whl
```

## Project Structure

1.  `Code` 

The `Code` folder contains the following files:

   - `train.py`
   
This file introduces training method of LAVDNN, which could be used for training new models. If you prefer to use the model we provide, this file could be ignored.
   
- `FunExtractor.py`
    
This file is used to automatically extract function names in target programs which are built with C\C++ and python. 

- `Vectorazation.py`
   
This file uses one-hot encoding method to vectorize the input of neural networks.

- `Predict_Vul.py`

This file is used to predict the vulnerable functions with trained model. The output of this file are vulnerable function names and corresponding weak probabilities.

2. `Data`

The `Data` folder contains two subfolders 

- `training_data`

This folder provides sample of training data, which are `benign_functions`, `vulnerable_functions` and `noise_data`.

`benign_functions` contains benign functions extracted from six open source programs, including QEMU, ImageMagick, multidiff, lrzip, KLEE, and vim. `vulnerable_functions` contains vulnerable function names from CVE website. We extract name of vulnerable functions from the CVE entries. `noise_data` contains infinite length strings that are randomly generated, such as `caisjuo1jfhskjhk2`. Noise data could be added to benign functions dataset to increase the discriminatioin between two datasets and avoid the overfitting. 

However, the amount of training data in this folder is too small to support for training the model. We only provide sample of benign and vulnerable functions. Plenty of training data is still used in our future experiments thus not convenient to open it now. And we will upload the full training datasets later.

- `test_data`

This folder contains two files, which are `FFmpeg-0.6.txt` and `LibTIFF-4.0.6.txt`. These two files list the extracted function names of two programs FFmpeg 0.6 and LibTIFF 4.0.6. Users could leverage model to identify vulnerbale functions of them to test the performance of LAVDNN.

3. `Model`

The `Model` folder contains a well-trained model `model_of_LAVDNN` and a description file `model_info.md`. We select the best-performance model  during training and specific description of it is illustrated in `model_info.md`.

## Usage

This part introduces the usage method of LAVDNN. To use LAVDNN, you first need function names from source code to be your dataset, which will be performed by `FunExtractor.py`. 
```
python FunExtractor.py <root_dir> <output_file>
```

We provide the sample of training data for users in `Data\training_data\`. We also provide a well-trained model in `Model\model_of_LAVDNN`. You could load model and leverage test data to test the accuracy.

### Train 

If you want to build and train the model, you could use `train.py`. But plenty of traing data is needed firstly, which is not provided in this project.

```
python train.py
```

### Test

If you want to test the performance of LAVDNN, we provide the test data in `Data\teat_data\`. We select FFmpeg 0.6 and LibTIFF 4.0.6 as test programs for test as they have been tested by many programs. 

We also provide a well-trained model in `Model\model_of_LAVDNN`. You could load model and leverage test data to test the accuracy.

For example

```
python Predict_Vul.py  ../Data/test_data/FFmpeg-0.6.txt
```