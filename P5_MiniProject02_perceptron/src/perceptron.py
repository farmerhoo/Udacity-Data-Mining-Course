import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
# Setting the random seed, feel free to change it and see different solutions.
np.random.seed(42)

def stepFunction(t):
    if t >= 0:
        return 1
    return 0

def prediction(X, W, b):
    return stepFunction((np.matmul(X,W)+b)[0])

# TODO: Fill in the code below to implement the perceptron trick.
# The function should receive as inputs the data X, the labels y,
# the weights W (as an array), and the bias b,
# update the weights and bias W, b, according to the perceptron algorithm,
# and return W and b.
def perceptronStep(X, y, W, b, learn_rate = 0.01):
    # Fill in code
    for i in range(len(X)):
        y_hat = prediction(X[i],W,b)
        if y[i]-y_hat == 1:
            W[0] += X[i][0]*learn_rate
            W[1] += X[i][1]*learn_rate
            b += learn_rate
        elif y[i]-y_hat == -1:
            W[0] -= X[i][0]*learn_rate
            W[1] -= X[i][1]*learn_rate
            b -= learn_rate
    return W, b
    
# This function runs the perceptron algorithm repeatedly on the dataset,
# and returns a few of the boundary lines obtained in the iterations,
# for plotting purposes.
# Feel free to play with the learning rate and the num_epochs,
# and see your results plotted below.
def trainPerceptronAlgorithm(X, y, learn_rate = 0.01, num_epochs = 25):
    x_min, x_max = min(X.T[0]), max(X.T[0])
    y_min, y_max = min(X.T[1]), max(X.T[1])
    W = np.array(np.random.rand(2,1))
    b = np.random.rand(1)[0] + x_max
    # These are the solution lines that get plotted below.
    boundary_lines = []
    for i in range(num_epochs):
        # In each epoch, we apply the perceptron step.
        W, b = perceptronStep(X, y, W, b, learn_rate)
        boundary_lines.append((-W[0]/W[1], -b/W[1]))
    return boundary_lines

def plot_model(X, y, bound_lines):
    fig = plt.figure(figsize=(10, 12))
    ax = fig.add_subplot(111)
    ax.scatter(X[np.argwhere(y==0), 0], X[np.argwhere(y==0), 1], color='r')
    ax.scatter(X[np.argwhere(y==1), 0], X[np.argwhere(y==1), 1], color='b')
    x0_min = min(X[:, 0]) - 0.1*min(X[:, 0])
    x0_max = max(X[:, 0]) + 0.1*max(X[:, 0])
    x1_min = min(X[:, 1]) - 0.1*min(X[:, 1])
    x1_max = max(X[:, 1]) + 0.1*max(X[:, 1])
    ax.set_xlim(x0_min, x0_max)
    ax.set_ylim(x1_min, x1_max)
    x0 = np.linspace(x0_min, x0_max, 100)
    for n, bound_line in enumerate(bound_lines):
        x1 = x0*bound_line[0] + bound_line[1]
        if n < len(bound_lines)-1:
            ax.plot(x0, x1, '--', color='g', alpha=0.1)
        else:
            # pass
            ax.plot(x0, x1, '-', color='k')
    plt.show()

if __name__ == '__main__':
    data = pd.read_csv("./data/data.csv")
    X = np.array(data.iloc[:,0:2])
    y = np.array(data.iloc[:, 2])
    bound_lines = trainPerceptronAlgorithm(X, y, learn_rate=0.01, num_epochs=100)
    plot_model(X, y, bound_lines)
    print(X)

