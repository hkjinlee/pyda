# -*- coding: utf-8 -*-

from sklearn import datasets, svm
import pandas as pd
import numpy as np

'''
iris 데이터셋: 총 150개, 4개 컬럼
'''
iris = datasets.load_iris()
iris.data
iris.data.shape
iris.target.shape

'''
SVM 학습
- gamma와 C는 임의의 값임.
- 총 150개 가운데 142개에 대해 정확한 값이 나옴
'''
clf = svm.SVC(gamma=0.0001, C=100.)
clf.fit(iris.data, iris.target)

pred = clf.predict(iris.data)
sum(iris.target == pred)

'''
위의 결과는 training set을 그대로 test set으로 사용한 결과. (일종의 cheating)
training set과 test set을 8:2로 분할하여 다시 훈련
'''
from sklearn.model_selection import train_test_split

data, target = {}, {}
data['train'], data['test'], target['train'], target['test'] = \
     train_test_split(iris.data, iris.target, test_size=.2)
clf.fit(data['train'], target['train'])

pred = clf.predict(data['train'])
sum(target['train'] == pred) / target['train'].shape

pred = clf.predict(data['test'])
sum(target['test'] == pred) / target['test'].shape
