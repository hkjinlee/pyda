# -*- coding: utf-8 -*-

'''
Tensorflow 튜토리얼

이름의 유래:
- tensor란 그냥 데이터 행렬(matrix)이라고 생각하면 됨.
- tensorflow: tensor가 여러 단계를 흐르며(flow) 원하는 모양으로 가공되는 과정을 의미

설치:
!pip install tensorflow
'''

from __future__ import absolute_import
from __future__ import print_function

import tensorflow as tf
import pandas as pd
import numpy as np

#%%
'''
세션(session)과 연산(operation. 이하 op)
- 세션은 연산의 실행환경
- op는 데이터를 뱉어내는 하나의 연산. 아래의 hello는 항상 "Hello, world"라는 상수를 뱉는 연산임
- session.run()에 op를 넣어주면 연산이 실행됨
- 실행이 끝나고 나면 close()해주어야 내부적으로 할당한 리소스가 반환
'''
sess = tf.Session()
hello = tf.constant('Hello, world')

result = sess.run(hello)
print(result)
sess.close()

#%%
'''
그래프(graph): op들의 연결
- 아래 예제에서는 op 3개를 정의
  - x: 상수가 아닌 변수 op. 변수가 들어갈 경우 반드시 연산 전에 초기화를 해주어야 함
  - two: 앞서의 hello와 마찬가지로 항상 2를 뱉어내는 상수(constant) op
  - outcome: var와 two의 결합(즉, x의 2제곱)으로 정의된 op
- session은 두 개의 op를 실행함
  - x.initializer: x를 초기화
  - outcome: 실제로 outcome을 실행
'''
sess = tf.Session()
x = tf.Variable(range(1, 10+1))
two = tf.constant(2)
outcome = x ** two

sess.run(x.initializer)
print(sess.run(outcome))
sess.close()

#%%
'''
변수의 할당(assignment)
- python의 with 문법을 사용하면 session.close()가 자동적으로 호출됨
- op가 뱉어내는 값을 변수에 저장하고 싶다면 tf.assign() op를 선언
  - update는 x에 2를 더해서 다시 x에 넣는 연산 op (+ 대신 add()를 사용. 결과는 동일)
  - update가 실행되기 전까지는 x는 그냥 0으로 남아 있음
'''
x = tf.Variable(0)
update = tf.assign(x, tf.add(x, two))

with tf.Session() as sess:
  sess.run(x.initializer)
  print('var = {}', sess.run(x))
  sess.run(update)
  print('var = {}', sess.run(x))
  sess.run(update)
  print('var = {}', sess.run(x))

#%%
'''
Placeholder
- 초기값이 존재하는 variable과는 달리 실행단계에 값을 넣어줄 수 있는 op
- 여러 변수를 한번에 초기화하고 싶다면 tf.global_variables_initializer() 이용
  - 아래 예제에서는 변수가 x 하나밖에 없기 때문에 사실 차이는 없음
'''
x = tf.Variable(range(1, 10+1))
a = tf.placeholder(tf.int32)
b = tf.placeholder(tf.int32)
y = a * x + b

with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  print(sess.run(y, feed_dict={a: 2, b: 100}))
  
#%%
'''
tf.contrib.learn을 이용한 간단한 머신러닝 classifier 실습

- 원래 skflow라는 scikit-learn 스타일의 3rd party 모듈을 tensorflow로 합병
- 먼저 tutorial/sklearn.py를 보고 오는 편이 좋음
- 선형분류기(LinearClassifier)와 딥러닝(DNNClassifier)를 이용하여 iris 데이터 분류
'''
from sklearn.model_selection import train_test_split

def get_x(iris):
  return iris.iloc[:, 0:4].values

def get_y(iris):
  return iris['type'].values.codes.astype('int32')

def fit_and_evaluate(clf):    
  clf.fit(x=get_x(iris_train), y=get_y(iris_train), steps=100)
  return clf.evaluate(x=get_x(iris_test), y=get_y(iris_test), steps=1)['accuracy']

iris = pd.read_csv('data/iris.csv')
iris['type'] = iris['type'].astype('category')

iris_train, iris_test = train_test_split(iris)

feature_cols = tf.contrib.learn.infer_real_valued_columns_from_input(
    iris_train.iloc[:, 0:4])

clf_linear = tf.contrib.learn.LinearClassifier(
    feature_columns=feature_cols, n_classes=iris['type'].nunique())
clf_dnn = tf.contrib.learn.DNNClassifier(
    feature_columns=feature_cols, n_classes=iris['type'].nunique(),
    hidden_units=[10, 20, 10])

accuracies = [ fit_and_evaluate(clf) for clf in [clf_linear, clf_dnn]]
print('Accracy: linear = {:.2f}, DNN = {:.2f}'.format(*accuracies))

#%%
'''

'''

