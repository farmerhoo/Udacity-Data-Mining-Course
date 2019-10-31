# Import, read, and split data
import pandas as pd
import numpy as np

data = pd.read_csv('./P5_MiniProject07_Complexity_Curve/data.csv')

X = np.array(data[['x1', 'x2']])
y = np.array(data['y'])

# Fix random seed
np.random.seed(55)

### Imports
from sklearn.ensemble import GradientBoostingClassifier

import sys 
sys.path.append("./P5_MiniProject07_Complexity_Curve")
from utils import draw_validation_curves

### 绘制复杂度曲线
estimator = GradientBoostingClassifier()
draw_validation_curves(X, y, estimator)
