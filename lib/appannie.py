# -*- coding: utf-8 -*-
'''
앱애니 API를 이용한 데이터 조회

- API key는 auth/appannie_headers.json에 둔다 (git commit에서는 제외)
'''

import requests
import json
import pandas as pd
import logging
import calendar

#%%
class AppAnnie():
  url_params = {
      'host': 'http://api.appannie.com/v1.2',
      'vertical': 'apps',
      'market': 'google-play',
  }
  params = {
      'countries': 'KR',
      'categories': 'OVERALL > GAME',
      'device': 'android',
  }

  def __init__(self, auth_file, debug=False):
    with open(auth_file) as f:
      self.headers = json.load(f)
    logging.basicConfig(level=debug and logging.DEBUG or logging.NOTSET) 
    
  def __api_call(self, url, params, result_key=None):
    response = requests.get(url, headers=self.headers, params=params)
    if not response.ok:
      raise Exception('error', response.content)
    json = response.json()
    if result_key:
      json = json[result_key]
    return pd.DataFrame(json)
  
  '''
  패키지명을 앱애니ID로 변환.
  input 순서와 output 순서가 일치하지 않을 수 있으므로 순서정렬 필요
  '''
  def packageName2ID(self, package_names):
    url = '{host}/{vertical}/{market}/package-codes2ids'.format(**self.url_params)
    params = {'package_codes': ','.join(package_names)}
    df = self.__api_call(url, params, result_key='items')
    return df.set_index(df.package_code).loc[package_names]

  '''
  top게임 랭킹을 가져옴
  - feeds: free | paid | grossing
  - granularity: daily | weekly | monthly
  - date: YYYY-MM-DD 형식
  '''
  def topGames(self, feeds='grossing', granularity='weekly', date=None, ranks=100):
    url = '{host}/intelligence/{vertical}/{market}/ranking'.format(**self.url_params)
    params = dict(self.params, 
                  feeds=feeds, granularity=granularity, ranks=ranks,
                  start_date=date, end_date=date,
                  )
    return self.__api_call(url, params=params, result_key='list')
    
  '''
  게임 한 개의 과거 실적을 가져옴
  '''
  def gameHistory(self, product_id, feeds='revenue', granularity='weekly', **kwargs):
    url = '{host}/intelligence/{vertical}/{market}/app/%s/history'\
      .format(**self.url_params) % product_id
    params = dict(self.params, feeds=feeds, granularity=granularity, **kwagrs)
    return self.__api_call(url, params=params, result_key='list')
  
  '''
  게임 한 개의 피처링선정 히스토리를 가져옴
  '''
  def gameFeaturedHistory(self, product_id, **kwargs):
    url = '{host}/{vertical}/{market}/app/%s/featured_history'\
      .format(**self.url_params) % product_id
    params = dict(countries='All', **kwargs)
    return self.__api_call(url, params=params, result_key='feature_history')
    
def get_start_end_date(year, month):
  last_day = calendar.monthrange(year, month)[1]
  return list(map(lambda x: '%d-%02d-%02d' % (year, month, x), [1, last_day]))
