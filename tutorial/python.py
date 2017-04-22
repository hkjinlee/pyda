# -*- coding: utf-8 -*-
'''
python 문법
'''

#%%
'''
from future
- python은 계속해서 문법이 변화하는 언어
- 따라서 새롭게 도입된 문법을 이용해 만든 프로그램은 과거버전 python에서는 동작하지 않을 수 있음
  - 가령, print는 python2.x에서는 예약어의 일부였음: print('a')가 아니라 print 'a'
  - 그러나 python3.x에서는 print가 함수로 변경: 따라서 print 'a'가 아니라 print('a')
- 이런 경우 python3를 기준으로 작성된 스크립트도 python2에서 실행 가능해짐
'''
from __future__ import print_function
print('Printed by print function')
from __future__ import division
print(10/3)

#%%
'''
기본연산자
'''
print(2 ** 3)
print(9 % 4)

#%%
'''
with 문법
- with A 뒤의 블럭을 시작할 때 A.__enter__(), 끝날 때 A.__exit__()을 자동 호출
- 파일을 읽기 위해 매번 file open, close를 해주어야 하는 번거로움을 with 문법으로 간략화할 수 있음
'''
class withTarget():
    def __init__(self):
        print("init()")        
    def __enter__(self):
        print("enter()")
    def __exit__(self, type, value, traceback):
        print("exit()")

with withTarget() as w:
    pass

#%%
'''
list comprehension
- 리스트의 각 요소에 특정한 operation을 실행한 결과를 다시 리스트로 만듦
'''
print([x + 1 for x in range(1, 10+1) if x % 2 == 0])