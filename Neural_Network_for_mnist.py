# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 03:17:25 2020

@author: strai
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 02:55:01 2020

@author: strai
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 20:25:08 2020

@author: strai
"""
import pandas as pd
import time, sys
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


def update_progress(progress):
    barLength = 10 
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rBatches: [{0}] {1}% {2}".format("#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

# %%

file = pd.read_csv('assignment5.csv')

y = file['label']
X = file.drop(columns = ['label'])

#%%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=1)

def normalize(i):
    return i / 255

def preprocess(X_train, X_test, X_val):
    X_train = normalize(X_train.values)
    X_test = normalize(X_test.values)
    X_val = normalize(X_val.values)
    return X_train, X_test, X_val

X_train, X_test, X_val = preprocess(X_train, X_test, X_val)
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()
y_val = y_val.to_numpy()

#%%

#One hot
digits = 10
examples = y_train.shape[0]

y_train_new = np.zeros((y_train.size, y_train.max()+1))
y_train_new[np.arange(y_train.size), y_train] = 1
y_train_new = y_train_new.T


#%%
examples = y_test.shape[0]

y_test_new = np.zeros((y_test.size, y_test.max()+1))
y_test_new[np.arange(y_test.size), y_test] = 1
y_test_new = y_test_new.T

#%%
class ANN():
    
    def sigmoid(self, input_):
        return 1.0 / (1 + np.exp(-1 * input_))   
    
    def softmax(self, input_):
        return np.exp(input_) / np.sum(np.exp(input_), axis=0)


    def relu(self, input_):
        result = input_
        result[input_ < 0] = 0
        return result
    
    def compute_loss(self, y_target, y_pred):
        pw = np.power((y_target-y_pred), 2)
        return np.sum(pw)
    
    def __init__(self, X_train, y_train, X_test, y_test, X_val, y_val):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.X_val = X_val
        self.y_val = y_val
        
        
        self.val_figure_score = []
        
        self.number_of_samples = X_train.shape[1]
        self.number_of_features = X_train.shape[0]
        self.hidden_layer_nodes = 70
        self.learning_rate = 0.001
        self.batch_size = 80
        self.epochs = 20
        
        self.weights = []
        #Connections between features and first layer
        self.weights.append(np.random.randn(self.hidden_layer_nodes, self.number_of_features)*0.01)
        #Connections between outputlayer(10 classes for each digit) and hidden layer
        self.weights.append(np.random.randn(10, self.hidden_layer_nodes)*0.01)
        
        
    def update_weights(self, delta_w1, delta_w2):
        
        self.weights[1] = self.weights[1] -  delta_w2
        self.weights[0] = self.weights[0] -  delta_w1
        
        
    def forward_and_backward(self, X, y):

        ##Forwars
        #Linear regression wTx 
        output_1 = np.dot(self.weights[0], X) 
        activation_1 = self.sigmoid(output_1)
        output_2 = np.dot(self.weights[1], activation_1) 
        activation_2 = self.softmax(output_2)
        self.prediction = activation_2
        
        #Backpropagation
        #(Predicted - actual) * derivative(1 in this case)
        delta_output = activation_2 - y
        #delta_output*weights*derivative ( act1 * (1-act1) in this case - derivative of sigmoid)
        delta_hidden = np.dot(self.weights[1].T, delta_output) * activation_1 * (1 - activation_1)
        
        #Delta for weights - delta_unit * input_unit
        delta_w2 = self.learning_rate * np.dot(delta_output, activation_1.T)
        delta_w1 = self.learning_rate * np.dot(delta_hidden, X.T)
        
        self.update_weights(delta_w1, delta_w2)

    
    def forward_and_backward_for_validation(self, X, y):
        output_1 = np.dot(self.weights[0], X)
        activation_1 = self.sigmoid(output_1)
        output_2 = np.dot(self.weights[1], activation_1) 
        activation_2 = self.softmax(output_2)
        return activation_2
        
    def train(self):
        for epoch in range(self.epochs):
            batch_size = self.batch_size
            batches = int(self.number_of_samples / batch_size)
            
            for batch in range(batches):
                # time.sleep(0.05)
                update_progress(batch / batches)
                begin = batch * batch_size
                end = min(begin + batch_size, self.X_train.shape[1] - 1)
                X = self.X_train[:, begin:end]
                Y = self.y_train[:, begin:end]
                
                self.forward_and_backward(X, Y)
                
              
            self.forward_and_backward(self.X_train, self.y_train)
            train_cost = self.compute_loss(self.y_train, self.prediction)
            print(f'Epoch {epoch}, train cost {train_cost}')
            val_score = self.predict_for_val(self.X_val, self.y_val)
            print(f'Validation score: {val_score}')
            self.val_figure_score.append(val_score)
            if val_score > 0.90:
                print('Enough score')
                break
            
        
    def predict_test(self):
        self.forward_and_backward(self.X_test, self.y_test)
        predictions = np.argmax(self.prediction, axis=0)
        labels = np.argmax(self.y_test, axis=0)
        print(classification_report(predictions, labels))
        print(multilabel_confusion_matrix(labels, predictions))
        return predictions
    
        
    def predict_for_val(self, X, y):
        act = self.forward_and_backward_for_validation(X, y)
        predictions = np.argmax(act, axis=0)
        return accuracy_score(y_val, predictions)
        
        
                
# %%
ann = ANN(X_train.T, y_train_new, X_test.T, y_test_new, X_val.T, y_val)
            
    
# %%    
    
ann.train()
predictions = ann.predict_test()

epochs = list(range(len(ann.val_figure_score)))
plt.title('Validation accuracy')
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.plot(epochs, ann.val_figure_score)


              