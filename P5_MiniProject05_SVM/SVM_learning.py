# 导入声名
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# 定义函数绘制模型分类边界
def plot_model(X, y, model):
    fig = plt.figure(figsize=(10, 12))
    ax = fig.add_subplot(111)
    x0_min = min(X[:, 0]) - 0.1
    x0_max = max(X[:, 0]) + 0.1
    x1_min = min(X[:, 1]) - 0.1
    x1_max = max(X[:, 1]) + 0.1
    ax.scatter(X[np.argwhere(y==0), 0], X[np.argwhere(y==0), 1], color='b', marker='o')
    ax.scatter(X[np.argwhere(y==1), 0], X[np.argwhere(y==1), 1], color='r', marker='o')
    ax.set_xlim(x0_min, x0_max)
    ax.set_ylim(x1_min, x1_max)

    x0 = np.linspace(x0_min, x0_max, 200)
    x1 = np.linspace(x1_min, x1_max, 200)
    s,t = np.meshgrid(x0, x1)
    s = np.reshape(s, (np.size(s), 1))
    t = np.reshape(t, (np.size(t), 1))
    h = np.concatenate((s, t), axis=1)

    z = model.predict(h)
    s = s.reshape((np.size(x0),np.size(x1)))
    t = t.reshape((np.size(x0),np.size(x1)))
    z = z.reshape((np.size(x0),np.size(x1)))

    ax.contourf(s,t,z,colors = ['blue','red'],alpha = 0.2,levels = range(-1,2))
    if len(np.unique(z)) > 1:
        ax.contour(s,t,z,colors = 'k', linewidths = 2)

    plt.show()

# 导入数据
data = np.array(pd.read_csv('./P5_MiniProject05_SVM/data.csv', header=None))
# 分别取出特征和标签给X和y
X = data[:, 0:2]
y = data[:, 2]

# 模型参数配置, 尝试调整C, kernel, gamma观察模型边界形状变化
model = SVC(C=10, kernel='rbf', gamma=10)

# 拟合模型
model.fit(X, y)

# 模型预测
y_pred = model.predict(X)

# 计算预测准确率
acc = accuracy_score(y, y_pred)
print("模型预测准确率为：{:.2f}".format(acc))
plot_model(X, y, model)
