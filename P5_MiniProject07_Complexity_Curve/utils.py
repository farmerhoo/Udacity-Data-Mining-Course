from sklearn.model_selection import validation_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import make_scorer
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt 
import numpy as np 

# It is good to randomize the data before drawing Learning Curves
def randomize(X, Y):
    permutation = np.random.permutation(Y.shape[0])
    X2 = X[permutation,:]
    Y2 = Y[permutation]
    return X2, Y2

def draw_validation_curves(X, y, estimator):
    # 创建10个随机交叉验证数据集
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=2)
    # 决策树算法的最大树深度
    max_depth = np.arange(1,9)
    # make_scorer
    scorer = make_scorer(f1_score)
    # 获取复杂度曲线
    train_scores, test_scores = validation_curve(estimator, X, y, \
        param_name = "max_depth", param_range = max_depth, cv = cv, scoring = 'r2')
    # 多个复杂度曲线数据计算均值和标准差
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    plt.grid()
    # 图标注
    plt.title("Complecity Curves")
    plt.xlabel("Maximum depth")
    plt.ylabel("Score")
    # 学习率曲线图
    plt.plot(max_depth, train_mean, 'o-', color="g",
             label="Training score")
    plt.plot(max_depth, test_mean, 'o-', color="y",
             label="Test score")
    # 学习率曲线的标准差填充
    plt.fill_between(max_depth, train_mean - train_std, \
        train_mean + train_std, alpha=0.15, color='g')
    plt.fill_between(max_depth, test_mean - test_std, \
        test_mean + test_std, alpha=0.15, color='y')

    plt.legend(loc="best")

    plt.show()