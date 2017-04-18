'''
Pandas 예제

Pandas란?
- 엑셀처럼 주로 2차원(row와 column)으로 구성된 데이터를 다루는 파이썬 패키지.
- 1차원 데이터는 Series, 2차원 데이터는 DataFrame이라고 부름.

dfply 패키지
- 데이터 변환을 하다보면 중간에 수많은 임시 데이터들이 생성됨
  - 원본 > 3번째 컬럼 제거 > 4번째 컬럼에 100 곱함 > 1번 컬럼 값으로 부분합...
- 불필요한 임시변수 생성을 줄이고 앞단계 작업을 뒷단계에서 바로 받아올 수 있도록 하는 pipe가 필요
- R의 dplyr 패키지가 대표적으로, dfply는 이 dplyr의 파이썬 구현체 
'''

#%% 모듈 import
import pandas as pd
import numpy as np
import io

#%% 데이터 읽어들여 DataFrame 만들기
df = pd.read_csv(io.StringIO("""\
Name Age Gender Salary
Kim   25      M    100
Lee   29      F    150
Park  24      M    120
Choi  32      F    200
Jang  23      F    100
"""), sep='\s+')
type(df)

#%% 간단한 데이터 요약
df.shape
df.head(2)
df.tail(2)
df.describe()

#%% 데이터 조회
df['Name']
df.Name
df[0:1]
df.iloc[0:3, 1:2]
df[df.Name == 'Kim']
df.query('Name == "Jin" and Age > 23')
df.drop('Name', axis=1)
df.apply(np.cumsum)

#%% dfply을 이용한 pipe operation
from dfply import *
df >> select('Name', X.Salary)
df >> mask(X.Name >= 'Kim', X.Age < 26) >> arrange(-X.Salary) >> select(X.Age, 'Salary')
df >> groupby(X.Gender) >> summarize_each([np.mean], X.Age, 'Salary')

#%% dfply를 이용한 long <> wide 변환
dict = {}
dict['raw'] = pd.read_csv(io.StringIO('''\
Type   Key  Value
Gender   M    남성
Gender   F    여성
Name   Kim     김
Name   Lee     이
'''), sep='\s+', encoding='utf-8')
dict['aligned'] = dict['raw'] >> mask(X.Type == 'Gender') >> \
    select(X.Key, X.Value) >> rename(Gender=X.Key)

#%% dfply를 이용한 join
df >> left_join(dict['aligned']) 