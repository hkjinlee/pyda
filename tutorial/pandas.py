# -*- coding: utf-8 -*-

'''
Pandas 교육용 스크립트
'''
import pandas as pd
import numpy as np
import io

'''
데이터 읽어들여 DataFrame 만들기
'''
df = pd.read_csv(io.StringIO("""\
Name Age Gender Salary
Kim   25      M    100
Lee   29      F    150
Park  24      M    120
Choi  32      F    200
Jang  23      F    100
"""), sep='\s+')
type(df)

'''
간단한 데이터 요약
'''
df.shape
df.head(2)
df.tail(2)
df.describe()

'''
데이터 조회
'''
df['Name']
df.Name
df[0:1]
df.iloc[0:3, 1:2]
df[df.Name == 'Kim']
df.query('Name == "Jin" and Age > 23')
df.drop('Name', axis=1)
df.apply(np.cumsum)

'''
dfply을 이용한 pipe operation
'''
from dfply import *
df >> select('Name', X.Salary)
df >> mask(X.Name >= 'Kim', X.Age < 26) >> arrange(-X.Salary) >> select(X.Age, 'Salary')
df >> groupby(X.Gender) >> summarize_each([np.mean], X.Age, 'Salary')

'''
dfply를 이용한 long <> wide 변환
'''
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

'''
dfply를 이용한 join
'''
df >> left_join(dict['aligned']) 

'''
ggplot을 이용한 plotting
'''
import ggplot