# -*- coding: utf-8 -*-

'''
Tableau 예제

!pip install tableaudocumentapi
'''

from tableaudocumentapi import Workbook

wb = Workbook('data/empty.twb')

Workbook.save_as(wb, 'data/iris.twb')