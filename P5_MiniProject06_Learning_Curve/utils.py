from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
import matplotlib.pyplot as plt 
import numpy as np 

# It is good to randomize the data before drawing Learning Curves
def randomize(X, Y):
    permutation = np.random.permutation(Y.shape[0])
    X2 = X[permutation,:]
    Y2 = Y[permutation]
    return X2, Y2

def draw_learning_curves(X, y, estimator):
    # 创建10个随机交叉验证数据集
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=2)
    # 获取训练数据集
    train_sizes = np.rint(np.linspace(10, X.shape[0]*0.8-1, 6)).astype(int)
    # 获取学习曲线数据
    sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, train_sizes=train_sizes)
    # 多个学习曲线数据计算均值和标准差
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.grid()
    # 图标注
    plt.title("Learning Curves")
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    # 学习率曲线图
    plt.plot(sizes, train_scores_mean, 'o-', color="g",
             label="Training score")
    plt.plot(sizes, test_scores_mean, 'o-', color="y",
             label="Cross-validation score")
    # 学习率曲线的标准差填充
    plt.fill_between(sizes, train_scores_mean - train_scores_std, \
        train_scores_mean + train_scores_std, alpha=0.15, color='g')
    plt.fill_between(sizes, test_scores_mean - test_scores_std, \
        test_scores_mean + test_scores_std, alpha=0.15, color='y')

    plt.legend(loc="best")

    plt.show()