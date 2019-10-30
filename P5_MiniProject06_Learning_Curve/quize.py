# Import, read, and split data
import pandas as pd
import numpy as np

data = pd.read_csv('./P5_MiniProject06_Learning_Curve/data.csv')

X = np.array(data[['x1', 'x2']])
y = np.array(data['y'])

# Fix random seed
np.random.seed(55)

### Imports
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC

import sys 
sys.path.append("./P5_MiniProject06_Learning_Curve")
from utils import draw_learning_curves

# TODO: 尝试以下三个模型，观察每个模型的学习率曲线

### Logistic Regression
estimator = LogisticRegression()
draw_learning_curves(X, y, estimator)

### Decision Tree
# estimator = GradientBoostingClassifier()
# draw_learning_curves(X, y, estimator)

### Support Vector Machine
# estimator = SVC(kernel='rbf', gamma=1000)
# draw_learning_curves(X, y, estimator)
