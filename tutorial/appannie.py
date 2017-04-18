'''
앱애니 API를 이용한 데이터 조회

- API key는 auth/appannie_headers.json에 둔다 (git commit에서는 제외)
'''

import requests
import json
import pandas as pd
import logging

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
    logging.basicConfig(level=logging.DEBUG) if debug
    
  def __api_call(self, url, params, result_key=None):
    response = requests.get(url, headers=self.headers, params=params)
    if not response.ok:
      raise Exception('error', response.content)
    json = response.json()
    return pd.DataFrame(result_key and json[result_key] or json)
  
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
  def topGames(self, feeds='grossing', granularity='weekly', date=None):
    url = '{host}/intelligence/{vertical}/{market}/ranking'.format(**self.url_params)
    params = { **self.params,
              'feeds': feeds,
              'granularity': granularity,
              'start_date': date,
              'end_date': date
              }
    return self.__api_call(url, params=params, result_key='list')
    
  '''
  게임 한 개의 과거 실적을 가져옴
  '''
  def gameHistory(self, product_id, feeds='revenue', granularity='weekly', **kwargs):
    url = '{host}/intelligence/{vertical}/{market}/app/%s/history'\
      .format(**self.url_params) % product_id
    params = { **self.params, **kwargs,
              'feeds': feeds,
              'granularity': granularity,
    }
    return self.__api_call(url, params=params, result_key='list')
  
  '''
  게임 한 개의 피처링선정 히스토리를 가져옴
  '''
  def gameFeaturedHistory(self, product_id, **kwargs):
    url = '{host}/{vertical}/{market}/app/%s/featured_history'\
      .format(**self.url_params) % product_id
    params = { **kwargs,
              'countries': 'All',
    }
    return self.__api_call(url, params=params)
    
appannie = AppAnnie('auth/appannie_headers.json')

#%% packageName2ID 테스트
package_names = [
    'com.webzen.muorigin.google', 
    'com.itsgames.aden',
    'com.longtukorea.snmg' ]
result = appannie.packageName2ID(package_names)

#%% weeklyTopGames 테스트
result = appannie.topGames(granularity='weekly', date='2017-04-01')

#%% 게임 history 테스트
result = appannie.gameHistory('20600005637922', granularity='monthly',
                              start_date='2017-01-01', end_date='2017-03-31')

#%% 게임 feature history 테스트
result = appannie.gameFeaturedHistory('20600005637922', start_date='2017-01-01', end_date='2017-01-31')
